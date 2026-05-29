"""Defensive parser: prompts forbid fences, but LLMs occasionally emit them.

Used by free-text fix-generator agents (CodeFixerAgent, InfraSREAgent) to
salvage fenced output without raising. Pure string transforms — no I/O,
no LLM-specific knowledge.
"""

from __future__ import annotations

import re


_FENCE_RE = re.compile(
    r"\A```[A-Za-z0-9_+\-]*\n(.*?)\n?```\Z",
    re.DOTALL,
)


def strip_markdown_fence(text: str) -> str:
    """Strip a single surrounding ```lang?\\n...\\n``` block if present.

    Returns the inner payload (stripped) when fenced; otherwise returns
    ``text.strip()``. Does not unwrap nested fences — only the outermost
    pair is removed.
    """
    stripped = text.strip()
    match = _FENCE_RE.match(stripped)
    if match is not None:
        return match.group(1).strip()
    return stripped
