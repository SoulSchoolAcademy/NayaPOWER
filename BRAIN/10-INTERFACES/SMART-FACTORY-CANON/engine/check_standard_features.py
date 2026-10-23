#!/usr/bin/env python3
"""Check a built Factory app against the standard-feature contracts.

The contracts live in templates-registry.json, beside this checker, under
``standard_feature_contracts``.  The checker intentionally uses only the
Python standard library so any seat can run it from a clean checkout.

A feature passes only when the shipped bytes contain both the surface and
the working mechanism named by its contract.  A heading, a route label, or
an unbound button is not enough.

Examples:
    python3 check_standard_features.py --template personal
    python3 check_standard_features.py https://example.workers.dev/
    python3 check_standard_features.py path/to/app.html --format json
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY = HERE / "templates-registry.json"
SUPPORTED_KINDS = {
    "count_at_least",
    "dom_exists",
    "route_targets",
    "source_regex",
    "text_contains",
}
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class Node:
    def __init__(self, tag: str, attrs: dict[str, str] | None = None,
                 parent: "Node | None" = None):
        self.tag = tag
        self.attrs = attrs or {}
        self.parent = parent
        self.children: list[Node] = []
        self.text_parts: list[str] = []

    def walk(self) -> Iterable["Node"]:
        yield self
        for child in self.children:
            yield from child.walk()

    def descendants(self) -> Iterable["Node"]:
        for child in self.children:
            yield child
            yield from child.descendants()

    def text(self) -> str:
        parts = list(self.text_parts)
        for child in self.children:
            child_text = child.text()
            if child_text:
                parts.append(child_text)
        return normalize_space(" ".join(parts))

    def own_text(self) -> str:
        return normalize_space(" ".join(self.text_parts))


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("[document]")
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        clean = {key.lower(): (value or "") for key, value in attrs}
        node = Node(tag.lower(), clean, self.stack[-1])
        self.stack[-1].children.append(node)
        if node.tag not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]):
        clean = {key.lower(): (value or "") for key, value in attrs}
        node = Node(tag.lower(), clean, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str):
        if data:
            self.stack[-1].text_parts.append(data)


class Document:
    def __init__(self, raw: str):
        self.raw = raw
        parser = DocumentParser()
        parser.feed(raw)
        parser.close()
        self.root = parser.root
        self.script_text = "\n".join(
            node.text() for node in self.root.walk() if node.tag == "script"
        )
        self.style_text = "\n".join(
            node.text() for node in self.root.walk() if node.tag == "style"
        )

    def source_for_scope(self, scope: str) -> str:
        if scope == "script":
            return self.script_text
        if scope == "style":
            return self.style_text
        if scope == "html":
            return self.raw
        if scope == "all":
            return self.raw
        raise ValueError(f"unsupported source scope: {scope}")


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def split_selector_groups(selector: str) -> list[str]:
    groups: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    for index, char in enumerate(selector):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        elif char == "," and depth == 0:
            groups.append(selector[start:index].strip())
            start = index + 1
    groups.append(selector[start:].strip())
    return [group for group in groups if group]


def split_descendant_parts(group: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    for index, char in enumerate(group):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        elif char.isspace() and depth == 0:
            if start < index:
                parts.append(group[start:index])
            start = index + 1
    if start < len(group):
        parts.append(group[start:])
    return [part for part in parts if part]


class SimpleSelector:
    def __init__(self, text: str):
        self.text = text
        self.tag: str | None = None
        self.id_value: str | None = None
        self.classes: list[str] = []
        self.attrs: list[tuple[str, str | None, str | None]] = []
        self._parse(text)

    def _parse(self, text: str):
        position = 0
        tag_match = re.match(r"(?:\*|[A-Za-z][A-Za-z0-9_-]*)", text)
        if tag_match:
            value = tag_match.group(0).lower()
            self.tag = None if value == "*" else value
            position = tag_match.end()
        token_re = re.compile(
            r"#(?P<id>[A-Za-z0-9_-]+)|\.(?P<class>[A-Za-z0-9_-]+)|\["
            r"(?P<attr>[A-Za-z0-9_-]+)(?:\s*(?P<op>\*=|~=|=)\s*"
            r"(?:'(?P<sq>[^']*)'|\"(?P<dq>[^\"]*)\"|(?P<bare>[^\]]+)))?\]"
        )
        while position < len(text):
            match = token_re.match(text, position)
            if not match:
                raise ValueError(f"unsupported selector syntax: {text}")
            if match.group("id"):
                self.id_value = match.group("id")
            elif match.group("class"):
                self.classes.append(match.group("class"))
            else:
                value = match.group("sq")
                if value is None:
                    value = match.group("dq")
                if value is None and match.group("bare") is not None:
                    value = match.group("bare").strip()
                self.attrs.append((match.group("attr").lower(), match.group("op"), value))
            position = match.end()

    def matches(self, node: Node) -> bool:
        if node.tag == "[document]":
            return False
        if self.tag and node.tag != self.tag:
            return False
        if self.id_value and node.attrs.get("id") != self.id_value:
            return False
        node_classes = set(node.attrs.get("class", "").split())
        if any(class_name not in node_classes for class_name in self.classes):
            return False
        for attr, operator, expected in self.attrs:
            if attr not in node.attrs:
                return False
            if operator is None:
                continue
            actual = node.attrs.get(attr, "")
            if operator == "=" and actual != (expected or ""):
                return False
            if operator == "*=" and (expected or "") not in actual:
                return False
            if operator == "~=" and (expected or "") not in actual.split():
                return False
        return True


def select(document: Document, selector: str) -> list[Node]:
    found: list[Node] = []
    seen: set[int] = set()
    for group in split_selector_groups(selector):
        current = [document.root]
        for part in split_descendant_parts(group):
            simple = SimpleSelector(part)
            next_nodes: list[Node] = []
            for base in current:
                for node in base.descendants():
                    if simple.matches(node):
                        next_nodes.append(node)
            current = next_nodes
        for node in current:
            marker = id(node)
            if marker not in seen:
                seen.add(marker)
                found.append(node)
    return found


def node_evidence(node: Node) -> str:
    label = node.tag
    if node.attrs.get("id"):
        label += f"#{node.attrs['id']}"
    if node.attrs.get("class"):
        label += "." + ".".join(node.attrs["class"].split()[:3])
    text = node.text()
    if text:
        label += f" text={text[:90]!r}"
    return label


def evaluate_check(document: Document, check: dict[str, Any]) -> dict[str, Any]:
    kind = check["kind"]
    result: dict[str, Any] = {
        "id": check["id"],
        "kind": kind,
        "label": check.get("label", check["id"]),
        "requirement": check.get("requirement", "required"),
        "pass": False,
        "evidence": [],
    }

    if kind == "dom_exists":
        nodes = select(document, check["selector"])
        result["pass"] = bool(nodes)
        result["observed"] = {"matches": len(nodes)}
        result["evidence"] = [node_evidence(node) for node in nodes[:3]]

    elif kind == "count_at_least":
        nodes = select(document, check["selector"])
        minimum = int(check["minimum"])
        result["pass"] = len(nodes) >= minimum
        result["observed"] = {"matches": len(nodes), "minimum": minimum}
        result["evidence"] = [node_evidence(node) for node in nodes[:5]]

    elif kind == "text_contains":
        nodes = select(document, check["selector"])
        combined = normalize_space(" ".join(node.text() for node in nodes))
        values = [str(value) for value in check.get("values", [])]
        matched = [value for value in values if value.lower() in combined.lower()]
        if check.get("match", "any") == "all":
            result["pass"] = len(matched) == len(values)
        else:
            result["pass"] = bool(matched)
        result["observed"] = {"matched": matched, "values": values}
        result["evidence"] = [f"matched {value!r}" for value in matched]

    elif kind == "route_targets":
        nodes = select(document, check["selector"])
        patterns = [str(pattern) for pattern in check.get("patterns", [])]
        matched_patterns: list[str] = []
        evidence: list[str] = []
        route_attrs = ("href", "data-hub", "data-goto", "data-url", "title", "aria-label")
        for pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            for node in nodes:
                haystacks = [node.text()] + [node.attrs.get(attr, "") for attr in route_attrs]
                if any(regex.search(value or "") for value in haystacks):
                    matched_patterns.append(pattern)
                    evidence.append(node_evidence(node))
                    break
        minimum = int(check["minimum"])
        result["pass"] = len(matched_patterns) >= minimum
        result["observed"] = {
            "matched_patterns": matched_patterns,
            "matched": len(matched_patterns),
            "minimum": minimum,
            "candidate_routes": len(nodes),
        }
        result["evidence"] = evidence[:8]

    elif kind == "source_regex":
        source = document.source_for_scope(str(check.get("scope", "all")))
        pattern = str(check["pattern"])
        match = re.search(pattern, source, flags=re.DOTALL)
        result["pass"] = match is not None
        result["observed"] = {"pattern": pattern, "scope": check.get("scope", "all")}
        if match:
            excerpt = normalize_space(match.group(0))[:220]
            result["evidence"] = [excerpt]

    else:  # validate_contracts normally rejects this first.
        raise ValueError(f"unsupported check kind: {kind}")

    return result


def validate_contracts(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    contracts = registry.get("standard_feature_contracts")
    if not isinstance(contracts, dict):
        return ["templates-registry.json has no standard_feature_contracts object"]
    features = contracts.get("features")
    if not isinstance(features, list):
        return ["standard_feature_contracts.features is not a list"]
    if len(features) != 13:
        errors.append(f"expected 13 standard features, found {len(features)}")

    feature_ids: set[str] = set()
    codes: set[str] = set()
    check_ids: set[str] = set()
    for feature in features:
        if not isinstance(feature, dict):
            errors.append("a standard feature is not an object")
            continue
        feature_id = feature.get("id")
        code = feature.get("code")
        if not feature_id or feature_id in feature_ids:
            errors.append(f"duplicate or missing feature id: {feature_id!r}")
        feature_ids.add(str(feature_id))
        if not code or code in codes:
            errors.append(f"duplicate or missing feature code: {code!r}")
        codes.add(str(code))
        if not feature.get("promise"):
            errors.append(f"feature {feature_id} has no promise")
        if not feature.get("pass_standard"):
            errors.append(f"feature {feature_id} has no pass_standard")
        checks = feature.get("checks")
        if not isinstance(checks, list) or not checks:
            errors.append(f"feature {feature_id} has no checks")
            continue
        for check in checks:
            if not isinstance(check, dict):
                errors.append(f"feature {feature_id} has a non-object check")
                continue
            check_id = check.get("id")
            if not check_id or check_id in check_ids:
                errors.append(f"duplicate or missing check id: {check_id!r}")
            check_ids.add(str(check_id))
            if check.get("kind") not in SUPPORTED_KINDS:
                errors.append(f"check {check_id} has unsupported kind {check.get('kind')!r}")
            if check["kind"] in {"dom_exists", "count_at_least", "text_contains", "route_targets"}:
                if not check.get("selector"):
                    errors.append(f"check {check_id} has no selector")
            if check["kind"] == "count_at_least" and not isinstance(check.get("minimum"), int):
                errors.append(f"check {check_id} has no integer minimum")
            if check["kind"] == "route_targets":
                if not isinstance(check.get("patterns"), list) or not check["patterns"]:
                    errors.append(f"check {check_id} has no route patterns")
                if not isinstance(check.get("minimum"), int):
                    errors.append(f"check {check_id} has no integer minimum")
            if check["kind"] == "text_contains":
                if not isinstance(check.get("values"), list) or not check["values"]:
                    errors.append(f"check {check_id} has no values")
            if check["kind"] == "source_regex" and not check.get("pattern"):
                errors.append(f"check {check_id} has no pattern")

    expected_codes = {f"S{number}" for number in range(1, 14)}
    if codes != expected_codes:
        errors.append(f"feature codes must be S1-S13; found {sorted(codes)}")
    return errors


def fetch_url(url: str) -> tuple[bytes, dict[str, Any]]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "NayaFactoryStandardFeatureChecker/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            return body, {
                "source": url,
                "status": response.status,
                "final_url": response.geturl(),
            }
    except (http.client.IncompleteRead, urllib.error.URLError, TimeoutError):
        # Some Cloudflare responses are truncated by urllib through this
        # environment's proxy at exactly 128 KiB.  Curl is the existing
        # command-line HTTP tool on the Factory machines and reads the
        # same response completely; use it only as a fetch fallback.
        with tempfile.TemporaryDirectory(prefix="naya-factory-check-") as tmp:
            output = Path(tmp) / "body.html"
            completed = subprocess.run(
                [
                    "curl",
                    "--location",
                    "--fail",
                    "--compressed",
                    "--silent",
                    "--show-error",
                    "--user-agent",
                    "NayaFactoryStandardFeatureChecker/1.0",
                    "--output",
                    str(output),
                    "--write-out",
                    "%{http_code} %{url_effective}",
                    url,
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if completed.returncode != 0 or not output.exists():
                raise RuntimeError(
                    f"could not fetch {url}: {completed.stderr.strip() or completed.stdout.strip()}"
                )
            status_text, final_url = completed.stdout.strip().split(" ", 1)
            return output.read_bytes(), {
                "source": url,
                "status": int(status_text),
                "final_url": final_url,
                "fetch_fallback": "curl (urllib response was incomplete)",
            }


def load_target(target: str | None, registry_path: Path,
                registry: dict[str, Any], template_key: str | None,
                ) -> tuple[bytes, dict[str, Any]]:
    if template_key:
        templates = registry.get("templates", {})
        entry = templates.get(template_key)
        if entry is None:
            missing = registry.get("missing", {}).get(template_key)
            detail = missing or f"template {template_key!r} is not in the registry"
            raise ValueError(f"template not buildable: {detail}")
        target_path = (registry_path.parent / entry["file"]).resolve()
        body = target_path.read_bytes()
        observed_md5 = hashlib.md5(body).hexdigest()
        metadata = {
            "source": str(target_path),
            "template": template_key,
            "registry_file": entry["file"],
            "registry_md5": entry.get("md5"),
            "observed_md5": observed_md5,
            "registry_md5_matches": observed_md5 == entry.get("md5"),
            "registry_bytes": entry.get("bytes"),
            "observed_bytes": len(body),
        }
        if not metadata["registry_md5_matches"]:
            raise ValueError(
                f"template base drift for {template_key}: observed md5 {observed_md5}, "
                f"registry md5 {entry.get('md5')}"
            )
        return body, metadata

    if not target:
        raise ValueError("provide a target file/URL or --template <key>")
    if target.startswith(("https://", "http://")):
        return fetch_url(target)
    target_path = Path(target).expanduser().resolve()
    return target_path.read_bytes(), {"source": str(target_path)}


def evaluate(body: bytes, metadata: dict[str, Any], registry: dict[str, Any],
             twin: dict[str, Any] | None = None) -> dict[str, Any]:
    html = body.decode("utf-8", errors="ignore")
    document = Document(html)
    feature_results: list[dict[str, Any]] = []

    for feature in registry["standard_feature_contracts"]["features"]:
        check_results = [evaluate_check(document, check) for check in feature["checks"]]
        required = [result for result in check_results if result["requirement"] == "required"]
        groups: dict[str, list[dict[str, Any]]] = {}
        for result in check_results:
            requirement = result["requirement"]
            if requirement.startswith("any:"):
                groups.setdefault(requirement.split(":", 1)[1], []).append(result)
        failed_required = [result["id"] for result in required if not result["pass"]]
        failed_groups = [
            group for group, results in groups.items()
            if not any(result["pass"] for result in results)
        ]
        passed = not failed_required and not failed_groups
        feature_results.append({
            "code": feature["code"],
            "id": feature["id"],
            "name": feature["name"],
            "status": "PASS" if passed else "FAIL",
            "promise": feature["promise"],
            "pass_standard": feature["pass_standard"],
            "failed_required_checks": failed_required,
            "failed_any_groups": failed_groups,
            "checks": check_results,
        })

    passed_count = sum(result["status"] == "PASS" for result in feature_results)
    report = {
        "checker": "check_standard_features.py",
        "contract_version": registry["standard_feature_contracts"].get("version"),
        "target": metadata,
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "score": {"passed": passed_count, "total": len(feature_results)},
        "features": feature_results,
    }
    # Step 6 annex: the §10 design-language checks ride in every report (so
    # every build receipt carries them) under their own status. They never
    # alter the S1-S13 score above -- the strict gate's arithmetic is
    # untouched; the annex is the visible verification the audit asked for.
    # A twin that cannot be loaded or parsed yields an UNAVAILABLE annex
    # with the reason named -- never a silent pass.
    try:
        twin_obj = twin
        twin_source = "argument"
        if twin_obj is None:
            twin_obj, twin_source = load_design_twin()
        annex = evaluate_design_language(document, design_params(twin_obj))
        annex["twin_source"] = twin_source
    except Exception as exc:
        annex = {
            "checker": "check_standard_features.py -- design-language annex "
                       "(Factory step 6)",
            "status": "UNAVAILABLE",
            "reason": str(exc),
            "checks": [],
            "not_mechanically_checkable": [
                {"item": e["item"], "name": e["name"]}
                for e in NOT_MECHANICALLY_CHECKABLE],
        }
    report["design_language"] = annex
    return report


# ---------------------------------------------------------------------------
# Design-language checks -- Factory Contract-Home step 6 (audit §3 step 6:
# "Wire the gate to the same source, visibly").
#
# The §10 Same-Language Check (DESIGN-LANGUAGE §10) names 24 items; the ones
# that are mechanically checkable from page bytes are implemented here. Every
# rule VALUE comes from the machine twin (NAYA-DESIGN-CONTRACT.machine.json),
# extracted exactly once by design_params(). The build gate (the processor
# loads THIS module from origin/main), the standalone CLI, and the Factory
# page's "Check against the contract" door all consume the same parameter
# object -- the generator embeds design_params() output verbatim in the page
# and the door's in-page logic reads that same data. No hand-duplicated rule
# values anywhere.
#
# Items that cannot be checked mechanically are NAMED in
# NOT_MECHANICALLY_CHECKABLE (carried in every report and shown by the door),
# never silently skipped and never faked. Mechanical scope boundary, stated
# once: the checks read the page's own bytes -- inline styles and <style>
# CSS. External stylesheets are not in the bytes, in either runtime.
# ---------------------------------------------------------------------------

DESIGN_TWIN_NAME = "NAYA-DESIGN-CONTRACT.machine.json"
DESIGN_TWIN_REL = ("BRAIN/10-INTERFACES/SMART-FACTORY-CANON/"
                   + DESIGN_TWIN_NAME)
DESIGN_REPO_CLONE = Path.home() / "workspace" / "nayapower-repo"
DESIGN_SNAPSHOT_TWIN = (Path.home() / "workspace" / "factory-pipeline"
                        / "canon" / DESIGN_TWIN_NAME)

# §10 items with no mechanical form (render, interaction, motion-measurement,
# semantic classification, or process evidence). Named in every report.
NOT_MECHANICALLY_CHECKABLE = [
    {"item": 1, "name": "Field",
     "why": "a layered near-black gradient ground is a rendered-appearance judgment; the twin carries no gradient parameters to test against"},
    {"item": 2, "name": "Full width",
     "why": "whether content owns the width is a layout outcome; a max-width in source is legitimate on cards and media, so no source rule separates cage from component"},
    {"item": 3, "name": "Shapes",
     "why": "rectangle-vs-circle is rendered geometry (border-radius against rendered aspect), not source bytes"},
    {"item": 4, "name": "No voids",
     "why": "empty space exists only after layout; source cannot see a desert"},
    {"item": 5, "name": "Twin pluses",
     "why": "presence is countable, but 'extreme corners, identical construction, opens the right drawer' is position + behavior -- render and click evidence"},
    {"item": 6, "name": "Smart Tabs",
     "why": "'tabs actually scroll' is interaction behavior on the rendered page"},
    {"item": 7, "name": "Drift",
     "why": "the check IS a pixel-motion measurement (median-of-3 at phone width); no source form exists"},
    {"item": 9, "name": "Color jobs unmixed",
     "why": "which job a color serves (section vs flow vs board mapping) is semantic classification; the mechanical edge -- non-walk hues confined to board contexts -- is inside DL-WALK"},
    {"item": 12, "name": "Jewel tones",
     "why": "the twin names the jewel hexes but sets no saturation/lightness boundary a 'pastel' test could read"},
    {"item": 13, "name": "Elevation",
     "why": "the recipe (inset top light + inset bottom shade + drop shadow) lives in prose; the twin parameterizes no shadow values to test against"},
    {"item": 14, "name": "Wells vs buttons",
     "why": "recessed-vs-raised is a rendered depth relationship plus a semantic role call (input vs action vs display)"},
    {"item": 15, "name": "One button DNA",
     "why": "the twin's button language is prose rules without numeric parameters (the 44px floor and state list live in the human text, not the twin's data)"},
    {"item": 16, "name": "Icons are jewels",
     "why": "'legible at a glance, unique per destination' is a rendered judgment"},
    {"item": 18, "name": "Orbs carry people + numbers",
     "why": "a flowing orb vs a flat disc is rendered appearance + animation state"},
    {"item": 19, "name": "Living data",
     "why": "'a human sentence, not a naked number' is a semantic read of the content"},
    {"item": 20, "name": "Timestamps alive",
     "why": "the check requires watching the stamp recompute over 60 seconds of render time"},
    {"item": 21, "name": "Motion has an off switch",
     "why": "requires toggling the Calm setting and emulating reduced-motion on the rendered page"},
    {"item": 22, "name": "No dead buttons (functional half)",
     "why": "DL-DEAD covers the checkable slice (no ignition styling exists); whether a click DOES something real requires clicking everything"},
    {"item": 23, "name": "Nothing recreated",
     "why": "provenance lives in the build brief and the harvest sources it names, not in page bytes"},
    {"item": 24, "name": "Edit-only respected",
     "why": "a diff discipline over the change itself; the page alone cannot show what it replaced"},
]


def load_design_twin(explicit: str | Path | None = None,
                     ) -> tuple[dict[str, Any], str]:
    """Load the machine twin -- the one source every design check reads.

    Order: an explicit path; the twin beside this checker in a repo checkout
    (canon root, or a vendored canon folder); origin/main via git show from
    the repo clone (the same mechanism the build processor uses to load this
    checker, so the gate reads canon from main even when this module was
    exec'd from a temp file); the pipeline's vendored snapshot. Raises
    ValueError naming every attempted source -- a missing twin is a loud
    failure, never a silent pass.
    """
    attempts: list[str] = []
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    candidates.append(HERE.parent / DESIGN_TWIN_NAME)
    candidates.append(HERE / DESIGN_TWIN_NAME)
    for cand in candidates:
        attempts.append(str(cand))
        try:
            return (json.loads(cand.read_text(encoding="utf-8")),
                    f"file {cand}")
        except Exception:
            pass
    attempts.append(f"git show origin/main:{DESIGN_TWIN_REL} "
                    f"(clone {DESIGN_REPO_CLONE})")
    try:
        out = subprocess.run(
            ["git", "-C", str(DESIGN_REPO_CLONE), "show",
             f"origin/main:{DESIGN_TWIN_REL}"],
            capture_output=True, timeout=30)
        if out.returncode == 0:
            return (json.loads(out.stdout.decode("utf-8")),
                    "repo clone origin/main (git show)")
    except Exception:
        pass
    attempts.append(str(DESIGN_SNAPSHOT_TWIN))
    try:
        return (json.loads(DESIGN_SNAPSHOT_TWIN.read_text(encoding="utf-8")),
                f"vendored snapshot {DESIGN_SNAPSHOT_TWIN}")
    except Exception:
        pass
    raise ValueError("machine twin unavailable; tried: "
                     + "; ".join(attempts))


def design_params(twin: dict[str, Any]) -> dict[str, Any]:
    """Extract THE check parameters from the machine twin. This function is
    the single place rule values leave the twin: the build checker runs on
    its output, and the Factory page's door embeds its output verbatim.
    Raises ValueError on a twin whose checkable data is missing or corrupt
    -- a corrupted rule value fails loud, here, before any page is judged.
    """
    def bad(what: str) -> ValueError:
        return ValueError(f"machine twin: {what}")

    walk_sec = twin.get("spectrum_walk") or {}
    order = [str(h).lower() for h in (walk_sec.get("order") or [])]
    if len(order) < 2 or any(not re.fullmatch(r"#[0-9a-f]{6}", h)
                             for h in order):
        raise bad("spectrum_walk.order is missing or not a hex list")
    names = [str(n) for n in (walk_sec.get("names") or [])]
    if len(names) != len(order):
        names = list(order)
    typo = twin.get("typography") or {}
    floor = (typo.get("body_px") or {}).get("floor")
    if not isinstance(floor, (int, float)) or not (4 <= floor <= 100):
        raise bad("typography.body_px.floor is missing or implausible")
    board_only = [str(e.get("hex")).lower()
                  for e in (twin.get("smartnote_board_mapping") or {})
                  .get("entries", [])
                  if e.get("board_mapping_only") and e.get("hex")]
    return {
        "source": DESIGN_TWIN_NAME,
        "contract_version": twin.get("version"),
        "walk": {"order": order, "names": names,
                 "wraps": bool(walk_sec.get("wraps_to_first", True))},
        "type_floor_px": floor,
        # §10.8's own evidence names --ac/--igc/--rc as the sequence source;
        # the Factory grammar adds --sec (rail/section color). Member
        # carriers color the pieces inside a zone (--sc cards, --tc template
        # cards, --tone the gem echo of --tc).
        "sequence_carriers": ["--sec", "--ac", "--igc", "--rc"],
        "member_carriers": ["--sc", "--tc", "--tone"],
        # SmartNote board sections are the one place non-walk hues may live
        # (twin: the mapping "may name non-walk hues; those non-walk hues
        # are forbidden everywhere else").
        "board_mapping_only_hexes": board_only,
        "board_context_classes": ["sn-board", "smartnote-board"],
        "board_context_attr": "data-board",
        "board_context_value": "smartnote",
        # DL-REST: spectrum at rest on interactive chrome is the failure the
        # twin's lighting states define (idle = white light; hover = the
        # element's own color ignites). §10.10's sole named exception:
        "rest_exceptions": ["life-with-naya", "lwn"],
        "interactive_tags": ["a", "button", "input", "select", "textarea"],
        "interactive_class_fragments": ["btn", "tab", "chip", "toggle",
                                        "pill"],
        # DL-CHIPS: contents chips are chip-classed elements grouped by
        # their parent (the Reports-eye steer: distinct spectrum colors,
        # never a same-color cluster).
        "chip_class_marker": "chip",
        "not_mechanically_checkable": [
            {"item": e["item"], "name": e["name"]}
            for e in NOT_MECHANICALLY_CHECKABLE],
    }


_HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


def _norm_hex(token: str) -> str:
    token = token.lower()
    if len(token) == 4:
        token = "#" + "".join(c * 2 for c in token[1:])
    return token


def _hexes_in(value: str) -> list[str]:
    return [_norm_hex(m.group(0)) for m in _HEX_RE.finditer(value or "")]


def _css_top_blocks(css: str) -> list[tuple[str, str]]:
    """Top-level (selector, full text) blocks, comments/strings respected --
    the same brace discipline the page generator uses."""
    blocks, i, n = [], 0, len(css)
    while i < n:
        while i < n:
            if css[i].isspace():
                i += 1
            elif css.startswith("/*", i):
                j = css.find("*/", i + 2)
                i = n if j < 0 else j + 2
            else:
                break
        if i >= n:
            break
        start = i
        while i < n and css[i] not in "{;":
            if css.startswith("/*", i):
                j = css.find("*/", i + 2)
                i = n if j < 0 else j + 2
            elif css[i] in "\"'":
                q = css[i]
                i += 1
                while i < n and css[i] != q:
                    i += 2 if css[i] == "\\" else 1
                i += 1
            else:
                i += 1
        if i >= n:
            break
        if css[i] == ";":
            i += 1
            continue
        selector = css[start:i].strip()
        depth, j = 0, i
        while j < n:
            if css.startswith("/*", j):
                k = css.find("*/", j + 2)
                j = n if k < 0 else k + 2
                continue
            if css[j] in "\"'":
                q = css[j]
                j += 1
                while j < n and css[j] != q:
                    j += 2 if css[j] == "\\" else 1
                j += 1
                continue
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        blocks.append((selector, css[start:j + 1]))
        i = j + 1
    return blocks


def _parse_decls(body: str) -> dict[str, str]:
    decls: dict[str, str] = {}
    for part in body.split(";"):
        if ":" not in part:
            continue
        prop, value = part.split(":", 1)
        prop = prop.strip().lower()
        if prop:
            decls[prop] = value.strip()
    return decls


def parse_css_rules(css_text: str) -> list[dict[str, Any]]:
    """Flatten a stylesheet to rules: {selector (one group), decls, media}.
    @media/@supports are recursed; @keyframes/@font-face carry no element
    rules and are skipped."""
    rules: list[dict[str, Any]] = []

    def walk(css: str, media: bool):
        for selector, text in _css_top_blocks(css):
            low = selector.lower()
            if low.startswith(("@media", "@supports")):
                walk(text[text.index("{") + 1:text.rindex("}")], True)
                continue
            if low.startswith("@"):
                continue
            body = text[text.index("{") + 1:text.rindex("}")]
            decls = _parse_decls(body)
            for group in split_selector_groups(selector):
                rules.append({"selector": group, "decls": decls,
                              "media": media})

    walk(css_text or "", False)
    return rules


_STATE_PSEUDO_RE = re.compile(
    r":(hover|focus-visible|focus-within|focus|active)(?![\w-])")
_STRIP_PSEUDO_RE = re.compile(
    r"::[A-Za-z-]+(\([^()]*\))?"
    r"|:(hover|focus-visible|focus-within|focus|active)(?![\w-])")


def _base_selector(selector: str) -> str:
    """The selector with STATE pseudo-classes and pseudo-elements stripped
    (state rules and their rest rules share a base). Structural pseudos
    (:root, :nth-child) are kept: the selector engine cannot match them, so
    such rules simply never assign carriers or ignition to elements -- a
    :root custom property is a var() source (see DesignContext.root_vars),
    not an element's own carried color."""
    base = _STRIP_PSEUDO_RE.sub("", selector)
    return normalize_space(base) or "*"


def _has_state(selector: str) -> bool:
    return bool(_STATE_PSEUDO_RE.search(selector))


class DesignContext:
    """Parsed page + rules + resolved custom properties, shared by the
    design checks (and mirrored by the door's in-page logic)."""

    def __init__(self, document: Document, params: dict[str, Any]):
        self.doc = document
        self.params = params
        self.rules = parse_css_rules(document.style_text)
        self.walk = params["walk"]["order"]
        self.walk_set = set(self.walk)
        self.walk_index = {h: i for i, h in enumerate(self.walk)}
        self.root_vars: dict[str, str] = {}
        for rule in self.rules:
            if rule["selector"].strip() == ":root":
                for prop, value in rule["decls"].items():
                    if prop.startswith("--"):
                        self.root_vars[prop] = value
        self._match_cache: dict[str, set[int]] = {}
        self._inline_cache: dict[int, dict[str, str]] = {}

    def resolve(self, value: str) -> str:
        """Resolve var(--x[, fallback]) against :root, a few passes."""
        for _ in range(3):
            m = re.search(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]*))?\)", value)
            if not m:
                break
            repl = self.root_vars.get(m.group(1), m.group(2) or "")
            value = value[:m.start()] + repl + value[m.end():]
        return value

    def matched(self, base_selector: str) -> set[int]:
        if base_selector not in self._match_cache:
            try:
                nodes = select(self.doc, base_selector)
                self._match_cache[base_selector] = {id(n) for n in nodes}
            except Exception:
                self._match_cache[base_selector] = set()
        return self._match_cache[base_selector]

    def inline_decls(self, node: Node) -> dict[str, str]:
        key = id(node)
        if key not in self._inline_cache:
            self._inline_cache[key] = _parse_decls(node.attrs.get("style", ""))
        return self._inline_cache[key]

    def carrier_value(self, node: Node, carriers: list[str],
                      ) -> tuple[str | None, str | None]:
        """(carrier, resolved hex) for the first carrier (in params order)
        the element carries, inline first, then matched rules in order."""
        inline = self.inline_decls(node)
        for carrier in carriers:
            if carrier in inline:
                hexes = _hexes_in(self.resolve(inline[carrier]))
                if hexes:
                    return carrier, hexes[0]
        for rule in self.rules:
            decls = rule["decls"]
            if not any(c in decls for c in carriers):
                continue
            if id(node) not in self.matched(_base_selector(rule["selector"])):
                continue
            for carrier in carriers:
                if carrier in decls:
                    hexes = _hexes_in(self.resolve(decls[carrier]))
                    if hexes:
                        return carrier, hexes[0]
        return None, None

    def in_board_context(self, node: Node) -> bool:
        attr = self.params["board_context_attr"]
        value = self.params["board_context_value"]
        classes = self.params["board_context_classes"]
        cur: Node | None = node
        while cur is not None and cur.tag != "[document]":
            if cur.attrs.get(attr) == value:
                return True
            have = set(cur.attrs.get("class", "").split())
            if any(c in have for c in classes):
                return True
            cur = cur.parent
        return False


