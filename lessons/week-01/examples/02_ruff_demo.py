"""A deliberately messy module: Java habits and Python traps that ruff catches.

Don't copy this style. Copy it into a project and let ruff tell you what's wrong:
    cp <this file> ~/ai-engineer-course/playground/hello-uv/src/hello_uv/messy.py
    cd ~/ai-engineer-course/playground/hello-uv && uv run ruff check
"""
import os, sys
import json
from typing import List, Optional
import re


def parseStatusCodes(lines: List[str], seen=[]) -> Optional[List[int]]:
    """Collect the HTTP status code from each access-log line."""
    codes = []
    tmp = 0
    for i in range(len(lines)):
        line = lines[i]
        try:
            code = int(line.split(" ")[8])
        except:
            continue
        if code != None:
            codes.append(code)
    if len(codes) == 0:
        return None
    return codes


class logSummary:
    def __init__(self, codes):
        self.codes = codes
    def errorCount(self):
        count = 0
        for c in self.codes:
            if (c >= 500) == True:
                count = count + 1
        return count


if __name__ == "__main__":
    sample = ['127.0.0.1 - - [14/Oct/2026:03:00:00 -0400] "GET /health HTTP/1.1" 200 2', '127.0.0.1 - - [14/Oct/2026:03:00:01 -0400] "GET /api HTTP/1.1" 503 19']
    codes = parseStatusCodes(sample)
    print(f"codes:", codes, "errors:", logSummary(codes).errorCount())
