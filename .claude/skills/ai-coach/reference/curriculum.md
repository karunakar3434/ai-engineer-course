# Default curriculum (adjust after the diagnostic)

This is the starting point for `syllabus.md`. The diagnostic, scores and missed days change it, and every change is logged in the syllabus changelog.

**Priorities.** P1 = core for the job; never cut, may compress. P2 = important; compress first. P3 = nice to have; cut first.
**Hours.** 18 h/week: Sat 3, Sun 3, Mon 3, Tue 2, Wed 2, Thu 2, Fri 3. Course day 1 of each week is Saturday. Per-topic hours include lesson time; task hours are listed separately. Each week plans about 1 h less than available as slack.
**Topic IDs** are `wNN-<slug>` and **task IDs** are `wNN-tK` (folder `tasks/wNN-tK-<slug>/`). Capstone milestones are `c-m1`…`c-m4`.

## syllabus.md shape

```markdown
# AI Engineer Course: Syllabus (v<version>, <date>)
Goal · dates · weekly hours · pass mark · how to read this file
## Adjustments (reason column names the source, never scores; the diagnostic summary goes to private/diagnostic.md)
## Week-by-week
### Week N (<start>–<end>): <title>
Goal: <one sentence: what the student can build by Friday>
| Topic ID | Topic | Priority | Hours |
| Task ID | Task | Hours | Est. API cost |
## Capstone
## Changelog
| Date | Change | Reason |
```

---

## Week 1: Python for Java developers I

Goal: write, test and run idiomatic Python with modern tooling.

| Topic | Contents | P | h |
|---|---|---|---|
| `w01-py-tooling` | uv vs Maven/Gradle (`uv init`, `uv add`, `uv run`, `uv.lock` vs lockfile-less Maven), virtual environments vs the classpath, `pyproject.toml` vs `pom.xml`, Python versions via uv, src layout, VS Code (Python, Pylance, Ruff extensions; selecting the interpreter), ruff for lint and format (vs Checkstyle/Spotless), PEP 8, REPL, PEP 723 inline-script metadata | P1 | 2.5 |
| `w01-py-core` | Names vs variables (references to objects), dynamic but strong typing, `None` vs `null`, truthiness, int/float/`Decimal` vs `BigDecimal`, strings and f-strings, `match` vs `switch`, functions (defaults, `*args`/`**kwargs`, keyword-only), the mutable default trap, closures and scope (LEGB), exceptions (EAFP vs LBYL, no checked exceptions, `raise ... from`), modules, imports, `if __name__ == "__main__"` | P1 | 4.5 |
| `w01-py-collections` | list/tuple/dict/set vs ArrayList/List.of/HashMap/HashSet, comprehensions vs streams, slicing, unpacking, the iterator protocol, generators and `yield` vs lazy Streams, `itertools`, `collections` (Counter, defaultdict, deque), `sorted(key=)` vs Comparator, shallow vs deep copy | P1 | 4 |
| `w01-py-testing` | pytest vs JUnit 5: plain asserts, fixtures vs @BeforeEach, `parametrize` vs @ParameterizedTest, `tmp_path`, `monkeypatch` and `unittest.mock` vs Mockito, test layout, coverage | P1 | 2 |

Tasks: **w01-t1 log-insights** (4 h). CLI that streams a large access log with generators and reports stats (Counter, dataclasses, argparse); provided pytest suite. Weights 50/30/20/0.

## Week 2: Python for Java developers II

Goal: build a typed, tested async service the way you would in Spring Boot.

| Topic | Contents | P | h |
|---|---|---|---|
| `w02-py-oop-typing` | Classes, dunder methods, `@property` vs getters, dataclasses vs records/Lombok, enums, ABCs vs Protocols (structural typing vs interfaces), type hints, generics (PEP 695), TypedDict, Literal, mypy/pyright, context managers vs try-with-resources, decorators vs annotations/AOP | P1 | 3.5 |
| `w02-py-async` | asyncio vs threads, virtual threads and CompletableFuture; async/await, `gather`, `TaskGroup`, timeouts, semaphores for rate limiting, httpx async client, the GIL and when to use threads or processes, why LLM apps are I/O-bound | P1 | 3.5 |
| `w02-pydantic-fastapi` | Pydantic v2 vs Jackson + Bean Validation, pydantic-settings and `.env`; FastAPI vs Spring Boot: routing, `Depends` vs DI container, request/response models, async endpoints, error handling, OpenAPI, TestClient/httpx tests, lifespan; layout of a production service | P1 | 4.5 |

