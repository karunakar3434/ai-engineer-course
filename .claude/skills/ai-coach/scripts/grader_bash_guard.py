#!/usr/bin/env python3
"""PreToolUse hook that keeps the ai-coach-grader subagent's Bash commands read-only.

Claude Code sends the hook input as JSON on stdin. Exit 0 allows the command; exit 2 blocks it
and shows stderr to the grader. Blocked: git commands that change state, deleting, moving or
editing files, writes outside the temp dir, dependency/lockfile changes, and anything that would
reveal .env contents or API keys. Code that pytest runs is not sandboxed; this guards only the
commands the grader itself types. Stdlib only, Python 3.9+.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys

DEVICE_PATHS = ("/dev/null", "/dev/stdout", "/dev/stderr")
TEMP_PREFIXES = ("/tmp/", "/private/tmp/", "/var/folders/", "$TMPDIR", "${TMPDIR}")
SCRATCH_DIR = "ai-coach-grader"
OPERATORS = {"|", "||", "&&", ";", "&", "|&", "(", ")", ";;", "{", "}"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>", ">&"}
ALWAYS_BLOCKED = {"rm", "rmdir", "mv", "shred", "truncate", "unlink", "chmod", "chown", "chgrp", "ln", "dd",
                  "install", "rsync", "patch", "eval", "printenv", "brew", "npm", "pnpm", "yarn", "gh"}
WRITE_TARGET_COMMANDS = {"cp", "touch", "mkdir", "tee"}
GIT_READ_ONLY = {"diff", "status", "log", "show", "rev-parse", "ls-files", "ls-tree", "cat-file", "blame",
                 "grep", "describe", "shortlog", "merge-base", "rev-list", "name-rev", "for-each-ref", "check-ignore"}
GIT_VALUE_OPTS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
UV_VALUE_OPTS = {"--directory", "--project", "--cache-dir", "--config-file", "--python", "-p", "--color", "--with",
                 "--with-editable", "--with-requirements", "--env-file", "--group", "--extra", "--package",
                 "--index", "--default-index", "--index-url", "--extra-index-url", "--only-group", "--no-group",
                 "--exclude-newer", "-w", "--from"}
UV_BLOCKED = {"add", "remove", "init", "pip", "self", "publish", "venv", "build"}
WRAPPERS = {"sudo", "nohup", "time", "command", "exec", "nice", "caffeinate", "xargs", "timeout", "env"}
FIND_EXEC = {"-exec", "-execdir", "-ok", "-okdir"}
SHELLS = {"bash", "sh", "zsh"}
FORMATTERS = {"black", "isort", "autopep8", "autoflake", "pyupgrade", "docformatter"}
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
ENV_FILE_IN_CODE = re.compile(r"(?<![\w-])\.env(?![\w-])(?!\.(?:example|sample|template))")
KEY_EXPANSION = re.compile(r"\$\{?\w*API_KEY")


class Blocked(Exception):
    pass


def is_safe_path(path: str) -> bool:
    """Writes may go to /dev/null and friends, or to a temp dir under .../ai-coach-grader/."""
    if path.startswith(DEVICE_PATHS):
        return True
    return path.startswith(TEMP_PREFIXES) and f"/{SCRATCH_DIR}" in path and ".." not in path


def is_env_file(token: str) -> bool:
    for part in re.split(r"[=:]", token):
        name = os.path.basename(part.strip("'\""))
        if re.fullmatch(r"\.env(\..+)?", name) and not name.endswith((".example", ".sample", ".template")):
            return True
    return False


def strip_heredocs(command: str) -> tuple[str, str]:
    """Return (shell text without heredoc bodies, concatenated heredoc bodies)."""
    shell_lines, bodies, pending = [], [], []
    for line in command.split("\n"):
        if pending:
            if line.strip() == pending[0]:
                pending.pop(0)
            else:
                bodies.append(line)
            continue
        shell_lines.append(line)
        pending.extend(match.group(2) for match in HEREDOC.finditer(line))
    return "\n".join(shell_lines), "\n".join(bodies)


def tokenize(shell_text: str) -> list[str]:
    text = shell_text.replace("`", " ; ").replace("\n", " ; ")
    lexer = shlex.shlex(text, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError as exc:
        raise Blocked(f"could not parse the command's quoting ({exc}); put code in a heredoc instead") from exc


def segments(tokens: list[str]) -> list[list[str]]:
    result, current = [], []
    for token in tokens:
        if token in OPERATORS:
            if current:
                result.append(current)
            current = []
        else:
            current.append(token)
    if current:
        result.append(current)
    return result


def check_redirects(segment: list[str]) -> list[str]:
    """Validate redirect targets and return the segment without redirections."""
    words, skip = [], False
    for i, token in enumerate(segment):
        if skip:
            skip = False
            continue
        if token in REDIRECTS:
            target = segment[i + 1] if i + 1 < len(segment) else ""
            if token == ">&" and (target.isdigit() or target == "-"):
                skip = True
                continue
            if not is_safe_path(target):
                raise Blocked(f"redirecting output to '{target}' writes into the repo; write only under $TMPDIR/ai-coach-grader/")
            skip = True
            continue
        if token in {"<", "<<", "<<-", "<<<"}:
            skip = True
            continue
        words.append(token)
    # Drop file-descriptor numbers left in front of redirects (e.g. the "2" of 2>/dev/null).
    return [w for w in words if not (w.isdigit() and len(w) == 1)]


def check_command(words: list[str]) -> None:
    while words and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[0]):
        words = words[1:]
    if not words:
        return
    cmd, args = os.path.basename(words[0]), words[1:]

    if cmd in ALWAYS_BLOCKED:
        raise Blocked(f"'{cmd}' is not allowed for the read-only grader")
    if cmd in WRITE_TARGET_COMMANDS:
        paths = [a for a in args if not a.startswith("-")]
        targets = paths[-1:] if cmd == "cp" else paths
        unsafe = [p for p in targets if not is_safe_path(p)]
        if unsafe:
            raise Blocked(f"'{cmd}' would write to {unsafe[0]}; write only under $TMPDIR/ai-coach-grader/")
    if cmd in {"sed", "perl", "ruby"} and any(re.match(r"^-[a-zA-Z]*i", a) or a.startswith("--in-place") for a in args):
        raise Blocked(f"in-place editing with '{cmd}' is not allowed")
    if cmd in {"set", "export", "declare", "typeset"} and (not args or args[0] in {"-p", "-x"}):
        raise Blocked("printing the environment could reveal API keys")
    if cmd in {"pip", "pip3"} or (cmd.startswith("python") and args[:3] in (["-m", "pip", "install"], ["-m", "pip", "uninstall"])):
        raise Blocked("installing packages is not allowed; use 'uv run --frozen --with <pkg>' for a throwaway tool")
    if cmd in SHELLS and "-c" in args:
        index = args.index("-c")
        if index + 1 < len(args):
            check_shell(args[index + 1])
        return
    if cmd == "git":
        check_git(args)
        return
    if cmd == "uv":
        check_uv(args)
        return
    if cmd == "uvx":
        tool_args = args
        while tool_args and tool_args[0].startswith("-"):
            tool_args = tool_args[2:] if tool_args[0] in UV_VALUE_OPTS else tool_args[1:]
        check_command(tool_args)
        return
    if "--fix" in args or "--fix-only" in args or any(a.startswith("--fix=") for a in args):
        raise Blocked(f"'{cmd} --fix' rewrites files; run linters without --fix")
    rewrites = (cmd == "ruff" and "format" in args) or cmd in FORMATTERS
    if rewrites and not {"--check", "--diff"} & set(args):
        raise Blocked(f"'{cmd}' would reformat files; add --check (or --diff)")
    if cmd == "find":
        for i, arg in enumerate(args):
            if arg == "-delete" or arg in {"-fprint", "-fprintf", "-fls"}:
                raise Blocked(f"'find {arg}' is not allowed")
            if arg in FIND_EXEC and i + 1 < len(args):
                check_command(args[i + 1:])
        return
    if cmd in WRAPPERS:
        check_command(skip_wrapper_options(cmd, args))


def skip_wrapper_options(cmd: str, args: list[str]) -> list[str]:
    i = 0
    value_opts = {"env": {"-u", "-S", "-C"}, "xargs": {"-n", "-I", "-P", "-L", "-s", "-d", "-E"},
                  "nice": {"-n"}, "sudo": {"-u", "-g"}, "timeout": {"-s", "-k"}}.get(cmd, set())
    while i < len(args) and (args[i].startswith("-") or (cmd == "env" and "=" in args[i])):
        i += 2 if args[i] in value_opts else 1
    if cmd == "timeout" and i < len(args):
        i += 1  # duration
    rest = args[i:]
    if cmd == "env" and not rest:
        raise Blocked("printing the environment could reveal API keys")
    return rest


def check_git(args: list[str]) -> None:
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in GIT_VALUE_OPTS else 1
    sub = args[i] if i < len(args) else ""
    if sub not in GIT_READ_ONLY:
        raise Blocked(f"'git {sub}' can change the repository; the grader may only use: {', '.join(sorted(GIT_READ_ONLY))}")


def check_uv(args: list[str]) -> None:
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in UV_VALUE_OPTS else 1
    sub, rest = (args[i], args[i + 1:]) if i < len(args) else ("", [])
    if sub in UV_BLOCKED:
        raise Blocked(f"'uv {sub}' changes dependencies or environments; report what's missing instead")
    if sub == "tool" and rest[:1] and rest[0] in {"install", "uninstall", "upgrade", "update-shell"}:
        raise Blocked("installing uv tools is not allowed; use uvx for one-off tools")
    if sub == "tool" and rest[:1] == ["run"]:
        check_command(["uvx", *rest[1:]])
    if sub == "lock" and not {"--check", "--dry-run", "--check-exists"} & set(rest):
        raise Blocked("'uv lock' rewrites uv.lock; use 'uv lock --check'")
    if sub == "sync" and not {"--frozen", "--locked", "--check", "--dry-run"} & set(rest):
        raise Blocked("'uv sync' may rewrite uv.lock; add --frozen")
    if sub == "run":
        j = 0
        while j < len(rest) and rest[j].startswith("-"):
            j += 2 if rest[j] in UV_VALUE_OPTS else 1
        options = set(rest[:j])
        if not {"--frozen", "--locked", "--no-project", "--script", "--no-sync"} & options:
            raise Blocked("'uv run' may rewrite uv.lock; use 'uv run --frozen ...'")
        check_command(rest[j:])


def check_shell(shell_text: str) -> None:
    shell_part, bodies = strip_heredocs(shell_text)
    tokens = tokenize(shell_part)
    for i, token in enumerate(tokens):
        if is_env_file(token) and not (token.startswith("--env-file") or (i and tokens[i - 1] == "--env-file")):
            raise Blocked("reading .env is not allowed (it holds API keys)")
        if KEY_EXPANSION.search(token):
            raise Blocked("expanding API key variables is not allowed")
    if ENV_FILE_IN_CODE.search(bodies) or KEY_EXPANSION.search(bodies):
        raise Blocked("scripts must not read .env or API keys")
    for segment in segments(tokens):
        check_command(check_redirects(segment))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    try:
        check_shell(command)
    except Blocked as exc:
        print(f"Blocked by ai-coach-grader guard: {exc}. The grader is read-only.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