def _check_result(check_id: str, item: int, name: str,
                  offenders: list[str], observed: dict[str, Any],
                  ) -> dict[str, Any]:
    return {"id": check_id, "section10_item": item, "name": name,
            "status": "FAIL" if offenders else "PASS",
            "offenders": offenders, "observed": observed}


def check_walk(ctx: DesignContext) -> dict[str, Any]:
    """§10.8 -- ordered sets follow the walk BY POSITION: no color twice in
    a row, every step the NEXT walk color (wrapping per the twin)."""
    p = ctx.params
    seq_carriers = p["sequence_carriers"]
    mem_carriers = p["member_carriers"]
    board_only = set(p["board_mapping_only_hexes"])
    offenders: list[str] = []
    groups = 0

    def step_ok(a: str, b: str) -> bool:
        ia, ib = ctx.walk_index[a], ctx.walk_index[b]
        if p["walk"]["wraps"]:
            return (ib - ia) % len(ctx.walk) == 1
        return ib == ia + 1

    def expected_next(a: str) -> str:
        i = ctx.walk_index[a]
        j = (i + 1) % len(ctx.walk) if p["walk"]["wraps"] else i + 1
        return ctx.walk[j] if j < len(ctx.walk) else "(end of walk)"

    marker = p["chip_class_marker"]
    for parent in ctx.doc.root.walk():
        if parent.tag in ("script", "style", "title"):
            continue
        kids = parent.children
        if len(kids) < 2:
            continue
        for carriers, strict in ((seq_carriers, True), (mem_carriers, False)):
            seq: list[tuple[Node, str, str]] = []
            for kid in kids:
                # Contents chips are governed by DL-CHIPS (distinctness is
                # their law); they are not sequenced here.
                if any(marker in cls
                       for cls in kid.attrs.get("class", "").split()):
                    continue
                carrier, hexv = ctx.carrier_value(kid, carriers)
                if carrier is None:
                    continue
                if hexv in board_only and ctx.in_board_context(kid):
                    continue
                seq.append((kid, carrier, hexv))
            if len(seq) < 2:
                continue
            groups += 1
            label = "section" if strict else "member"
            for kid, carrier, hexv in seq:
                if hexv not in ctx.walk_set:
                    offenders.append(
                        f"{node_evidence(kid)}: {label} carrier {carrier} = "
                        f"{hexv} is not a spectrum-walk color (non-walk hues "
                        "live only in SmartNote board sections)")
            runs: list[tuple[Node, str]] = []
            for kid, _carrier, hexv in seq:
                if hexv not in ctx.walk_set:
                    continue
                if strict and runs and runs[-1][1] == hexv:
                    offenders.append(
                        f"{node_evidence(kid)}: section color {hexv} repeats "
                        "the previous section -- the walk never wears the "
                        "same color twice in a row")
                if not runs or runs[-1][1] != hexv:
                    runs.append((kid, hexv))
            for (ka, ha), (kb, hb) in zip(runs, runs[1:]):
                if not step_ok(ha, hb):
                    offenders.append(
                        f"{node_evidence(kb)}: walk breaks {ha} -> {hb}; "
                        f"the next color after {ha} is {expected_next(ha)}")
    return _check_result("DL-WALK", 8, "Spectrum walk sequence",
                         offenders, {"groups_checked": groups})