Tasks: **w02-t1 async-fetcher** (3 h). Concurrent fetcher with a concurrency limit, retries with backoff and timeouts, tested with a fake transport. Weights 50/30/20/0. **w02-t2 bookmarks-api** (3 h). FastAPI service with Pydantic models, settings and DI, plus tests. Weights 45/25/30/0.

## Week 3: How LLMs work and the Claude API

Goal: call Claude from Python reliably and know what every token costs.

| Topic | Contents | P | h |
|---|---|---|---|
| `w03-llm-fundamentals` | Tokens and tokenization, context windows, next-token prediction, transformer and attention intuition, pretraining → instruction tuning → RLHF/Constitutional AI, sampling (temperature, top-p; check which params current models accept), why hallucinations happen, extended/adaptive thinking and effort | P1 | 3.5 |
| `w03-ml-just-enough` | Vectors, dot product, cosine similarity, normalization; softmax and probabilities; loss and gradient descent intuition; train/val/test splits, overfitting, leakage; precision, recall, F1 and confusion matrices; numpy basics vs Java arrays | P1 | 2.5 |
| `w03-claude-api` | anthropic SDK: client, Messages API, system prompt, stateless multi-turn, `max_tokens`, `stop_reason`, streaming, typed errors and retries, rate limits, async client, `usage` fields and cost math, token counting, Models API, choosing Haiku/Sonnet/Opus, keys via `.env`, Console spend limits | P1 | 5 |

Tasks: **w03-t1 cost-meter** (3 h). Wraps the client and logs every call's usage and cost to `.usage/usage.jsonl` in the format from models-and-costs.md; reused by every later task. **w03-t2 cli-chat** (3 h). Streaming CLI chat with history, token-budget trimming and a `/cost` command. Weights 40/20/20/20.

## Week 4: Prompt engineering, structured outputs, tool use

Goal: get reliable, validated, tool-using behavior from a model, and measure it.

| Topic | Contents | P | h |
|---|---|---|---|
| `w04-prompting` | Clear instructions, system prompts and roles, XML-tag structure, few-shot examples, thinking/effort vs explicit reasoning, prompt templates and versioning, long-context tips, a tiny eval loop for prompt changes | P1 | 4 |
| `w04-structured-outputs` | JSON via structured outputs and Pydantic parsing, strict tool schemas, validation and repair/retry, refusals and `stop_reason` handling | P1 | 3.5 |
| `w04-tool-use` | Tool definitions (JSON Schema), the tool_use → tool_result loop, parallel tool calls, `is_error`, `tool_choice` limits on current models, SDK tool runner vs manual loop, tool security | P1 | 4 |

Tasks: **w04-t1 extractor** (3.5 h). Job posting → Pydantic schema extraction over a labeled set of 20 examples, with a field-level accuracy target (live eval, a few cents). Weights 35/15/20/30. **w04-t2 sql-assistant** (2 h). Tool-calling assistant over SQLite with a read-only SQL guard. Weights 40/20/20/20.

## Week 5: Embeddings, vector databases, RAG I

Goal: build a working RAG pipeline with citations.

| Topic | Contents | P | h |
|---|---|---|---|
| `w05-embeddings` | What embeddings are; Voyage AI vs local open-weight models (sentence-transformers or fastembed; the 24 GB Mac has room for more than the smallest models); dimensions, normalization, similarity metrics; query vs document input types; batching and caching; cost, latency and privacy trade-offs | P1 | 3.5 |
| `w05-vector-dbs` | ANN intuition (HNSW, IVF), pgvector in Postgres vs Chroma/Qdrant/LanceDB, metadata filtering, running Postgres + pgvector in Docker (install Docker Desktop or colima here) | P1 | 3.5 |
| `w05-rag-basics` | Load → chunk → embed → index → retrieve → generate with citations; chunking (fixed, recursive, Markdown-aware, semantic), size and overlap trade-offs, grounded-answer prompts, "I don't know" behavior | P1 | 4 |

Tasks: **w05-t1 semantic-search** (3 h). Index a docs corpus (e.g. FastAPI docs) in pgvector; search CLI. **w05-t2 rag-qa** (3 h). RAG Q&A with citations and abstention. Weights 40/20/20/20.

