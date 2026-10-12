// Shared look for revision PDFs (included by tools/build_pdf.py).
#set par(justify: false, leading: 0.6em)
#show raw: set text(font: ("Menlo", "DejaVu Sans Mono"))
#show raw.where(block: true): it => block(
  fill: luma(246), inset: 7pt, radius: 3pt, width: 100%, breakable: true,
  text(size: 8pt, it),
)
#show raw.where(block: false): it => box(
  fill: luma(238), inset: (x: 2pt), outset: (y: 2pt), radius: 2pt, text(size: 0.9em, it),
)
#show link: set text(fill: rgb("#1a5fb4"))
#show heading.where(level: 1): set text(size: 17pt)
#show heading.where(level: 2): set text(size: 13pt)
#show heading: set block(above: 1.3em, below: 0.7em)
#set table(inset: 5pt, stroke: 0.5pt + luma(185))
#show table: set text(size: 8.5pt)
#show table: set align(left)
#show figure.where(kind: table): set block(breakable: true)