_RIM_PROPS = ("border", "border-color", "border-top", "border-right",
              "border-bottom", "border-left", "border-top-color",
              "border-right-color", "border-bottom-color",
              "border-left-color", "box-shadow", "outline", "outline-color")
_IGNITION_PROPS = _RIM_PROPS + ("color", "background", "background-color",
                                "transform", "filter")


def _is_neutral_light(hexv: str) -> bool:
    """White-family test for rest rims: white light reads as a near-neutral,
    light value (the factory recipe's silver-white included). A saturated
    color fails by channel spread; a dark neutral fails by lightness. The
    spectrum test runs first -- this only separates 'white light' from
    'some other color worn at rest'."""
    r, g, b = (int(hexv[i:i + 2], 16) for i in (1, 3, 5))
    return max(r, g, b) - min(r, g, b) <= 24 and min(r, g, b) >= 192


def _interactiveish(ctx: DesignContext, base: str,
                    ignition_bases: set[str]) -> bool:
    if base in ignition_bases:
        return True
    last = split_descendant_parts(base)[-1] if base.strip() else ""
    try:
        simple = SimpleSelector(last)
    except Exception:
        return False
    if simple.tag in ctx.params["interactive_tags"]:
        return True
    frags = ctx.params["interactive_class_fragments"]
    return any(any(f in cls for f in frags) for cls in simple.classes)


