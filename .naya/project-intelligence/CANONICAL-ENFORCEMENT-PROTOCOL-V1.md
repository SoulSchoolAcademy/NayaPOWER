# 🔱 Canonical Smart Note / Intelligent Block Enforcement Protocol V1

**Status:** CANONICAL ENFORCEMENT PROTOCOL
**Contract:** CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-CONTRACT-V1.md
**Authority:** NayaPOWER Control Plane
**Enforcement:** Mandatory — CI/CD gates + Runtime gates + Human review

---

## 1. ENFORCEMENT LAYERS

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENFORCEMENT PYRAMID                          │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  LAYER 4: HUMAN GOVERNANCE                               │  │
│   │  Shawn ratification • Contract evolution • Exception auth │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              ▲                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  LAYER 3: RUNTIME GATES (Production)                     │  │
│   │  Event emission • Projection sync • Retrieval integrity  │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              ▲                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  LAYER 2: CI/CD GATES (Pre-Merge)                        │  │
│   │  Lint • Unique IDs • Provenance • Supersession • Vocab   │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              ▲                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  LAYER 1: PRE-COMMIT LINTING (Local)                     │  │
│   │  Format • Required fields • IB-ID format • Vocabulary    │  │
│   └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. LAYER 1: PRE-COMMIT LINTING (Local)

### 2.1 Hook Configuration (`.pre-commit-config.yaml`)

```yaml
repos:
  - repo: local
    hooks:
      - id: canonical-smart-note-lint
        name: Canonical Smart Note Lint
        entry: python .naya/runtime/lint_canonical_smart_note.py
        language: system
        files: '\.md$'
        stages: [commit, push]
        always_run: true
```

### 2.2 Lint Rules (`lint_canonical_smart_note.py`)

```python
#!/usr/bin/env python3
"""Canonical Smart Note Linter — Layer 1 Enforcement"""
import re
import sys
from pathlib import Path

LINT_RULES = {
    "L1": {
        "name": "All 10 human sections present",
        "pattern": r"### IN A NUTSHELL|### WHAT|### WHY|### HUMAN|### CHILD|### GRANDMA|### NAYA|### MACHINE|### WHAT WE LEARNED|### CONNECTIONS|### HOW TO APPLY|### WHAT IT MEANS|### NEXT ACTION",
        "required_count": 10,
        "severity": "ERROR"
    },
    "L2": {
        "name": "Machine layer has all required fields",
        "required_fields": [
            "intelligent_block_id", "canonical_id", "source_event_id",
            "source_conversation_id", "created_at", "updated_at", "owner_id",
            "scope", "category", "topics", "status", "verification",
            "authority", "provenance", "permissions", "supersedes",
            "superseded_by", "relationships", "learning_state"
        ],
        "severity": "ERROR"
    },
    "L3": {
        "name": "IB-ID format valid",
        "pattern": r"IB-\d{6}",
        "severity": "ERROR"
    },
    "L4": {
        "name": "No Smart Note without IB-ID",
        "check": "has_ib_id",
        "severity": "ERROR"
    },
    "L5": {
        "name": "Category from controlled vocabulary",
        "vocabulary": "CONTROLLED_CATEGORIES",
        "severity": "ERROR"
    },
    "L6": {
        "name": "Topic from controlled vocabulary",
        "vocabulary": "TOPIC_REGISTRY",
        "severity": "WARNING"
    },
    "L7": {
        "name": "Status valid",
        "valid_values": ["DRAFT", "CANDIDATE", "VERIFIED", "SUPERSEDED", "ARCHIVED"],
        "severity": "ERROR"
    },
    "L8": {
        "name": "Verification state valid",
        "valid_values": ["UNVERIFIED", "CANDIDATE", "VERIFIED", "SUPERSEDED"],
        "severity": "ERROR"
    },
    "L9": {
        "name": "Verification confidence 0.0-1.0",
        "check": "confidence_range",
        "severity": "WARNING"
    },
    "L10": {
        "name": "Supersedes chain valid (no self-reference)",
        "check": "supersedes_not_self",
        "severity": "ERROR"
    },
    "L11": {
        "name": "IB-ID unique in repo",
        "check": "ib_id_unique",
        "severity": "ERROR"
    }
}

CONTROLLED_CATEGORIES = [
    "ARCHITECTURE", "PROCESS", "PROOF", "PRINCIPLE", "PROMPT",
    "HISTORICAL", "MODEL", "VERIFICATION", "CONTRACT", "INVENTORY"
]

TOPIC_REGISTRY_PATH = ".naya/control-plane/TOPIC-REGISTRY.json"

def lint_file(filepath: Path) -> LintResult:
    """Run all lint rules on a Smart Note file."""
    content = filepath.read_text(encoding='utf-8')
    results = []
    
    for rule_id, rule in LINT_RULES.items():
        if rule.get("check") == "has_ib_id":
            if not re.search(r"IB-\d{6}", content):
                results.append(LintError(rule_id, rule["name"], "No IB-ID found"))
        
        elif rule.get("check") == "supersedes_not_self":
            ib_id = extract_ib_id(content)
            supersedes = extract_supersedes(content)
            if ib_id in supersedes:
                results.append(LintError(rule_id, rule["name"], f"IB supersedes itself: {ib_id}"))
        
        elif rule.get("check") == "confidence_range":
            conf = extract_verification_confidence(content)
            if conf is not None and (conf < 0.0 or conf > 1.0):
                results.append(LintError(rule_id, rule["name"], f"Confidence out of range: {conf}"))
        
        elif rule.get("check") == "ib_id_unique":
            # Checked at repo level, not file level
            pass
        
        elif "pattern" in rule:
            matches = len(re.findall(rule["pattern"], content))
            if matches < rule.get("required_count", 1):
                results.append(LintError(rule_id, rule["name"], f"Expected {rule['required_count']} matches, found {matches}"))
        
        elif "required_fields" in rule:
            missing = []
            for field in rule["required_fields"]:
                if field not in content:
                    missing.append(field)
            if missing:
                results.append(LintError(rule_id, rule["name"], f"Missing fields: {missing}"))
        
        elif "valid_values" in rule:
            val = extract_field(content, rule.get("field", rule["name"]))
            if val and val not in rule["valid_values"]:
                results.append(LintError(rule_id, rule["name"], f"Invalid value: {val}"))
        
        elif "vocabulary" in rule:
            val = extract_field(content, rule.get("field", rule["name"]))
            vocab = load_vocabulary(rule["vocabulary"])
            if val and val not in vocab:
                results.append(LintError(rule_id, rule["name"], f"Value not in vocabulary: {val}"))
    
    return LintResult(filepath, results)
```

