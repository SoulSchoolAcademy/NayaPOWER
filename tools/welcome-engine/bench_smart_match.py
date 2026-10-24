#!/usr/bin/env python3
"""Scale benchmark for Smart Match (v1.5 hardening, item 6).

Synthetic populations (seeded, deterministic): citizens drawn from theme
clusters — same-theme pairs are the planted positives. Measures:
  - full pairwise ranking time, naive (rank_matches for every entity),
  - the inverted-index pre-filter (rank_matches_indexed): time + proof it
    returns IDENTICAL rankings to naive on the 1,000 population,
  - at 10,000: naive time extrapolated from the measured per-score cost
    (labeled as extrapolation), indexed measured on a 500-entity sample,
  - IDF evidence at n=200: precision/recall of surfaced pairs against the
    planted same-theme truth, mode OFF vs ON.
Run: python3 bench_smart_match.py"""
import random, time, sys
import smart_match as m

DOMAINS = ["garden", "chess", "music", "code", "food", "fitness", "photo",
           "craft", "finance", "language", "science", "fashion", "pets",
           "travel", "film", "dance", "writing", "yoga", "tech", "art",
           "history", "astronomy", "theatre", "pottery", "cycling",
           "baking", "robotics", "surfing", "poetry", "carpentry",
           "beekeeping", "swimming", "painting", "podcasting", "hiking",
           "coding", "quilting", "brewing", "sailing", "archery"]
SERVICES = [f"{d} help" for d in DOMAINS] + [f"{d} coaching" for d in DOMAINS]
PEOPLE = [f"{d} people" for d in DOMAINS] + ["neighbors", "students", "mentors"]


def theme_pool(theme):
    return {
        "topics": [f"{theme} practice", f"{theme} theory", f"{theme} basics",
                   f"advanced {theme}", f"{theme} circle", f"{theme} lab"],
        "goals": [f"grow the {theme} community", f"master {theme}", f"share {theme} widely"],
        "services": [f"{theme} help", f"{theme} coaching", f"{theme} workshops"],
    }


def make_population(n, seed=20261024):
    rng = random.Random(seed)
    themes = DOMAINS[:40]
    pop, truth = {}, {}
    for i in range(n):
        theme = themes[i % len(themes)]
        pool = theme_pool(theme)
        pick = lambda xs, k: [rng.choice(xs) for _ in range(k)]
        topics = pick(pool["topics"], 3) + pick([f"{d} practice" for d in themes], 1)
        if rng.random() < 0.7:
            topics.append("community collaboration")  # ubiquitous filler (IDF bait)
        vec = {
            "topics": sorted(set(topics)),
            "goals": sorted(set(pick(pool["goals"], 2))),
            "offers": sorted(set(pick(pool["services"], 2) + pick(SERVICES, 1))),
            "needs": sorted(set(pick(SERVICES, 2) + pick(pool["services"], 1))),
            "wants": sorted(set(pick(PEOPLE, 2))),
        }
        name = f"citizen-{i:05d}"
        pop[name] = vec
        truth[name] = theme
    return pop, truth


def full_rank(pop, indexed=False, sample=None):
    index = m.build_index(pop) if indexed else None
    names = list(pop) if sample is None else list(pop)[:sample]
    t0 = time.perf_counter()
    out = {}
    for name in names:
        fn = m.rank_matches_indexed if indexed else m.rank_matches
        kw = {"index": index} if indexed else {}
        out[name] = fn(pop[name], pop, self_name=name, **kw)
    return time.perf_counter() - t0, out


def main():
    print("== n=100 ==")
    pop, _ = make_population(100)
    t, _ = full_rank(pop)
    print(f"naive full pairwise ranking: {t:.2f}s  ({t / (100 * 99) * 1000:.3f} ms/score)")

    print("== n=1,000 ==")
    pop, _ = make_population(1000)
    t_naive, naive_rows = full_rank(pop)
    per_score = t_naive / (1000 * 999)
    print(f"naive full pairwise ranking: {t_naive:.1f}s  ({per_score * 1000:.3f} ms/score)")
    t_idx, idx_rows = full_rank(pop, indexed=True)
    print(f"indexed full pairwise ranking: {t_idx:.2f}s  (speedup {t_naive / t_idx:.1f}x)")
    mismatches = sum(1 for n in pop
                     if [(r['name'], r['score']) for r in naive_rows[n]]
                     != [(r['name'], r['score']) for r in idx_rows[n]])
    print(f"identity proof: {1000 - mismatches}/1000 entities identical, {mismatches} mismatches")

    print("== n=10,000 ==")
    pop, _ = make_population(10000)
    index = m.build_index(pop)
    sig0 = m.signature(pop["citizen-00000"])
    kept = len(set().union(*[index.get(tok, set()) for tok in sig0]))
    print(f"candidate set for citizen-00000: {kept} of 10,000 survive the pre-filter")
    t_idx, _ = full_rank(pop, indexed=True, sample=500)
    print(f"indexed ranking, 500-entity sample: {t_idx:.2f}s -> extrapolated full: {t_idx * 20:.0f}s")
    print(f"naive full at 10,000 (extrapolated from {per_score * 1000:.3f} ms/score): "
          f"{per_score * 10000 * 9999 / 60:.0f} minutes")
    n1s = 1.0 / per_score
    print(f"1s budget: full pairwise ranking crosses 1s at ~{int(n1s ** 0.5)} entities "
          f"(n*(n-1) scores at {per_score * 1000:.3f} ms each)")

    print("== IDF evidence, n=200 (planted truth = same theme) ==")
    pop, truth = make_population(200)
    idf = m.compute_idf(list(pop.values()))
    print(f"down-weighted tokens: {sorted(idf)}")
    names = list(pop)
    for label, kw in (("OFF", {}), ("ON", {"idf": idf})):
        tp = fp = fn_ = 0
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                r = m.score(pop[names[i]], pop[names[j]], **kw)
                same = truth[names[i]] == truth[names[j]]
                if r["surface"] and same: tp += 1
                elif r["surface"] and not same: fp += 1
                elif not r["surface"] and same: fn_ += 1
        prec = tp / (tp + fp) if tp + fp else 0
        rec = tp / (tp + fn_) if tp + fn_ else 0
        print(f"IDF {label}: surfaced TP={tp} FP={fp} FN={fn_}  precision={prec:.2f} recall={rec:.2f}")


if __name__ == "__main__":
    sys.exit(main())