def check_rest(ctx: DesignContext) -> dict[str, Any]:
    """§10.10/11 + the twin's lighting states: chrome sits WHITE at rest and
    ignites in its own color only on hover/focus. A spectrum color (or any
    saturated color) worn in a rest-state rim is a fail."""
    p = ctx.params
    offenders: list[str] = []
    ignition_bases = {_base_selector(r["selector"]) for r in ctx.rules
                      if _has_state(r["selector"])}
    examined = 0
    for rule in ctx.rules:
        sel = rule["selector"]
        if _has_state(sel):
            continue
        base = _base_selector(sel)
        if any(x in base for x in p["rest_exceptions"]):
            continue
        if not _interactiveish(ctx, base, ignition_bases):
            continue
        rim = {k: v for k, v in rule["decls"].items() if k in _RIM_PROPS}
        if not rim:
            continue
        examined += 1
        for prop, value in rim.items():
            for hexv in _hexes_in(ctx.resolve(value)):
                if hexv in ctx.walk_set:
                    offenders.append(
                        f"{sel}: {prop} wears spectrum color {hexv} at "
                        "rest -- elements sit white at rest and ignite on "
                        "hover/focus")
                elif prop != "box-shadow" and not _is_neutral_light(hexv):
                    offenders.append(
                        f"{sel}: {prop} rest rim is {hexv}, not white "
                        "light (idle state = white border/glow)")
    return _check_result("DL-REST", 10, "Rest-state rims (white at rest)",
                         offenders, {"rest_rules_examined": examined})