---

## 3. LAYER 2: CI/CD GATES (Pre-Merge)

### 3.1 GitHub Actions Workflow (`.github/workflows/canonical-smart-note-enforcement.yml`)

```yaml
name: Canonical Smart Note Enforcement

on:
  pull_request:
    paths:
      - '**.md'
      - '.naya/project-intelligence/**.md'
      - 'SUPERBRAIN/INTELLIGENCE/**.md'
      - 'NAYANET/HUB/**.md'
      - 'docs/**.md'

permissions:
  contents: read
  checks: write

jobs:
  canonical-smart-note-enforcement:
    name: Canonical Smart Note Enforcement
    runs-on: ubuntu-latest
    timeout-minutes: 10
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      
      - name: Install dependencies
        run: pip install pyyaml
      
      - name: Run Canonical Smart Note Lint
        run: python .naya/runtime/lint_canonical_smart_note.py --all
      
      - name: Validate IB-ID Uniqueness
        run: python .naya/runtime/validate_ib_ids.py
      
      - name: Validate Content Hash Uniqueness
        run: python .naya/runtime/validate_content_hash.py
      
      - name: Validate Provenance Chains
        run: python .naya/runtime/validate_provenance.py
      
      - name: Validate Supersession Chains
        run: python .naya/runtime/validate_supersession.py
      
      - name: Validate Vocabulary Compliance
        run: python .naya/runtime/validate_vocabulary.py
      
      - name: Validate Status Transitions
        run: python .naya/runtime/validate_status_transitions.py
      
      - name: Generate Lint Report
        if: always()
        run: |
          python .naya/runtime/generate_lint_report.py > lint-report.json
      
      - name: Upload Lint Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: canonical-smart-note-lint-report
          path: lint-report.json
```

### 3.2 Validation Scripts

