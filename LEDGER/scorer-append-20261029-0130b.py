import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t1023",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "Q15 honest close: mu=1.0 last-sentence boost as pre-registered primary, DECOY-HOLDS verdict",
        "receipt": "t1023-lane10.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: hidden_files/auto-retrieval/semantic-arm-hybrid-t1023.py sha256 19baf6e1cd3656681d254b1131f35068cf74ac57b5ce00e49051023d54915b08 exactly as receipted, and semantic-arm-hybrid-t1023-results.json sha256 3b2001348e6ec202e32d38584662ba9777a97fa5f3d1f0d569f0d496d7f14cc7 exactly as receipted. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below lane self-claimed 9.0 pass-3 ship (held at 9.0, not 9.5). Why not 9.5: (1) the receipted report md sha256 5031b642... no longer matches live bytes (4857290d...), i.e. the report drifted after the receipt pin with no drift note; (2) no adversarial/negative-control pair set for the boost (the lane's own hole); (3) the Oct-17 form remains unrecoverable, so the comparison carries the stated provenance caveat. Gap-recycle: throttled this tick (queue 31 >= 30), no follow-up filed.",
    },
    {
        "tick": "t1011",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "Lexical-penalty hybrid replication for t0553 semantic arm, Q15 DECOY-HOLDS at lambda=0.05",
        "receipt": "t1011-lane10.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: hidden_files/auto-retrieval/semantic-arm-hybrid-t1011.py sha256 6367499ee8db834f5399def3afc4932fb92edaceaf26201a6e68416772539a94 exactly as receipted, and semantic-arm-hybrid-t1011-results.json sha256 f8a84ad14552c93e631aac1920dc40f2902743f55e0181221acc107b0a87b29a exactly as receipted. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below lane self-claimed 9.5 (pass 3). Why not 9.5: (1) determinism was not re-proven live this tick (no re-run executed, only pinned bytes checked); (2) no adversarial/negative-control pair set (the lane's own hole); (3) the run replicated rather than advanced (the lane's own pass-2 note). Gap-recycle: throttled this tick (queue 31 >= 30), no follow-up filed.",
    },
]

with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")

n = 0
for line in open(path):
    if line.strip():
        json.loads(line)
        n += 1
print("appended 2 rows; total parseable rows:", n)