def _font_size_px(value: str) -> tuple[float | None, str | None]:
    """(px, None) when a font-size value is statically determinable, else
    (None, unit) for relative units a source check cannot resolve."""
    m = re.search(r"(\d+(?:\.\d+)?)(px|rem|em|pt|%)", value)
    if not m:
        return None, None
    num, unit = float(m.group(1)), m.group(2)
    if unit == "px":
        return num, None
    if unit == "rem":
        return num * 16, None
    if unit == "pt":
        return num * 4 / 3, None
    return None, unit


def check_type(ctx: DesignContext) -> dict[str, Any]:
    """§10.17 + twin typography.body_px.floor: no text below the floor."""
    floor = ctx.params["type_floor_px"]
    offenders: list[str] = []
    skipped: list[str] = []

    def judge(where: str, value: str):
        px, rel = _font_size_px(value)
        if px is not None:
            if px < floor:
                offenders.append(
                    f"{where}: font-size {value.strip()} = {px:g}px is "
                    f"below the twin's type floor ({floor:g}px)")
        elif rel:
            skipped.append(f"{where}: {value.strip()} (relative unit)")

    for rule in ctx.rules:
        for prop in ("font-size", "font"):
            if prop in rule["decls"]:
                judge(rule["selector"], rule["decls"][prop])
    for node in ctx.doc.root.walk():
        inline = ctx.inline_decls(node)
        for prop in ("font-size", "font"):
            if prop in inline:
                judge(f"inline {node_evidence(node)}", inline[prop])
    return _check_result(
        "DL-TYPE", 17, "Type floor", offenders,
        {"floor_px": floor, "relative_units_not_determinable": skipped[:10],
         "relative_units_count": len(skipped)})


