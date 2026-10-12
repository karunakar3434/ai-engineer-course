---
topic_id: "{{topic-id}}"
week: {{N}}
built: "{{YYYY-MM-DD}}"
---

# {{Topic title}}

*Week {{N}} · `{{topic-id}}` · built {{YYYY-MM-DD}} · docs verified {{YYYY-MM-DD}}*

## Summary

{{3–6 sentences: what this topic is, why an applied AI engineer needs it, what the student can now build or debug.}}

## Key concepts

- **{{Concept}}**: {{one-line definition}}. {{Why it matters in production LLM work.}}
- {{6–12 items}}

## Java vs Python

| Concept | Java | Python | Watch out |
|:--|:--|:--|:--|
| {{e.g. value object}} | `record Point(int x, int y)` | `@dataclass(frozen=True) class Point: x: int; y: int` | {{dataclasses are mutable unless frozen=True}} |

## Code snippets

### {{Snippet name}}

```python
# {{one line on what this shows}}
{{short, runnable-shaped code}}
```

## Common pitfalls

1. **{{Pitfall}}**: {{symptom}} → {{cause}} → {{fix}}.
2. {{Include the student's own mistakes from quizzes and grader reports, tagged e.g. "(w01-t1, attempt 1)".}}

## Review next

- {{Concepts to revisit before the next quiz, from open weak areas. No scores or quiz results: this file is public.}}

```{=typst}
#pagebreak(weak: true)
#[
#set text(size: 8.5pt)
#show: columns.with(2, gutter: 14pt)
```

## Cheat sheet

**{{Group}}**

- `{{syntax}}`: {{meaning}}
- {{Must fit on ONE page: about 45–60 short lines across both columns. Syntax, idioms, commands, Java→Python one-liners, numbers worth remembering (prices, limits) with their date.}}

```{=typst}
]
#pagebreak(weak: true)
```

## Official docs

- [{{Title}}]({{url}}): {{what to use it for}} (verified {{YYYY-MM-DD}})
