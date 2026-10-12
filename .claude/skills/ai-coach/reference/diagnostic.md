# Diagnostic (first session, about 25–30 minutes)

Purpose: calibrate the syllabus, not to judge. Tell the student that up front. It's short and they should guess rather than look things up. Record raw answers and scores in `private/progress.json → diagnostic.results`.

Run the parts in order. Use AskUserQuestion for self-ratings and multiple choice when available (up to 4 questions per call, no "(Recommended)" labels); otherwise use plain text. Grade nothing aloud until the end of each part.

## Part A: Background (3 min)

Confirm or adjust, in one message:
1. Java versions and frameworks used most (Spring Boot? reactive? Kafka?), and years of experience.
2. Any Python so far (none / scripts / real project)?
3. Docker, Kubernetes, cloud (AWS/GCP/Azure), CI (GitHub Actions/Jenkins): never / some / daily.
4. Ever called an LLM API or built anything with one?

## Part B: Python transfer (8 min). Predict the output; guessing is fine

Ask all six at once and score 1 per correct answer (0.5 for right reasoning with a slip).

```python
# B1
def add(x, items=[]):
    items.append(x)
    return items
add(1); print(add(2))
```
Answer: `[1, 2]` (the default list is created once).

```python
# B2
a = [1, 2, 3]
b = a
b.append(4)
print(a, a is b)
```
Answer: `[1, 2, 3, 4] True`

```python
# B3
print(7 // 2, -7 // 2, 7 / 2)
```
Answer: `3 -4 3.5`

```python
# B4
print(bool([]), bool("0"), bool(0.0), bool(None))
```
Answer: `False True False False`

```python
# B5
d = {"b": 2, "a": 1}
print([k for k in d], {v: k for k, v in d.items()})
```
Answer: `['b', 'a'] {2: 'b', 1: 'a'}` (insertion order is kept)

```python
# B6
nums = (n * n for n in range(4))
print(sum(nums), sum(nums))
```
Answer: `14 0` (a generator is exhausted after one pass)

**B7 (translate, 3 min):** write Python for

```java
Map<String, Long> counts = words.stream()
    .filter(w -> w.length() > 3)
    .collect(Collectors.groupingBy(String::toLowerCase, Collectors.counting()));
```
Good answer: `Counter(w.lower() for w in words if len(w) > 3)`. Accept a dict comprehension or loop for partial credit (0.5).

## Part C: Tooling self-rating (2 min)

Rate 0–3 (0 = never, 1 = a little, 2 = comfortable, 3 = expert): terminal/zsh, Git, Docker, CI pipelines, async/concurrent programming, HTTP API frameworks, SQL, writing tests.

## Part D: LLM and ML concepts (8 min). Two sentences each, guessing is fine

Score 0, 0.5 or 1 each.
1. What is a token, and why do API prices use tokens rather than words?
2. What does a context window limit?
3. What does raising temperature do?
4. What is an embedding, and what is it used for?
5. What does cosine similarity measure?
6. What is RAG, and what problem does it solve?
7. Does the Claude API remember earlier requests? How does a chat app keep a conversation going?
8. Precision vs recall: which matters more for a retrieval step that feeds an LLM, and why?

## Part E: Goals and logistics (3 min)

1. Target role and domain (industry, company type, location or remote).
2. Capstone interests (show the options from curriculum.md, or their own idea).
3. Learning preference: more reading or more building? Prefer short quizzes or longer ones?
4. Known days off in the next 13 weeks (Thanksgiving 2026-11-26, the December holidays, travel). Record them as `course.schedule_overrides` with 0 hours or reduced hours.
5. Can they install Docker Desktop (or colima) on this Mac? Have they created the Claude Console API key yet (needed before week 3)?

## Scoring and adjustments

| Signal | Adjustment |
|---|---|
| Python transfer ≥ 6/7 and some real Python | Compress weeks 1–2 by about 30%; move the time to RAG, evals and the capstone |
| Python transfer ≤ 3/7 | Keep weeks 1–2 as planned; add more predict-the-output drills to recap quizzes |
| Concepts ≥ 6/8 | Halve `w03-llm-fundamentals`; keep `w03-ml-just-enough` (evals depend on it) |
| Concepts ≤ 3/8 | Keep week 3 as planned; add a concept card to each week-1/2 recap quiz |
| Docker ≤ 1 | 1 h Docker primer in week 5 before pgvector |
| CI ≤ 1 | 30 min GitHub Actions primer in week 9 (evals in CI) |
| Async ≤ 1 | Extra 30 min on asyncio in week 2 |
| Days off declared | Add schedule overrides; build them into the syllabus from the start |

Then give the student a five-line summary: strengths, gaps, and what changes in the syllabus. Write `diagnostic.completed = true`, `diagnostic.date`, `results` (per-part scores and raw notes) and `adjustments` (list of strings), and seed `weak_areas` with any part D question scored 0 that the course depends on. Write the summary, background and the reason for each adjustment to `private/diagnostic.md`; the public syllabus lists the adjustments with "Diagnostic" as the reason, never the scores.