## Week 6: RAG II, retrieval quality and RAG evals

Goal: measurably improve retrieval and prove it with numbers.

| Topic | Contents | P | h |
|---|---|---|---|
| `w06-retrieval-quality` | Hybrid search (BM25 + vectors, reciprocal rank fusion), reranking (Voyage rerank vs local cross-encoder), query rewriting, contextual retrieval, parent-document retrieval, metadata filters | P1 | 4.5 |
| `w06-rag-evals` | Golden question sets, recall@k, MRR, nDCG, faithfulness and answer relevance with an LLM judge (preview of week 9), ablations | P1 | 3.5 |
| `w06-rag-service` | FastAPI RAG endpoint, ingestion job, incremental re-indexing, embedding cache | P2 | 2 |

Tasks: **w06-t1 better-retrieval** (4 h). Hybrid + rerank with an eval harness showing improvement over the w05 baseline. Weights 35/15/20/30. **w06-t2 rag-api** (3 h). The RAG pipeline as a FastAPI service. Weights 40/20/25/15.

## Week 7: Agents by hand and MCP

Goal: understand the agent loop by building it yourself, then expose tools over MCP.

| Topic | Contents | P | h |
|---|---|---|---|
| `w07-agent-patterns` | Workflows vs agents; prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer; when not to build an agent | P1 | 3 |
| `w07-agent-loop` | The loop on the Messages API: tool registry, dispatch, stop conditions, max turns, error recovery, context growth and trimming, per-step tracing, cost per run, human approval gates | P1 | 4.5 |
| `w07-mcp` | MCP concepts (hosts, clients, servers; tools, resources, prompts; stdio vs streamable HTTP), building a server with the Python MCP SDK, connecting it to Claude Code and to your agent, MCP security (tool poisoning, least privilege) | P1 | 3.5 |

Tasks: **w07-t1 hand-agent** (4 h). Agent with 3–4 tools (your RAG search, read-only SQL, calculator, fetch) plus tracing, a turn cap and a cost cap. Weights 35/20/20/25. **w07-t2 mcp-server** (2 h). MCP server exposing your RAG index. Weights 40/20/25/15.

## Week 8: Claude Agent SDK and multi-step workflows

Goal: rebuild the agent on the Agent SDK and argue the trade-offs like a senior engineer.

| Topic | Contents | P | h |
|---|---|---|---|
| `w08-agent-sdk` | Claude Agent SDK (Python): `query()` vs client sessions, options (tools, permission mode, system prompt, max turns, model), custom tools via in-process MCP, hooks, subagents, sessions. Runs on the Max login with `ANTHROPIC_API_KEY` unset; keep runs small | P1 | 4.5 |
| `w08-hand-vs-sdk` | Compare hand-rolled and SDK agents: code size, control, observability, failure handling, cost and limits, and deployment (the SDK needs the Claude Code runtime and API-key auth for anything shipped). Write an ADR | P1 | 2.5 |
| `w08-workflows` | Multi-step workflows: state machines, checkpoints, idempotent retries, human-in-the-loop, long-running jobs, memory | P2 | 3 |

Tasks: **w08-t1 sdk-rebuild** (4 h). The w07 agent on the Agent SDK, plus a comparison ADR. Weights 30/20/25/25. **w08-t2 triage-workflow** (3 h). Ticket triage → draft → evaluator-optimizer review, with an approval gate. Weights 35/20/20/25.

## Week 9: Evals, observability, guardrails, prompt-injection defense

Goal: know whether your LLM app works, see what it does, and stop it being hijacked.

| Topic | Contents | P | h |
|---|---|---|---|
| `w09-evals` | Eval-driven development; golden, synthetic and production-sampled datasets; code-based graders, LLM-as-judge (rubrics, pairwise, calibration against human labels), bootstrap confidence intervals, regression evals in CI, eval cost | P1 | 5 |
| `w09-observability` | Structured logs, tracing (OpenTelemetry; Langfuse or similar), token/cost/latency metrics, tagging prompt versions | P1 | 2.5 |
| `w09-guardrails` | Input/output validation, PII redaction, refusal handling; prompt injection (direct and indirect via documents and tool output); defenses: least-privilege tools, separating instructions from data, allow-lists, output checks, approval gates; OWASP Top 10 for LLM applications | P1 | 3.5 |