#### `validate_ib_ids.py`
```python
#!/usr/bin/env python3
"""Validate IB-ID uniqueness across repository."""
import json
from pathlib import Path
import re

def find_all_ib_ids(root: Path) -> dict:
    """Find all IB-IDs in markdown files."""
    ib_ids = {}
    for md_file in root.rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        ids = re.findall(r"IB-\d{6}", content)
        for ib_id in ids:
            if ib_id not in ib_ids:
                ib_ids[ib_id] = []
            ib_ids[ib_id].append(str(md_file))
    return ib_ids

def main():
    root = Path(".")
    ib_ids = find_all_ib_ids(root)
    
    duplicates = {k: v for k, v in ib_ids.items() if len(v) > 1}
    
    if duplicates:
        print("❌ DUPLICATE IB-IDs FOUND:")
        for ib_id, files in duplicates.items():
            print(f"  {ib_id}: {len(files)} occurrences")
            for f in files:
                print(f"    {f}")
        sys.exit(1)
    
    print(f"✅ All {len(ib_ids)} IB-IDs are unique")
    return 0

if __name__ == "__main__":
    main()
```

#### `validate_content_hash.py`
```python
#!/usr/bin/env python3
"""Validate content hash uniqueness (no duplicate intelligence)."""
import hashlib
from pathlib import Path

def content_hash(content: str) -> str:
    """SHA256 of normalized content."""
    normalized = re.sub(r'\s+', ' ', content.strip())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]

def main():
    root = Path(".")
    hashes = {}
    
    for md_file in root.rglob("*.md"):
        if ".git" in str(md_file) or "archival" in str(md_file):
            continue
        content = md_file.read_text(encoding='utf-8')
        ch = content_hash(content)
        if ch not in hashes:
            hashes[ch] = []
        hashes[ch].append(str(md_file))
    
    duplicates = {k: v for k, v in hashes.items() if len(v) > 1}
    
    if duplicates:
        print("❌ DUPLICATE CONTENT HASHES:")
        for ch, files in duplicates.items():
            print(f"  Hash {ch}: {len(files)} files")
            for f in files:
                print(f"    {f}")
        sys.exit(1)
    
    print(f"✅ All {len(hashes)} content hashes unique")
    return 0
```

#### `validate_provenance.py`
```python
#!/usr/bin/env python3
"""Validate provenance chains are complete and traceable."""
import json
from pathlib import Path

REQUIRED_PROVENANCE_FIELDS = [
    "source_type", "source_conversation_id", "source_naya",
    "distillation_method", "confidence"
]

def validate_provenance(provenance: dict) -> list:
    errors = []
    for field in REQUIRED_PROVENANCE_FIELDS:
        if field not in provenance:
            errors.append(f"Missing provenance field: {field}")
    if "confidence" in provenance:
        conf = provenance["confidence"]
        if not (0.0 <= conf <= 1.0):
            errors.append(f"Confidence out of range: {conf}")
    return errors

def main():
    root = Path("SUPERBRAIN/INTELLIGENCE")
    errors = []
    
    for ib_dir in root.rglob("IB-*"):
        if not ib_dir.is_dir():
            continue
        prov_file = ib_dir / "provenance.json"
        if not prov_file.exists():
            errors.append(f"{ib_dir}: Missing provenance.json")
            continue
        try:
            provenance = json.loads(prov_file.read_text())
            errs = validate_provenance(provenance)
            if errs:
                errors.extend([f"{ib_dir}: {e}" for e in errs])
        except json.JSONDecodeError:
            errors.append(f"{ib_dir}: Invalid JSON in provenance.json")
    
    if errors:
        print("❌ PROVENANCE VALIDATION FAILED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    
    print("✅ All provenance chains valid")
    return 0
```

