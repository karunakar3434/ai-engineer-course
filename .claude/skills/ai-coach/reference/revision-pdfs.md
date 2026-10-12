# Revision notes and PDFs

## When

- **Per topic**: at the session where the topic's last lesson is taught. Don't wait for its task to pass. If later grading or quizzes expose new pitfalls, update the notes and rebuild at the next week kickoff.
- **Combined course PDF**: rebuilt weekly at the week kickoff (`--all --combined`), and on request.

## How

1. Write `revision/<topic-id>.md` from `templates/revision.md`. Section order is fixed: Summary → Key concepts → Java vs Python → Code snippets → Common pitfalls → Review next → Cheat sheet → Official docs.
2. Build: `python3 tools/build_pdf.py revision/<topic-id>.md` → `pdfs/<topic-id>.pdf`.
3. Read the PDF to check it: tables readable, code not clipped, **cheat sheet on exactly one page**. If it spills over, cut lines; don't shrink fonts.
4. Set `topics[id].revision` and `topics[id].pdf` in private/progress.json.
5. Combined: `python3 tools/build_pdf.py --all --combined` → `pdfs/ai-engineer-course.pdf` (title page, topic-level table of contents, every topic in filename order, so `wNN-` prefixes keep it chronological). Set `pdfs.combined_last_built`.

## Content rules

- Written for revision, not first learning: dense, scannable, no narrative padding.
- **Java vs Python** table: 5–12 rows, real code in both columns, a "Watch out" column for where the analogy breaks. For LLM-only topics, compare with the closest backend concept (a vector index vs a B-tree index, an eval suite vs an integration test suite, prompt caching vs an HTTP cache, an agent loop vs a workflow engine).
- **Code snippets**: short, correct, consistent with the lessons and the student's own code, with the Python version and library versions they were verified against.
- **Common pitfalls**: include the student's own mistakes from grader reports and quizzes, tagged with the source.
- **Review next**: concepts to revisit before the next quiz, drawn from open weak areas. No scores or quiz results: revision notes and PDFs are public (SKILL.md rule 11).
- **Cheat sheet**: two columns inside the raw typst block from the template; about 45–60 short lines in total, grouped under bold labels. It should be useful printed on its own.
- **Official docs**: only primary sources (python.org, docs.pydantic.dev, fastapi.tiangolo.com, platform.claude.com/docs, code.claude.com/docs, modelcontextprotocol.io, docs.voyageai.com, and so on), each with "verified YYYY-MM-DD".
- Pandoc Markdown → typst: no Mermaid or HTML. Use tables or ASCII diagrams. Keep raw typst only in the template's two blocks (page break and cheat-sheet columns).
