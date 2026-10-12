# Models, costs, keys and auth

## Who pays for what

| Activity | Runs on | Cost |
|---|---|---|
| Coach sessions (this skill) and grading (ai-coach-grader) | Claude Code on the student's **Claude Max** plan | Max limits |
| Agent SDK exercises (weeks 7–8) | Claude Agent SDK, locally, on the **Max login** | Max limits; keep them small |
| All other exercise code, evals, capstone | Claude API with a **Claude Console API key** (pay as you go) | Real money: **$20/month budget**, enforced by a spend limit the student sets in the Console |
| Embeddings and reranking (weeks 5–6+) | Voyage AI API key, or a free local model | Voyage free allowance, then paid; local is free |

## Model policy for exercise code

- Default to the **cheapest current Claude model (Haiku)**. As of 2026-10-09 that is `claude-haiku-5-5` at $0.10 / $0.50 per million input/output tokens for prompts up to 100K tokens ($0.50 / $2.50 above that). **Re-verify the ID and prices** on the models overview (`https://platform.claude.com/docs/en/about-claude/models/overview`) and pricing page (`https://platform.claude.com/docs/en/about-claude/pricing`) whenever a week's lessons involve the API, and update this line if anything changed.
- Use Sonnet or Opus only when a task needs it, and say why in the README. Examples: an LLM judge where Haiku's agreement with human labels is measurably poor; a complex multi-step agent where Haiku fails the eval set; one capstone design-review call. Default to measuring first: run the eval on Haiku, then justify the upgrade with numbers.
- Model behavior to check against current docs before teaching it (it changes): whether thinking is on by default and how `effort` affects token spend, which sampling parameters are accepted, whether assistant prefill is allowed, `tool_choice` restrictions, structured-output syntax. The `claude-api` skill, if available, has current details.
- Teach the student to read `response.usage` on every call: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` (and any thinking/server-tool fields the current API reports).

## Estimating cost (put the arithmetic in every task README)

```
cost ≈ calls × (avg_input_tokens × input_price + avg_output_tokens × output_price) / 1,000,000
```

Add cache writes and reads at the multipliers on the pricing page (verify them; historically writes cost more than base input and reads cost a small fraction of it). Thinking tokens bill as output. Multiply by 2 as a safety margin and round up to the cent. Example: 20 eval cases × 2 calls × (1,500 in × $0.10 + 300 out × $0.50) / 1M = $0.012, so with the margin the README says "≈ $0.03".

## Budget tracking

- **Local estimate:** the student's cost meter (built in w03-t1) appends one JSON object per API call to `.usage/usage.jsonl` (gitignored) at the repo root:
  `{"ts": "2026-10-28T19:02:11Z", "model": "claude-haiku-5-5", "input_tokens": 812, "output_tokens": 164, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cost_usd": 0.000163, "source": "tasks/w03-t2-cli-chat"}`
  `python3 tools/spend.py` totals it by month and model.
- **Authoritative figure:** the Claude Console usage page. Ask for month-to-date spend once a week and record it in `api_spend.by_month[YYYY-MM].console_reported_usd`.
- Thresholds per calendar month: at 50% ($10), mention it at session start. At 80% ($16), run no live tests or evals without explicit approval, and prefer offline fakes. At 100%, the Console limit stops calls; switch to offline work and tell the student.

## API keys (never hard-code)

- Keys live only in `~/ai-engineer-course/.env` (gitignored, never committed; a pre-commit hook in `.githooks/` blocks key-like strings). `.env.example` lists the variable names with empty values.
- Load them per process: `uv run --env-file .env ...` from the repo root (or `--env-file ../../.env` from a task dir), python-dotenv, or pydantic-settings in services. **Never** export keys in `~/.zshrc` or `~/.zprofile`.
- Coach and grader never read `.env` (the project settings deny `Read(./.env)`, and the grader's guard blocks it).
- Suggest the student create a dedicated Console workspace (e.g. `ai-course`) with its own key and a $20 monthly spend limit, so course spend is isolated and capped.
- Setup checklist before week 3: Console account → workspace → API key → spend limit → copy `.env.example` to `.env` → paste key → `uv run --env-file .env` a hello-world example.

## Agent SDK exercises (weeks 7–8): Max login, not the API key

- The Claude Agent SDK runs the Claude Code runtime. If `ANTHROPIC_API_KEY` is present in its environment it bills that key; with it unset, it uses the logged-in Claude Code account (the Max plan).
- So SDK exercises run as `env -u ANTHROPIC_API_KEY uv run <script>` or `env -u ANTHROPIC_API_KEY uv run pytest --agent-sdk`, never with `--env-file .env`. SDK code must not call `load_dotenv()`. Start each SDK script with a guard:
  ```python
  if os.environ.get("ANTHROPIC_API_KEY"):
      sys.exit("Unset ANTHROPIC_API_KEY so this runs on your Max login, not the Console key.")
  ```
- Keep runs small, because they draw on the same Max limits the study sessions need: the smallest model that works (Haiku), `max_turns` ≤ 8, tiny prompts and file sets, and a handful of runs per session. Prefer offline tests with the SDK's transport mocked for logic, and real runs only to demonstrate.
- Anthropic's Agent SDK docs say third-party products may not offer claude.ai login. Personal local learning on your own Max login is fine, but anything deployed or shared (capstone demo, portfolio service others run) must use API-key auth within budget. Teach this as part of `w08-hand-vs-sdk`.
- Other ways the key can leak into the environment: VS Code's Python extension can inject `.env` into integrated terminals, and a shell that exported the key makes Claude Code itself offer to use it. If the env guard at session start shows the key is set, tell the student to find where it's exported, remove it, and restart the terminal and Claude Code.

## Embeddings: Anthropic has no embedding model

- **Voyage AI** (Anthropic's recommended embeddings provider): strong retrieval quality, managed, domain-specific models (code, finance, law), rerankers, a free token allowance before paid pricing (verify current models, prices and free tier on Voyage's docs when week 5 starts). Costs: needs `VOYAGE_API_KEY`, data leaves the machine, network latency, rate limits on the free tier.
- **Local open-weight models** (sentence-transformers or fastembed with a small model such as a bge-small or MiniLM variant): free, private, offline, deterministic for tests. Costs: lower quality on hard retrieval, CPU-bound, roughly 100–500 MB of downloads. The 24 GB Mac has room for larger models and batches than the smallest ones, so let the retrieval eval decide the size.
- Teaching approach: build with a local model first (free, good for tests), then compare against Voyage on the student's own retrieval eval (recall@k, MRR) and choose from the numbers. That comparison is itself a lesson in evals and trade-off thinking.

## Prompt caching and other savings (week 10, used from week 4)

Cache stable prefixes (system prompt, tool definitions, big documents) and confirm with `cache_read_input_tokens > 0` on repeated calls. Check the minimum cacheable prefix length for the model on the docs; short prompts silently don't cache. Other levers: Message Batches for offline evals (about half price; verify), lower `effort`, smaller `max_tokens`, trimming context, and routing easy requests to Haiku.