def check_dead(ctx: DesignContext) -> dict[str, Any]:
    """Reports-eye steer + §10.22's checkable slice: an interactive element
    with NO hover/focus ignition rule anywhere is a dead board -- it cannot
    light up, so it reads dead. Disabled controls are intentionally inert
    and are excluded by name, here, not silently."""
    offenders: list[str] = []
    ignition: list[tuple[str, dict[str, str]]] = []
    for rule in ctx.rules:
        if _has_state(rule["selector"]):
            if any(k in rule["decls"] for k in _IGNITION_PROPS):
                ignition.append((_base_selector(rule["selector"]),
                                 rule["decls"]))
    tags = set(ctx.params["interactive_tags"])
    sigs: dict[str, dict[str, Any]] = {}
    for node in ctx.doc.root.walk():
        if node.tag in ("[document]", "script", "style"):
            continue
        interactive = (
            node.tag in tags and node.tag != "a"
            or (node.tag == "a" and "href" in node.attrs)
            or node.attrs.get("role") == "button"
            or "onclick" in node.attrs)
        if not interactive:
            continue
        if node.tag == "input" and node.attrs.get("type") == "hidden":
            continue
        if "disabled" in node.attrs:
            continue
        classes = sorted(node.attrs.get("class", "").split())
        sig = node.tag + ("." + ".".join(classes) if classes else "")
        entry = sigs.setdefault(sig, {"count": 0, "nodes": [],
                                      "evidence": node_evidence(node)})
        entry["count"] += 1
        entry["nodes"].append(node)
    dead = 0
    for sig, entry in sorted(sigs.items()):
        nodes = entry["nodes"]
        alive = False
        for base, _decls in ignition:
            matched = ctx.matched(base)
            if any(id(n) in matched for n in nodes):
                alive = True
                break
        if not alive:
            # Inline handlers that restyle on hover/focus count as ignition.
            if any(("onmouseover" in n.attrs or "onfocus" in n.attrs)
                   for n in nodes):
                alive = True
        if not alive:
            dead += 1
            offenders.append(
                f"{sig} x{entry['count']} (e.g. {entry['evidence']}): no "
                ":hover/:focus ignition rule sets border, glow, color, "
                "background, outline, transform or filter -- the element "
                "cannot light up")
    return _check_result("DL-DEAD", 22, "Dead boards (no ignition)",
                         offenders,
                         {"interactive_signatures": len(sigs),
                          "dead_signatures": dead})


