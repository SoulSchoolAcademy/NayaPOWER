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


def evaluate(body: bytes, metadata: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
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
    return {
        "checker": "check_standard_features.py",
        "contract_version": registry["standard_feature_contracts"].get("version"),
        "target": metadata,
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "score": {"passed": passed_count, "total": len(feature_results)},
        "features": feature_results,
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
    lines.append(f"Score: {report['score']['passed']}/{report['score']['total']}")
    lines.append("")
    for feature in report["features"]:
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
    args = parser.parse_args(argv)

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
        report = evaluate(body, metadata, registry)
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
