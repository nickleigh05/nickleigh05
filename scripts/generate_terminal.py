#!/usr/bin/env python3
"""Generates assets/terminal.svg — an animated terminal boot sequence
built from this account's live repo data. Run by .github/workflows/terminal.yml.
"""
import json
import os
import urllib.request

USER = "nickleigh05"
REPOS = ["cloud-collar", "MMA-Machine", "NNFS", "nicksnexus"]
TOKEN = os.environ.get("GITHUB_TOKEN")

FONT = "SFMono-Regular, Menlo, Consolas, monospace"
BG = "#0d1117"
FG = "#39d353"
DIM = "#8b949e"
FRAME = "#30363d"
LINE_H = 22
CHAR_W = 8.4
PAD_X = 18
PAD_TOP = 42


def gh_get(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def latest_commit_subject(repo):
    try:
        commits = gh_get(f"/repos/{USER}/{repo}/commits?per_page=1")
        msg = commits[0]["commit"]["message"].splitlines()[0]
        return msg[:52]
    except Exception:
        return "(no recent activity)"


def build_lines():
    lines = [("prompt", "whoami")]
    lines.append(("out", "nick — ASU CS · cloud + AI/ML"))
    lines.append(("prompt", "tail -f activity.log"))
    for repo in REPOS:
        subject = latest_commit_subject(repo)
        tag = f"[{repo}]".ljust(16)
        lines.append(("log", f"{tag}{subject}"))
    lines.append(("prompt", "uptime"))
    lines.append(("out", "building since 2023 —"))
    return lines


def esc(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render(lines):
    width = 640
    height = PAD_TOP + LINE_H * len(lines) + 24
    rows = []
    t = 0.0
    per_char = 0.028
    for kind, text in lines:
        n_chars = len(text) + (2 if kind == "prompt" else 0)
        dur = max(0.3, n_chars * per_char)
        y = PAD_TOP + len(rows) * LINE_H
        prefix = "$ " if kind == "prompt" else ""
        color = FG if kind == "prompt" else (DIM if kind == "log" else "#c9d1d9")
        full = esc(prefix + text)
        clip_id = f"clip{len(rows)}"
        rows.append(f"""
    <clipPath id="{clip_id}">
      <rect x="0" y="0" height="{LINE_H}" width="0">
        <animate attributeName="width" from="0" to="{len(full) * CHAR_W:.1f}"
          begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="linear"/>
      </rect>
    </clipPath>
    <text x="{PAD_X}" y="{y + 15}" font-family="{FONT}" font-size="13.5"
      fill="{color}" clip-path="url(#{clip_id})">{full}</text>""")
        t += dur + 0.12

    cursor_y = PAD_TOP + (len(rows) - 1) * LINE_H
    cursor_x = PAD_X + len(lines[-1][1]) * CHAR_W + 4

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" rx="10" fill="{BG}" stroke="{FRAME}"/>
  <circle cx="24" cy="20" r="6" fill="#ff5f56"/>
  <circle cx="44" cy="20" r="6" fill="#ffbd2e"/>
  <circle cx="64" cy="20" r="6" fill="#27c93f"/>
  <text x="{width/2}" y="24" font-family="{FONT}" font-size="12" fill="{DIM}" text-anchor="middle">nick@github</text>
  <defs>{''.join(rows)}
  </defs>
  <rect x="{cursor_x:.1f}" y="{cursor_y+2}" width="8" height="14" fill="{FG}">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/>
  </rect>
</svg>"""
    return svg


if __name__ == "__main__":
    lines = build_lines()
    svg = render(lines)
    os.makedirs("assets", exist_ok=True)
    with open("assets/terminal.svg", "w") as f:
        f.write(svg)
    print("wrote assets/terminal.svg")
