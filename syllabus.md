# AI Engineer Course: Syllabus (v2, 2026-10-11)

**Goal:** job-ready applied AI Engineer at a product company building AI products: ship production LLM apps (Claude API, RAG, agents, MCP, evals, deployment).
**Dates:** Sat 2026-10-10 → Fri 2027-01-15, 14 weeks · **Hours:** Sat/Sun/Mon/Fri 3 h, Tue/Wed/Thu 2 h (18 h/week) · **Pass mark:** 70/100

How to read this: each week has a goal, topics (P1 = core; P2 = important; P3 = nice to have) and tasks with hours and estimated API cost. Hours include lesson time, and each week plans about 1 h less than available as slack. **Your rule: topics are never compressed.** When time runs short, the plan extends the course instead (see the changelog). Each week's detailed plan is written at its first session in `lessons/week-NN/README.md`, adapted to your latest scores.

## Adjustments

Changes to the default curriculum after the first-session diagnostic.

| Adjustment | Reason |
|:--|:--|
| Course extended from 13 to 14 weeks; the extra week is a third Python week (practical Python, data access, a Python mini-capstone) | Diagnostic, a missed day, and the student's choice to extend rather than compress |
| Every recap quiz in weeks 1–3 includes predict-the-output drills | Diagnostic |
| Each week 1–3 recap quiz has one LLM/ML concept card | Diagnostic |
| `w01-py-testing` +1 h (3 h), and every task asks for some of your own tests | Diagnostic |
| `w02-py-async` +0.5 h | Diagnostic |
| 1 h Docker primer (with Docker Desktop or colima install) at the start of week 6 | Diagnostic |
| 30 min GitHub Actions primer in week 10 | Diagnostic |
| Recap quizzes use 5 questions, and a 10-question weekly review quiz runs in the last session of each week | Student preference |

## Week-by-week

### Week 1 (2026-10-10 – 10-16): Python for Java developers I
Goal: write and run idiomatic Python with uv, and build a streaming log-analysis CLI. 14 h (15 h left after the missed Saturday, 1 h of it used by the diagnostic).

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w01-py-tooling` | uv vs Maven/Gradle, pyproject.toml, venvs vs classpath, src layout, ruff, VS Code, REPL, PEP 723, running pytest | P1 | 2.5 |
| `w01-py-core` | Names vs variables, typing model, None/truthiness, numbers, strings, `match`, functions and args, mutable defaults, scope, exceptions, modules | P1 | 4.5 |
| `w01-py-collections` | list/tuple/dict/set, comprehensions vs streams, slicing, unpacking, iterators and generators, itertools, Counter/defaultdict/deque, sorting, copying | P1 | 4 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w01-t1` | log-insights: streaming access-log stats CLI (generators, Counter, dataclasses, argparse). Weights 50/30/20/0 | 4 (moved to week 2, from day 1) | $0 |

Re-planned 10-14: `w01-py-collections` (all three parts) and the last 20 min of `w01-py-core` move to the start of week 2, before `w01-t1`.

### Week 2 (10-17 – 10-23): Python for Java developers II
Goal: write tested, typed, concurrent Python.

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w01-py-testing` | pytest vs JUnit 5: asserts, fixtures, parametrize, tmp_path, monkeypatch, `unittest.mock` vs Mockito, coverage (moved from week 1, expanded) | P1 | 3 |
| `w02-py-oop-typing` | Classes, dunders, properties, dataclasses vs records, enums, Protocols vs interfaces, type hints and generics, context managers, decorators | P1 | 3.5 |
| `w02-py-async` | asyncio vs threads/CompletableFuture/virtual threads, gather, TaskGroup, timeouts, semaphores, httpx, the GIL | P1 | 4 |
| `w02-py-practical` | Everyday Python for services: pathlib, JSON, logging vs SLF4J/Logback, datetime/zoneinfo, regex, CLIs, mypy | P2 | 2.5 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w01-t1` | scaffold, build and submit (moved from week 1) | 4 | $0 |
| `w02-t1` | async-fetcher: concurrent fetcher with a concurrency limit, retries with backoff and timeouts, tested with a fake transport. Weights 50/30/20/0 | 3 | $0 |

