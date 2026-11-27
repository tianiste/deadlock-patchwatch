"""Merge two independent reviews; write disputes for judging, then (with --final) write scoring/reviewed_tags.json."""
import json, glob, os, sys, collections

R = "data/review"
lines = {}
for k in range(1, 9):
    for l in json.load(open(f"{R}/batch_{k}.json", encoding="utf-8")):
        lines[l["id"]] = l
A, B = {}, {}
for k in range(1, 9):
    A.update(json.load(open(f"{R}/result_{k}.json", encoding="utf-8")))
    B.update(json.load(open(f"{R}/blind_result_{k}.json", encoding="utf-8")))
assert set(A) == set(lines) == set(B), (len(A), len(B), len(lines))

agree = {i for i in lines if A[i]["tag"] == B[i]["tag"]}
disputes = [dict(lines[i], review_a=A[i], review_b=B[i]) for i in sorted(set(lines) - agree, key=lambda i: (lines[i]["hero"], lines[i]["date"]))]
print(f"{len(lines)} lines, reviewers agree on {len(agree)} ({len(agree)/len(lines):.1%}), disputes {len(disputes)}")
print("agreed tag differs from auto rule:", sum(1 for i in agree if A[i]["tag"] != lines[i]["auto_tag"]))

if "--final" not in sys.argv:
    n = 4
    for j in range(n):
        part = disputes[j::n]
        json.dump(part, open(f"{R}/disputes_{j+1}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("disputes", j + 1, len(part))
    sys.exit()

J = {}
for f in glob.glob(f"{R}/judged_*.json"):
    J.update(json.load(open(f, encoding="utf-8")))
missing = [d["id"] for d in disputes if d["id"] not in J]
assert not missing, f"{len(missing)} disputes not judged"

# keyed by exact line text; identical text in two patches must agree, else keep the later judgement
# add to the existing file so earlier reviews are kept when only a new patch was reviewed
out, how = {}, collections.Counter()
if os.path.exists("scoring/reviewed_tags.json"):
    out = json.load(open("scoring/reviewed_tags.json", encoding="utf-8"))
for i, l in sorted(lines.items(), key=lambda kv: kv[1]["date"]):
    if i in agree:
        tag, why, src = A[i]["tag"], B[i]["why"], "two reviewers agree"
    else:
        tag, why, src = J[i]["tag"], J[i]["why"], "judged"
    how[src] += 1
    out[l["text"]] = {"tag": tag, "why": why}
os.makedirs("scoring", exist_ok=True)
json.dump(dict(sorted(out.items())), open("scoring/reviewed_tags.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
final = {i: (A[i]["tag"] if i in agree else J[i]["tag"]) for i in lines}
print(dict(how), "written", len(out))
print("final tags", collections.Counter(final.values()))
print("final differs from auto rule:", sum(1 for i in lines if final[i] != lines[i]["auto_tag"]))