def check_chips(ctx: DesignContext) -> dict[str, Any]:
    """Reports-eye steer: a contents-chip group must carry DISTINCT spectrum
    colors -- a same-color cluster is unreadable. Chips are chip-classed
    elements grouped by their parent."""
    marker = ctx.params["chip_class_marker"]
    offenders: list[str] = []
    groups = 0
    carriers = ctx.params["sequence_carriers"] + ctx.params["member_carriers"]
    for parent in ctx.doc.root.walk():
        chips = [c for c in parent.children
                 if any(marker in cls
                        for cls in c.attrs.get("class", "").split())]
        if len(chips) < 2:
            continue
        groups += 1
        seen: dict[str, list[Node]] = {}
        for chip in chips:
            _carrier, hexv = ctx.carrier_value(chip, carriers)
            if hexv is None:
                for prop in ("border-color", "color"):
                    decls = ctx.inline_decls(chip)
                    if prop in decls:
                        hexes = _hexes_in(ctx.resolve(decls[prop]))
                        if hexes:
                            hexv = hexes[0]
                            break
            if hexv is None:
                offenders.append(
                    f"{node_evidence(chip)}: chip carries no spectrum "
                    "color (contents chips are colored by the walk)")
            elif hexv not in ctx.walk_set:
                offenders.append(
                    f"{node_evidence(chip)}: chip color {hexv} is not a "
                    "spectrum-walk color")
            else:
                seen.setdefault(hexv, []).append(chip)
        for hexv, nodes in seen.items():
            if len(nodes) > 1:
                offenders.append(
                    f"{node_evidence(parent)}: {len(nodes)} contents chips "
                    f"share {hexv} -- a same-color cluster; chips carry "
                    "distinct spectrum colors")
    return _check_result("DL-CHIPS", 8, "Contents chips (distinct colors)",
                         offenders, {"chip_groups_checked": groups})


