```python
#!/usr/bin/env python3
"""
Regenerates the synchronized brain index by:
1. Scanning all SN-* files for valid projections
2. Removing duplicate entries (keeping the canonical one)
3. Writing a clean, synchronized index
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).parent.parent
BRAIN_DIR = REPO_ROOT / "BRAIN"
INDEX_FILE = BRAIN_DIR / "index.json"

def scan_smart_notes():
    """Scan all SN-* files and collect their metadata."""
    notes = []
    sn_pattern = re.compile(r'^SN-(\d+)', re.MULTILINE)
    
    for md_file in REPO_ROOT.rglob("SN-*.md"):
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        match = sn_pattern.search(content)
        if match:
            sn_id = f"SN-{match.group(1)}"
            notes.append({
                "id": sn_id,
                "path": str(md_file.relative_to(REPO_ROOT)),
                "content_preview": content[:200],
                "has_duplicate": False
            })
    
    return notes

def detect_duplicates(notes):
    """Detect duplicate projections for the same SN ID."""
    id_counts = defaultdict(list)
    for note in notes:
        id_counts[note["id"]].append(note)
    
    duplicates = {}
    for sn_id, items in id_counts.items():
        if len(items) > 1:
            # Keep the first one as canonical, mark others as duplicates
            canonical = items[0]
            for item in items[1:]:
                item["has_duplicate"] = True
                item["canonical_path"] = canonical["path"]
            duplicates[sn_id] = items[1:]
    
    return duplicates

def fix_obsolete_paths(content):
    """Replace obsolete .naya/preview/ paths with canonical .naya/ paths."""
    # Pattern to match obsolete .naya/preview/ references
    obsolete_pattern = re.compile(r'\.naya/preview/')
    if obsolete_pattern.search(content):
        return obsolete_pattern.sub('.naya/', content), True
    return content, False

def regenerate_index():
    """Main function to regenerate the synchronized brain index."""
    print("Scanning smart notes...")
    notes = scan_smart_notes()
    
    print("Detecting duplicates...")
    duplicates = detect_duplicates(notes)
    
    # Fix obsolete paths in all notes
    print("Fixing obsolete path references...")
    for note in notes:
        file_path = REPO_ROOT / note["path"]
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            fixed_content, had_fix = fix_obsolete_paths(content)
            if had_fix:
                file_path.write_text(fixed_content, encoding="utf-8")
                print(f"  Fixed obsolete path in: {note['path']}")
    
    # Build clean index
    clean_notes = [n for n in notes if not n["has_duplicate"]]
    
    index = {
        "version": "1.0",
        "generated_at": "2026-10-04T00:00:00Z",
        "total_smart_notes": len(clean_notes),
        "duplicate_projections_removed": sum(len(v) for v in duplicates.values()),
        "smart_notes": clean_notes,
        "duplicates": {k: [{"path": v["path"], "canonical": v["canonical_path"]} for v in items] for k, items in duplicates.items()}
    }
    
    # Ensure BRAIN directory exists
    BRAIN_DIR.mkdir(exist_ok=True)
    
    # Write index
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"Index regenerated: {len(clean_notes)} notes, {sum(len(v) for v in duplicates.values())} duplicates removed")
    print(f"Index written to: {INDEX_FILE}")

if __name__ == "__main__":
    regenerate_index()