Tasks: **w09-t1 rag-evals-ci** (3 h). Eval suite for your RAG app with an LLM judge calibrated on 20 hand labels, run from pytest with thresholds. Weights 30/15/20/35. **w09-t2 red-team** (3 h). 15+ injection cases against your agent; harden it and report attack success rate before and after. Weights 30/15/20/35.

## Week 10: Production

Goal: ship a containerized, streaming, cost-controlled LLM service, and know when to self-host.

| Topic | Contents | P | h |
|---|---|---|---|
| `w10-docker-deploy` | Dockerfile for uv + FastAPI (multi-stage, slim, non-root), compose with Postgres/pgvector, config and secrets via env, health checks; optional deploy to a low-cost host | P1 | 3.5 |
| `w10-streaming-latency` | End-to-end SSE streaming (Claude stream → FastAPI StreamingResponse → client), time to first token, timeouts, retries/backoff, fallbacks, concurrency | P1 | 2.5 |
| `w10-cost-optimization` | Prompt caching (breakpoints, minimum sizes, TTL, measuring hit rate), Message Batches, model routing, effort, `max_tokens`, context trimming, per-request budgets | P1 | 3 |
| `w10-open-source-models` | One lesson: why and when teams self-host (privacy, data residency, cost at scale, latency, control), Ollama/llama.cpp locally vs vLLM in production, quality gap and ops cost, fine-tuning vs RAG vs prompting, LoRA intuition; local-model demo sized for 24 GB RAM | P2 | 2 |

Tasks: **w10-t1 ship-it** (4 h). Productionize the RAG service: Docker + compose + streaming + prompt caching, with measured cache hit rate and cost per request. Weights 35/20/20/25. **w10-t2 local-vs-haiku** (1 h, P3). Run a small local model on your eval set and compare quality, latency and cost with Haiku.

## Weeks 11–12: Capstone (about 34 h)

Choose in the last session of week 10. Options:
- **Codebase copilot for Spring Boot services**: RAG over a Java repo's code and docs, agent tools (search, read file, run tests), MCP server, evals. Uses the student's Java background, which interviewers like.
- **Support knowledge assistant**: RAG over a public docs corpus plus a ticket-triage agent, with human approval.
- **The student's own idea**, if it covers the required components.

Required components: FastAPI service; hybrid retrieval with reranking; at least one agentic workflow with tools (if it uses the Agent SDK, the deployed version must use API-key auth); structured outputs; an eval suite with thresholds that runs in CI (GitHub Actions); observability (traces plus cost and latency metrics); guardrails and injection tests; Docker compose; streaming; prompt caching; a README with an architecture diagram, ADRs and a cost analysis; a demo.

| Milestone | When | Deliverable | Weights |
|---|---|---|---|
| `c-m1` | Week 11, day 2 | Design doc, ADRs, skeleton service, eval set v0 | 20/20/40/20 |
| `c-m2` | End of week 11 | Core RAG and agent working; evals running | 35/20/20/25 |
| `c-m3` | Week 12, day 4 | Production hardening: Docker, streaming, caching, guardrails, observability, CI | 30/20/25/25 |
| `c-m4` | End of week 12 | Final polish, README, demo, cost report | 30/20/25/25 |

Capstone API budget: plan for at most about $10 of the month's $20, with Haiku by default and evals sized to match.

## Week 13: Buffer, portfolio, interview prep

The buffer goes first: re-plans absorb missed time here. Keep at least 8 h of interview prep (P1 for job-readiness) and 4 h of portfolio polish.
- **Portfolio**: root README (course overview, skills matrix, links to the best projects), per-project READMEs, architecture diagrams, a demo GIF or video, a capstone write-up or blog post, resume bullets with metrics.
- **Interview prep**: LLM system design (RAG over 10M documents; a customer-support agent; an eval pipeline; cutting cost on a high-volume app), Python coding drills and idioms, ML/LLM concept questions, your Java-to-AI career story (STAR), and 2–3 mock interviews where the coach interviews and the grader scores the written design.

## Rules for adjusting

- Diagnostic shows strong Python: compress weeks 1–2 to about 1.3 weeks and give the time to weeks 5–10.
- Diagnostic shows strong LLM concepts: halve `w03-llm-fundamentals`.
- No Docker experience: add a 1 h Docker primer to week 5.
- A P1 task failed twice: add a remedial 30–45 min block next session and re-plan if needed.
- Keep the order of dependencies: Python → API → prompting/tools → RAG → agents → evals → production → capstone.