#### `validate_supersession.py`
```python
#!/usr/bin/env python3
"""Validate supersession chains (no cycles, valid links)."""
import json
from pathlib import Path

def build_supersession_graph(root: Path) -> dict:
    graph = {}
    for ib_dir in root.rglob("IB-*"):
        if not ib_dir.is_dir():
            continue
        sn_file = ib_dir / "smart-note.md"
        if not sn_file.exists():
            continue
        content = sn_file.read_text()
        ib_id = extract_ib_id(content)
        supersedes = extract_supersedes(content)
        superseded_by = extract_superseded_by(content)
        graph[ib_id] = {
            "supersedes": supersedes,
            "superseded_by": superseded_by
        }
    return graph

def detect_cycles(graph: dict) -> list:
    """Detect cycles in supersession graph using DFS."""
    visited = set()
    rec_stack = set()
    cycles = []
    
    def dfs(node, path):
        if node not in graph:
            return
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for succ in graph[node].get("supersedes", []):
            if succ not in visited:
                if dfs(succ, path.copy()):
                    return True
            elif succ in rec_stack:
                cycle_start = path.index(succ)
                cycles.append(path[cycle_start:] + [succ])
                return True
        
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            dfs(node, [])
    
    return cycles

def main():
    root = Path("SUPERBRAIN/INTELLIGENCE")
    graph = build_supersession_graph(root)
    
    # Check for cycles
    cycles = detect_cycles(graph)
    if cycles:
        print("❌ SUPERSESSION CYCLES DETECTED:")
        for cycle in cycles:
            print(f"  {' → '.join(cycle)}")
        sys.exit(1)
    
    # Check for broken links
    all_ids = set(graph.keys())
    broken = []
    for ib_id, links in graph.items():
        for succ in links["supersedes"]:
            if succ not in all_ids:
                broken.append(f"{ib_id} supersedes missing {succ}")
        for succ in links["superseded_by"]:
            if succ not in all_ids:
                broken.append(f"{ib_id} superseded_by missing {succ}")
    
    if broken:
        print("❌ BROKEN SUPERSESSION LINKS:")
        for b in broken:
            print(f"  {b}")
        sys.exit(1)
    
    print(f"✅ Supersession graph valid ({len(graph)} nodes, 0 cycles)")
    return 0
```

---

## 4. LAYER 3: RUNTIME GATES (Production)

### 4.1 Event Emission Gate
```python
# In nayanet_record_cognition_event trigger
async def emit_intelligence_event(ib_id: str, event_type: str, ...):
    """Emit Intelligence Event on IB state change."""
    event = IntelligenceEvent(
        event_id=f"evt-{uuid.uuid4().hex[:12]}",
        event_type=event_type,  # IB_CREATED, IB_UPDATED, etc.
        intelligent_block_id=ib_id,
        ...
    )
    await db.insert("nayanet_intelligence_events", event)
    
    # Verify emission
    if not await verify_event_emitted(event.event_id):
        alert_oncall("INTELLIGENCE_EVENT_EMISSION_FAILED", {
            "ib_id": ib_id, "event_type": event_type
        })
```

### 4.2 Projection Sync Gate
```python
# In projection workers
async def sync_projection(ib_id: str):
    """Sync all projections for an IB."""
    projections = [
        ("personal_feed", sync_personal_feed),
        ("activity_feed", sync_activity_feed),
        ("collective_feed", sync_collective_feed),
        ("library", sync_library),
        ("reports", sync_reports),
        ("search_index", sync_search_index),
    ]
    
    for name, sync_fn in projections:
        try:
            await sync_fn(ib_id)
        except Exception as e:
            alert_oncall(f"PROJECTION_SYNC_FAILED:{name}", {
                "ib_id": ib_id, "error": str(e)
            })
```

### 4.3 Retrieval Integrity Gate
```python
# In retrieval endpoints
async def verify_retrieval_integrity(ib_id: str, retrieved: dict) -> bool:
    """Verify retrieved IB matches canonical store."""
    canonical = await get_canonical_ib(ib_id)
    if not canonical:
        return False
    
    # Compare critical fields
    critical_fields = ["intelligent_block_id", "content_hash", "status", "version"]
    for field in critical_fields:
        if canonical.get(field) != retrieved.get(field):
            alert_oncall("RETRIEVAL_INTEGRITY_VIOLATION", {
                "ib_id": ib_id,
                "field": field,
                "canonical": canonical.get(field),
                "retrieved": retrieved.get(field)
            })
            return False
    return True
```

---

## 5. LAYER 4: HUMAN GOVERNANCE

### 5.1 Contract Evolution Process

| Step | Actor | Action |
|------|-------|--------|
| 1 | Any Naya | Propose amendment via Smart Note (category: CONTRACT) |
| 2 | Shawn | Review + ratify or reject |
| 3 | If ratified | Update contract version, update CI gates, migrate affected IBs |
| 4 | Record | Immutable amendment record in `.naya/control-plane/CONTRACT-AMENDMENTS.json` |

