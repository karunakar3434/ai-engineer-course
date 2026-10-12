#!/usr/bin/env python3
"""Build revision PDFs from Markdown with pandoc + typst.

    python3 tools/build_pdf.py revision/w01-python-core.md   # one topic -> pdfs/w01-python-core.pdf
    python3 tools/build_pdf.py --all                         # every revision/*.md whose PDF is stale
    python3 tools/build_pdf.py --combined                    # all topics -> pdfs/ai-engineer-course.pdf

Needs `brew install pandoc typst`. Stdlib only (Python 3.9+).
Revision notes may embed raw typst with ```{=typst} blocks (page breaks, two-column cheat sheets).
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVISION_DIR = ROOT / "revision"
PDF_DIR = ROOT / "pdfs"
STYLE_DIR = ROOT / "tools" / "pdf"
COMBINED_NAME = "ai-engineer-course.pdf"
FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
PAGE_BREAK = "\n\n```{=typst}\n#pagebreak(weak: true)\n```\n\n"


def pandoc(inputs: list[Path], output: Path, extra: list[str]) -> None:
    cmd = [
        "pandoc",
        *map(str, inputs),
        "--from=markdown+autolink_bare_uris-implicit_figures",
        "--pdf-engine=typst",
        f"--metadata-file={STYLE_DIR / 'metadata.yaml'}",
        f"--include-in-header={STYLE_DIR / 'style.typ'}",
        f"--resource-path={REVISION_DIR}:{ROOT}",
        "--output",
        str(output),
        *extra,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pandoc failed for {output.name}:\n{result.stderr.strip()}")


def build_one(source: Path) -> Path:
    PDF_DIR.mkdir(exist_ok=True)
    output = PDF_DIR / f"{source.stem}.pdf"
    pandoc([source], output, [])
    return output


def build_combined() -> Path:
    sources = sorted(REVISION_DIR.glob("*.md"))
    if not sources:
        raise RuntimeError("no revision/*.md files yet")
    parts = [
        "---\n"
        "title: AI Engineer Course\n"
        "subtitle: Revision notes\n"
        f"date: {date.today().isoformat()}\n"
        "---\n"
    ]
    for source in sources:
        parts.append(FRONT_MATTER.sub("", source.read_text(), count=1))
    PDF_DIR.mkdir(exist_ok=True)
    output = PDF_DIR / COMBINED_NAME
    with tempfile.TemporaryDirectory() as tmp:
        combined = Path(tmp) / "combined.md"
        combined.write_text(PAGE_BREAK.join(parts))
        pandoc([combined], output, ["--toc", "--toc-depth=1"])
    return output


def stale(source: Path) -> bool:
    output = PDF_DIR / f"{source.stem}.pdf"
    return not output.exists() or output.stat().st_mtime < source.stat().st_mtime


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sources", nargs="*", type=Path, help="revision Markdown files to build")
    parser.add_argument("--all", action="store_true", help="build every stale revision/*.md")
    parser.add_argument("--combined", action="store_true", help=f"build pdfs/{COMBINED_NAME}")
    args = parser.parse_args()

    missing = [tool for tool in ("pandoc", "typst") if shutil.which(tool) is None]
    if missing:
        print(f"build_pdf: missing {', '.join(missing)}; run: brew install {' '.join(missing)}", file=sys.stderr)
        return 1

    targets = list(args.sources)
    if args.all:
        targets += [s for s in sorted(REVISION_DIR.glob("*.md")) if stale(s)]
    if not targets and not args.combined:
        parser.print_help()
        return 1

    try:
        for source in targets:
            print(f"built {build_one(source.resolve()).relative_to(ROOT)}")
        if args.combined:
            print(f"built {build_combined().relative_to(ROOT)}")
    except RuntimeError as exc:
        print(f"build_pdf: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