def evaluate_design_language(document: Document,
                             params: dict[str, Any]) -> dict[str, Any]:
    """Run the mechanically checkable §10 items against a parsed page."""
    ctx = DesignContext(document, params)
    checks = [check_walk(ctx), check_rest(ctx), check_type(ctx),
              check_dead(ctx), check_chips(ctx)]
    failed = [c["id"] for c in checks if c["status"] != "PASS"]
    return {
        "checker": "check_standard_features.py -- design-language annex "
                   "(Factory step 6)",
        "params_source": params["source"],
        "contract_version": params.get("contract_version"),
        "status": "FAIL" if failed else "PASS",
        "failed_checks": failed,
        "checks": checks,
        "not_mechanically_checkable": params["not_mechanically_checkable"],
    }


def render_text(report: dict[str, Any]) -> str:
    lines = []
    target = report["target"]
    lines.append("SMART FACTORY — STANDARD FEATURE CHECK")
    lines.append(f"Target: {target.get('source')}")
    if target.get("status"):
        lines.append(f"HTTP: {target['status']}  Final URL: {target.get('final_url')}")
    if target.get("template"):
        lines.append(
            f"Template: {target['template']}  Registry MD5: {target['observed_md5']} "
            f"(matches: {target['registry_md5_matches']})"
        )
    lines.append(f"Bytes: {report['bytes']}  SHA-256: {report['sha256']}")
    if "score" in report:
        lines.append(f"Score: {report['score']['passed']}/{report['score']['total']}")
    lines.append("")
    for feature in report.get("features", []):
        lines.append(f"{feature['status']}  {feature['code']}  {feature['name']}")
        if feature["status"] == "FAIL":
            failures = list(feature["failed_required_checks"])
            failures.extend(f"any-group:{group}" for group in feature["failed_any_groups"])
            lines.append(f"      Failed: {', '.join(failures)}")
        for check in feature["checks"]:
            marker = "✓" if check["pass"] else "✗"
            lines.append(f"      {marker} {check['id']} — {check['label']}")
            for evidence in check.get("evidence", [])[:2]:
                lines.append(f"          evidence: {evidence}")
    annex = report.get("design_language")
    if annex is not None:
        lines.append("")
        lines.append("DESIGN LANGUAGE — §10 SAME-LANGUAGE CHECK (mechanical "
                     "items, from the machine twin)")
        if annex.get("status") == "UNAVAILABLE":
            lines.append(f"UNAVAILABLE: {annex.get('reason')}")
        else:
            lines.append(f"Annex status: {annex['status']}  "
                         f"(twin: {annex.get('twin_source')})")
            for check in annex["checks"]:
                marker = "✓" if check["status"] == "PASS" else "✗"
                lines.append(f"{marker} {check['id']}  {check['name']} "
                             f"(§10.{check['section10_item']})")
                for offender in check["offenders"][:5]:
                    lines.append(f"      offender: {offender}")
                if len(check["offenders"]) > 5:
                    lines.append(f"      … and {len(check['offenders']) - 5} "
                                 "more (full list in the JSON report)")
        named = annex.get("not_mechanically_checkable") or []
        if named:
            lines.append("Not mechanically checkable (named, never "
                         "skipped): " + ", ".join(
                             f"§10.{e['item']} {e['name']}" for e in named))
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", help="Built app file path or URL")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY,
                        help="templates-registry.json (default: beside this checker)")
    parser.add_argument("--template", help="score the registry base for this template key")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path, help="also write the JSON report here")
    parser.add_argument("--registry-only", action="store_true",
                        help="validate the contracts and exit without scoring an app")
    parser.add_argument("--twin", type=Path,
                        help="machine twin for the design-language checks "
                             "(default: load beside the checker / from "
                             "origin/main / vendored snapshot)")
    parser.add_argument("--design-only", action="store_true",
                        help="run only the §10 design-language checks "
                             "(exit 0 pass, 1 failures, 2 twin/target "
                             "invalid); the target may be a file or URL")
    args = parser.parse_args(argv)

    twin_obj = None
    if args.twin:
        try:
            twin_obj = json.loads(args.twin.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"ERROR: cannot read machine twin {args.twin}: {exc}",
                  file=sys.stderr)
            return 2

    if args.design_only:
        try:
            if not args.target:
                print("ERROR: --design-only needs a target file or URL",
                      file=sys.stderr)
                return 2
            if args.target.startswith(("https://", "http://")):
                body, metadata = fetch_url(args.target)
            else:
                target_path = Path(args.target).expanduser().resolve()
                body = target_path.read_bytes()
                metadata = {"source": str(target_path)}
            twin = twin_obj
            twin_source = f"file {args.twin}" if args.twin else None
            if twin is None:
                twin, twin_source = load_design_twin()
            document = Document(body.decode("utf-8", errors="ignore"))
            annex = evaluate_design_language(document,
                                             design_params(twin))
            annex["twin_source"] = twin_source
            report = {"target": metadata,
                      "sha256": hashlib.sha256(body).hexdigest(),
                      "bytes": len(body), "design_language": annex}
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        if args.output:
            args.output.write_text(json.dumps(report, indent=2) + "\n",
                                   encoding="utf-8")
        if args.format == "json":
            print(json.dumps(report, indent=2))
        else:
            print(render_text(report), end="")
        return 0 if annex["status"] == "PASS" else 1

    try:
        registry = json.loads(args.registry.read_text(encoding="utf-8"))
        errors = validate_contracts(registry)
        if errors:
            print("INVALID STANDARD-FEATURE CONTRACTS:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 2
        if args.registry_only:
            print("Standard-feature contracts valid: 13 features, S1-S13.")
            return 0
        body, metadata = load_target(args.target, args.registry.resolve(), registry, args.template)
        report = evaluate(body, metadata, registry, twin=twin_obj)
    except Exception as exc:  # CLI boundary: report configuration/fetch errors plainly.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report), end="")
    return 0 if report["score"]["passed"] == report["score"]["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