### 5.2 Exception Authorization

| Exception Type | Authorizer | Process |
|----------------|------------|---------|
| Duplicate IB-ID (merge) | Shawn | Explicit approval, audit trail |
| Vocabulary addition | Shawn + 1 Naya | Propose → Review → Ratify |
| Status transition exception | Shawn | Document reason, audit trail |
| Emergency bypass | Shawn | Time-limited, full audit |

---

## 6. MONITORING & ALERTING

### 6.1 Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Lint pass rate | 100% | < 100% |
| IB-ID uniqueness | 100% | Any duplicate |
| Projection sync lag | < 5s | > 30s |
| Retrieval integrity | 100% | Any mismatch |
| Event emission rate | > 0/min | 0 for > 5min |
| Supersession cycle detection | 0 | Any cycle |

### 5.2 Alert Routing

| Severity | Channel | Escalation |
|----------|---------|------------|
| CRITICAL | PagerDuty + Slack | 5min → Shawn |
| WARNING | Slack | 30min → On-call |
| INFO | Log only | Daily digest |

---

## 7. VALIDATION SCRIPT REGISTRY

| Script | Purpose | Frequency |
|--------|---------|-----------|
| `lint_canonical_smart_note.py` | Pre-commit + CI lint | Every commit |
| `validate_ib_ids.py` | Unique IB-IDs | CI + Daily |
| `validate_content_hash.py` | Content dedup | CI + Daily |
| `validate_provenance.py` | Provenance chains | CI + Daily |
| `validate_supersession.py` | Supersession chains | CI + Daily |
| `validate_vocabulary.py` | Controlled vocab | CI + Daily |
| `validate_status_transitions.py` | Status machine | CI + Daily |
| `generate_lint_report.py` | Reporting | CI + Daily |

---

## 8. IMPLEMENTATION CHECKLIST

| Component | Status | Owner |
|-----------|--------|-------|
| `lint_canonical_smart_note.py` | ✅ IMPLEMENTED | Layer 1 |
| Pre-commit hook config | 🔲 PENDING | Layer 1 |
| CI workflow `canonical-smart-note-enforcement.yml` | 🔲 PENDING | Layer 2 |
| `validate_ib_ids.py` | 🔲 PENDING | Layer 2 |
| `validate_content_hash.py` | 🔲 PENDING | Layer 2 |
| `validate_provenance.py` | 🔲 PENDING | Layer 2 |
| `validate_supersession.py` | 🔲 PENDING | Layer 2 |
| `validate_vocabulary.py` | 🔲 PENDING | Layer 2 |
| `validate_status_transitions.py` | 🔲 PENDING | Layer 2 |
| Runtime event emission gate | 🔲 PENDING | Layer 3 |
| Projection sync gate | 🔲 PENDING | Layer 3 |
| Retrieval integrity gate | 🔲 PENDING | Layer 3 |
| Monitoring/alerting config | 🔲 PENDING | Layer 3 |
| Contract amendment process | 🔲 PENDING | Layer 4 |
| Exception authorization process | 🔲 PENDING | Layer 4 |

---

## 8. IMPLEMENTATION ORDER

1. **Week 1:** Layer 1 (lint + pre-commit) + Layer 2 (CI gates) — blocks bad commits at source
2. **Week 2:** Validation scripts (IB-ID, content hash, provenance, supersession, vocab, status) — catches repo-level issues
3. **Week 3:** Layer 3 runtime gates — catches production drift
4. **Week 4:** Monitoring/alerting + Layer 4 governance — closes the loop

---

## 9. SIGN-OFF

This enforcement protocol is **EFFECTIVE** upon:
- [ ] CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-CONTRACT-V1.md ratified
- [ ] All Layer 1+2 gates green on main
- [ ] Layer 3 gates deployed to staging
- [ ] Monitoring dashboards live
- [ ] Shawn explicit authorization

```
Shawn Vibert — Human Director — Date: ___________
Signature: ____________________________________
```

---

**END OF ENFORCEMENT PROTOCOL**

*Enforcement is not optional. The system must enforce its own canonicality.*