### Week 3 (10-24 – 10-30): Python services: Pydantic, FastAPI, data access
Goal: build a production-shaped Python service the way you would in Spring Boot.

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w03-pydantic-fastapi` | Pydantic v2 vs Jackson + Bean Validation, pydantic-settings and `.env`; FastAPI vs Spring Boot: routing, `Depends` vs DI, models, errors, OpenAPI, tests, lifespan, layout | P1 | 4.5 |
| `w03-py-data-access` | sqlite3 and SQLAlchemy 2.0 vs JDBC/JPA, sessions vs persistence context, migrations awareness | P2 | 2.5 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w03-t1` | bookmarks-api: FastAPI service with Pydantic models, settings, DI, SQLite persistence and tests. Weights 45/25/30/0 | 3.5 | $0 |
| `w03-t2` | feed-digest (Python mini-capstone): async ingestion of several JSON feeds, validation, dedupe, storage, a FastAPI read endpoint, tests, ruff and mypy clean. Weights 40/25/35/0 | 5 | $0 |

Setup before week 4: you create a Claude Console account, a workspace, an API key and a $20 spend limit, then put the key in `.env` (walkthrough in week 3's last session).

### Week 4 (10-31 – 11-06): How LLMs work and the Claude API
Goal: call Claude from Python reliably and know what every token costs.

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w04-llm-fundamentals` | Tokens, context windows, next-token prediction, attention intuition, training stages, sampling, hallucinations, thinking/effort | P1 | 3.5 |
| `w04-ml-just-enough` | Vectors, dot product, cosine similarity, softmax, loss and gradient descent intuition, splits and leakage, precision/recall/F1, numpy basics | P1 | 2.5 |
| `w04-claude-api` | anthropic SDK, Messages API, system prompts, stateless multi-turn, streaming, errors and retries, rate limits, async client, usage and cost math, token counting, model choice | P1 | 5 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w04-t1` | cost-meter: client wrapper logging usage and cost to `.usage/usage.jsonl`; reused by every later task. Weights 40/20/20/20 | 3 | ≈ $0.01 |
| `w04-t2` | cli-chat: streaming CLI chat with history, token-budget trimming and `/cost`. Weights 40/20/20/20 | 3 | ≈ $0.05 |

### Week 5 (11-07 – 11-13): Prompt engineering, structured outputs, tool use
Goal: get reliable, validated, tool-using behavior from a model, and measure it.

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w05-prompting` | Instructions, system prompts, XML structure, few-shot, thinking vs explicit reasoning, templates and versioning, a tiny eval loop | P1 | 4 |
| `w05-structured-outputs` | Structured outputs, Pydantic parsing, strict tool schemas, validation and repair, refusals | P1 | 3.5 |
| `w05-tool-use` | Tool definitions, the tool_use → tool_result loop, parallel calls, `is_error`, tool runner vs manual loop, tool security | P1 | 4 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w05-t1` | extractor: job posting → Pydantic schema over 20 labeled examples, field-level accuracy target. Weights 35/15/20/30 | 3.5 | ≈ $0.10 |
| `w05-t2` | sql-assistant: tool-calling assistant over SQLite with a read-only SQL guard. Weights 40/20/20/20 | 2 | ≈ $0.05 |

### Week 6 (11-14 – 11-20): Docker primer, embeddings, vector databases, RAG I
Goal: build a working RAG pipeline with citations on Postgres + pgvector in Docker.

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w06-docker-primer` | Docker for a Spring Boot developer: images, containers, volumes, ports, compose; install Docker Desktop or colima | P1 | 1 |
| `w06-embeddings` | Embeddings, Voyage AI vs local models (24 GB RAM), dimensions, normalization, query vs document, batching and caching | P1 | 3.5 |
| `w06-vector-dbs` | ANN intuition (HNSW, IVF), pgvector vs Chroma/Qdrant/LanceDB, metadata filtering | P1 | 3.5 |
| `w06-rag-basics` | Load → chunk → embed → index → retrieve → generate with citations; chunking strategies; abstention | P1 | 4 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w06-t1` | semantic-search: index a docs corpus in pgvector, search CLI. Weights 40/20/20/20 | 3 | $0 (local) to ≈ $0.02 (Voyage) |
| `w06-t2` | rag-qa: RAG Q&A with citations and abstention. Weights 40/20/20/20 | 3 | ≈ $0.10 |

### Week 7 (11-21 – 11-27): RAG II, retrieval quality and RAG evals
Goal: measurably improve retrieval and prove it with numbers. (Thanksgiving is Thu 11-26. Tell me if it's a day off.)

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w07-retrieval-quality` | Hybrid search (BM25 + vectors, RRF), reranking, query rewriting, contextual retrieval, parent-document retrieval | P1 | 4.5 |
| `w07-rag-evals` | Golden sets, recall@k, MRR, nDCG, faithfulness and relevance with an LLM judge, ablations | P1 | 3.5 |
| `w07-rag-service` | FastAPI RAG endpoint, ingestion job, incremental re-indexing, embedding cache | P2 | 2 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w07-t1` | better-retrieval: hybrid + rerank with an eval harness beating the week 6 baseline. Weights 35/15/20/30 | 4 | ≈ $0.20 |
| `w07-t2` | rag-api: the RAG pipeline as a FastAPI service. Weights 40/20/25/15 | 3 | ≈ $0.05 |

### Week 8 (11-28 – 12-04): Agents by hand and MCP
Goal: understand the agent loop by building it yourself, then expose tools over MCP.

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w08-agent-patterns` | Workflows vs agents; chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer | P1 | 3 |
| `w08-agent-loop` | Tool registry, dispatch, stop conditions, turn caps, error recovery, context growth, tracing, cost per run, approval gates | P1 | 4.5 |
| `w08-mcp` | MCP hosts/clients/servers, tools/resources/prompts, stdio vs HTTP, Python MCP SDK, MCP security | P1 | 3.5 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w08-t1` | hand-agent: 3–4 tools, tracing, turn cap and cost cap. Weights 35/20/20/25 | 4 | ≈ $0.20 |
| `w08-t2` | mcp-server: MCP server exposing your RAG index. Weights 40/20/25/15 | 2 | ≈ $0.02 |

### Week 9 (12-05 – 12-11): Claude Agent SDK and multi-step workflows
Goal: rebuild the agent on the Agent SDK and argue the trade-offs like a senior engineer.

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w09-agent-sdk` | `query()` vs client sessions, options, custom tools via in-process MCP, hooks, subagents (Max login, `ANTHROPIC_API_KEY` unset) | P1 | 4.5 |
| `w09-hand-vs-sdk` | Hand-rolled vs SDK: control, observability, failure handling, cost, deployment and auth; write an ADR | P1 | 2.5 |
| `w09-workflows` | State machines, checkpoints, idempotent retries, human-in-the-loop, memory | P2 | 3 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w09-t1` | sdk-rebuild: the week 8 agent on the Agent SDK, plus a comparison ADR. Weights 30/20/25/25 | 4 | Max plan |
| `w09-t2` | triage-workflow: triage → draft → evaluator-optimizer review with an approval gate. Weights 35/20/20/25 | 3 | ≈ $0.15 |

### Week 10 (12-12 – 12-18): Evals, observability, guardrails, prompt-injection defense
Goal: know whether your LLM app works, see what it does, and stop it being hijacked.

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w10-evals` | Eval-driven development, datasets, code graders, LLM-as-judge and calibration, confidence intervals, regression evals in CI, plus a 30 min GitHub Actions primer | P1 | 5.5 |
| `w10-observability` | Structured logs, tracing (OpenTelemetry, Langfuse), token/cost/latency metrics, prompt versions | P1 | 2.5 |
| `w10-guardrails` | Validation, PII redaction, direct and indirect prompt injection, defenses, OWASP Top 10 for LLM apps | P1 | 3.5 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w10-t1` | rag-evals-ci: eval suite with an LLM judge calibrated on 20 hand labels, run from pytest with thresholds. Weights 30/15/20/35 | 3 | ≈ $0.30 |
| `w10-t2` | red-team: 15+ injection cases against your agent, harden it, report attack success before and after. Weights 30/15/20/35 | 3 | ≈ $0.20 |

### Week 11 (12-19 – 12-25): Production
Goal: ship a containerized, streaming, cost-controlled LLM service, and know when to self-host. Choose the capstone in the last session. (Christmas is Fri 12-25. Tell me if it's a day off.)

| Topic ID | Topic | Priority | Hours |
|:--|:--|:--|:--|
| `w11-docker-deploy` | Multi-stage Dockerfile for uv + FastAPI, compose with pgvector, config and secrets, health checks | P1 | 3.5 |
| `w11-streaming-latency` | End-to-end SSE streaming, time to first token, timeouts, retries, fallbacks, concurrency | P1 | 2.5 |
| `w11-cost-optimization` | Prompt caching and hit rate, Message Batches, model routing, effort, context trimming, budgets | P1 | 3 |
| `w11-open-source-models` | When and why teams self-host; Ollama vs vLLM; fine-tuning vs RAG vs prompting; LoRA intuition; small local demo | P2 | 2 |

| Task ID | Task | Hours | Est. API cost |
|:--|:--|:--|:--|
| `w11-t1` | ship-it: Docker + compose + streaming + prompt caching, with measured cache hit rate and cost per request. Weights 35/20/20/25 | 4 | ≈ $0.30 |
| `w11-t2` | local-vs-haiku: small local model vs Haiku on your eval set (quality, latency, cost). Weights 40/20/20/20 | 1 | ≈ $0.05 |

### Weeks 12–13 (12-26 – 2027-01-08): Capstone (34 h)
See [Capstone](#capstone). New Year's Day (Fri 01-01) falls in week 12. Declare any days off early so the plan can take them into account.

### Week 14 (2027-01-09 – 01-15): Portfolio and interview prep
Interview prep 8 h (LLM system design, Python drills, concept questions, career story, 2–3 mock interviews), portfolio polish 4 h, buffer 1 h.

## Capstone

Decide in week 11's last session: (a) codebase copilot for Spring Boot services, (b) support knowledge assistant, or (c) your own idea.

Required components: FastAPI service; hybrid retrieval with reranking; at least one agentic workflow with tools (if it uses the Agent SDK, the deployed version must use API-key auth); structured outputs; an eval suite with thresholds running in GitHub Actions; observability (traces, cost and latency metrics); guardrails and injection tests; Docker compose; streaming; prompt caching; a README with an architecture diagram, ADRs and a cost analysis; a demo. API budget about $10.

| Milestone | When | Deliverable | Weights |
|:--|:--|:--|:--|
| `c-m1` | Week 12, day 2 | Design doc, ADRs, skeleton service, eval set v0 | 20/20/40/20 |
| `c-m2` | End of week 12 | Core RAG and agent working; evals running | 35/20/20/25 |
| `c-m3` | Week 13, day 4 | Docker, streaming, caching, guardrails, observability, CI | 30/20/25/25 |
| `c-m4` | End of week 13 | Final polish, README, demo, cost report | 30/20/25/25 |

## Changelog

| Date | Change | Reason |
|:--|:--|:--|
| 2026-10-11 | v1 written from the default curriculum and the diagnostic (13 weeks, with compressions to absorb the missed day) | First session |
| 2026-10-11 | v2: course extended to 14 weeks (ends 2027-01-15); all compressions, the task merge and the P3 cut reverted; new week 3 (`w02-py-practical`, `w03-py-data-access`, `w03-t2` feed-digest); later weeks renumbered +1; missed 2026-10-10 absorbed by the extra week | Student: no compression, expansion welcome, about 3 months is fine |
| 2026-10-11 | Machine updated to an M5 Pro with 24 GB RAM (was 8 GB); `w06-embeddings` no longer limited to the smallest local models | Student's Mac was replaced |
| 2026-10-12 | Re-plan: 1.5 h of 10-11's plan shifted forward. `w01-t1` moves fully to week 2 (scaffolded on day 1) with the last 40 min of `w01-py-collections`; final-week buffer 6 h → 4.5 h | 1.5 h of 10-11's plan not reached; no topics compressed |
| 2026-10-14 | Re-plan: 3.5 h shifted forward. `w01-py-collections` and the last 20 min of `w01-py-core` move to the start of week 2, before `w01-t1`; final-week buffer 4.5 h → 1 h. The next shortfall extends the end date | Tue 10-13 missed and 1.5 h of 10-12's plan not reached; no topics compressed |
