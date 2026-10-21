"""Generate the animated SVGs used by the profile README.

Every image comes in a dark and a light variant; README.md picks one with
<picture> so it follows the viewer's GitHub theme.

    python3 scripts/build_assets.py
"""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 860

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(
        bg="#0b0b0d", panel="#121215", line="#24242a", dot="#1f1f25",
        text="#eeede8", muted="#8d8c94", faint="#55545c",
        gold="#f2b632", llm="#a98bfa", code="#f2b632", human="#4ade80", io="#8d8c94",
    ),
    "light": dict(
        bg="#fbfaf6", panel="#ffffff", line="#e3e0d8", dot="#ebe8df",
        text="#141417", muted="#5d5c64", faint="#a9a7a0",
        gold="#a86b00", llm="#6d3fe0", code="#a86b00", human="#15803d", io="#5d5c64",
    ),
}

MONO_CH = 0.6  # width of one monospace glyph, in em


def svg(height, body, style, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" role="img" aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n<style>{style}</style>\n{body}\n</svg>\n"
    )


def base_style(t):
    return f"""
.mono{{font-family:{MONO}}} .sans{{font-family:{SANS}}}
.text{{fill:{t['text']}}} .muted{{fill:{t['muted']}}} .faint{{fill:{t['faint']}}}
.gold{{fill:{t['gold']}}} .llm{{fill:{t['llm']}}} .code{{fill:{t['code']}}}
.human{{fill:{t['human']}}} .io{{fill:{t['io']}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
"""


def frame(t, h, dots=True):
    grid = ""
    if dots:
        grid = (
            f'<defs><pattern id="d" width="16" height="16" patternUnits="userSpaceOnUse">'
            f'<circle cx="1.5" cy="1.5" r="1" fill="{t["dot"]}"/></pattern>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{t["bg"]}" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="{t["bg"]}" stop-opacity="0"/></linearGradient></defs>'
            f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="14" fill="url(#d)"/>'
            f'<rect x="1" y="1" width="{W*0.75:.0f}" height="{h-2}" rx="14" fill="url(#fade)"/>'
        )
    return (
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="14" fill="{t["bg"]}" stroke="{t["line"]}"/>'
        + grid
    )


# --------------------------------------------------------------------- hero

TRACE = [
    # role, verb, message, outcome
    ("llm", "propose", "root cause: connection pool exhausted on orders-db", "? hypothesis"),
    ("code", "ground", "claim E2 is backed by the evidence it cites", "✓ grounded"),
    ("code", "policy", "restart orders-api · blast radius 1 of 6 replicas", "✓ allowed"),
    ("human", "approve", "waiting for a human before anything changes", "APPROVE"),
    ("code", "verify", "p95 latency back under SLO for 5 minutes", "✓ resolved"),
]


def hero(t):
    h = 424
    cycle = 14.0
    fs = 13
    ch = fs * MONO_CH
    x0, y0, lh = 40, 262, 27
    cols = 92  # total characters per trace line

    css = base_style(t) + f"""
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.pulse{{animation:pulse 1.6s ease-in-out infinite}}
.cursor{{animation:blink 1s step-end infinite}}
"""
    body = [frame(t, h)]

    # top bar
    body.append(
        f'<text x="{x0}" y="44" class="mono faint" font-size="12">~/umangbagadi03 '
        f'<tspan class="muted">$</tspan> <tspan class="text">agent run --until verified</tspan></text>'
        f'<circle cx="{W-112}" cy="40" r="4" class="human pulse"/>'
        f'<text x="{W-100}" y="44" class="mono muted" font-size="12">building</text>'
    )

    # name + tagline
    body.append(
        f'<text x="{x0-2}" y="112" class="sans text" font-size="50" font-weight="700" '
        f'letter-spacing="-1.5">Umang Bagadi</text>'
        f'<text x="{x0}" y="150" class="sans muted" font-size="19">I build LLM agents that '
        f'<tspan class="gold" font-weight="600">prove their work</tspan> before they act.</text>'
        f'<text x="{x0}" y="178" class="mono faint" font-size="12.5">AI engineer · B.Tech in Artificial '
        f'Intelligence · Nagpur, India</text>'
    )

    # trace header + rule
    body.append(
        f'<line x1="{x0}" x2="{W-x0}" y1="{y0-30}" y2="{y0-30}" stroke="{t["line"]}"/>'
        f'<text x="{x0}" y="{y0-38}" class="mono faint" font-size="11" letter-spacing="1.5">'
        f"TRACE · incident #4127</text>"
        f'<text x="{W-x0}" y="{y0-38}" class="mono faint" font-size="11" text-anchor="end" '
        f'letter-spacing="1.5">LLM PROPOSES · CODE DECIDES</text>'
    )

    # trace lines, revealed one by one on a loop
    start, step, hold_until = 0.5, 1.5, 12.6
    for i, (role, verb, msg, outcome) in enumerate(TRACE):
        y = y0 + i * lh
        t_in = start + i * step
        a = t_in / cycle * 100
        b = (t_in + 0.25) / cycle * 100
        c = hold_until / cycle * 100
        d = (hold_until + 0.5) / cycle * 100
        css += (
            f"@keyframes l{i}{{0%,{a:.2f}%{{opacity:0;transform:translateX(-6px)}}"
            f"{b:.2f}%,{c:.2f}%{{opacity:1;transform:none}}{d:.2f}%,100%{{opacity:0}}}}"
            f".l{i}{{animation:l{i} {cycle}s linear infinite}}"
        )
        prefix = f"{i+1:02d}  {role:<6} {verb:<8} {msg} "
        tail = "✓ approved" if role == "human" else outcome
        pad = cols - len(prefix) - len(tail) - 2
        leader = "." * max(pad, 3)
        g = [f'<g class="l{i}">']
        g.append(
            f'<text x="{x0}" y="{y}" class="mono" font-size="{fs}" xml:space="preserve">'
            f'<tspan class="faint">{i+1:02d}  </tspan>'
            f'<tspan class="{role}" font-weight="600">{role:<6}</tspan> '
            f'<tspan class="text">{verb:<8}</tspan> '
            f'<tspan class="muted">{escape(msg)} </tspan>'
            f'<tspan class="faint">{leader}</tspan></text>'
        )
        tx = x0 + (cols - 1) * ch
        if role == "human":
            # "waiting" flips to "approved" a beat after the line appears
            w_on, w_off = t_in / cycle * 100, (t_in + 1.1) / cycle * 100
            css += (
                f"@keyframes wait{{0%,{w_on:.2f}%{{opacity:1}}{w_off:.2f}%,100%{{opacity:0}}}}"
                f"@keyframes ok{{0%,{w_off:.2f}%{{opacity:0}}{w_off+0.5:.2f}%,100%{{opacity:1}}}}"
                f".wait{{animation:wait {cycle}s step-end infinite}}"
                f".ok{{animation:ok {cycle}s linear infinite}}"
            )
            g.append(
                f'<text x="{tx}" y="{y}" class="mono human wait" font-size="{fs}" '
                f'text-anchor="end" opacity="0">◌ waiting</text>'
                f'<text x="{tx}" y="{y}" class="mono human ok" font-size="{fs}" '
                f'text-anchor="end" font-weight="600">✓ approved</text>'
            )
        else:
            cls = "human" if outcome.startswith("✓") else "llm"
            g.append(
                f'<text x="{tx}" y="{y}" class="mono {cls}" font-size="{fs}" '
                f'text-anchor="end" font-weight="600">{escape(outcome)}</text>'
            )
        g.append("</g>")
        body.append("".join(g))

    # prompt + cursor under the trace
    yc = y0 + len(TRACE) * lh + 4
    body.append(
        f'<text x="{x0}" y="{yc}" class="mono muted" font-size="{fs}">›</text>'
        f'<rect x="{x0 + 2*ch}" y="{yc-11}" width="{ch:.1f}" height="14" class="gold cursor"/>'
    )
    return svg(h, "\n".join(body), css, "Umang Bagadi: I build LLM agents that prove their work before they act.")


# -------------------------------------------------------------------- cards

PROJECTS = [
    dict(
        slug="incidentpilot",
        num="01",
        name="IncidentPilot",
        stack="python · langgraph · qdrant · fastapi",
        tagline=[
            "An on-call agent for production incidents that fact-checks its own root",
            "cause, and changes nothing until a policy check and a human say yes.",
        ],
        nodes=[
            ("alert", "io"), ("investigate", "llm"), ("analyze", "llm"), ("ground", "code"),
            ("plan_fix", "llm"), ("policy", "code"), ("approve", "human"), ("verify", "code"),
        ],
        loop=(7, 1, "still broken → re-investigate"),
        proof=["claim-level grounding", "prompt-injection guardrail", "6 adversarial evals"],
    ),
    dict(
        slug="argus",
        num="02",
        name="Argus",
        stack="python · langgraph · gemini · streamlit",
        tagline=[
            "A multi-agent research assistant: plans, researches in parallel, writes",
            "a cited report, critiques its own draft and loops back to fill the gaps.",
        ],
        nodes=[
            ("question", "io"), ("plan", "llm"), ("research ×N", "llm"), ("aggregate", "code"),
            ("write", "llm"), ("critic", "llm"), ("review", "human"), ("finalize", "code"),
        ],
        loop=(5, 1, "gaps found → re-plan"),
        stacked=2,
        proof=["parallel fan-out", "self-critique loop", "resumable human review"],
    ),
    dict(
        slug="kasauti",
        num="03",
        name="Kasauti",
        stack="python · fastapi · langgraph · ollama",
        tagline=[
            "A touchstone for packaged food: scan a label, get a health verdict made",
            "for you. Deterministic rules decide; the LLM only reads and explains.",
        ],
        nodes=[
            ("label", "io"), ("extract", "llm"), ("analyze", "code"), ("enrich", "llm"),
            ("score", "code"), ("explain", "llm"), ("verdict", "io"),
        ],
        loop=(3, 2, "unknown ingredient → re-check"),
        proof=["rules decide, LLMs explain", "Claude · Gemini · GPT · Ollama", "36 offline tests"],
    ),
]


def card(t, p):
    h = 262
    x0 = 32
    css = base_style(t) + """
@keyframes flow{to{stroke-dashoffset:-20}}
.flow{animation:flow 1.1s linear infinite}
@keyframes ping{0%{opacity:0}10%{opacity:1}30%,100%{opacity:0}}
"""
    body = [frame(t, h, dots=False)]

    body.append(
        f'<text x="{x0}" y="50" class="mono gold" font-size="13" font-weight="600">{p["num"]}</text>'
        f'<text x="{x0+30}" y="51" class="sans text" font-size="26" font-weight="700" '
        f'letter-spacing="-0.5">{p["name"]}</text>'
        f'<text x="{W-x0}" y="48" class="mono faint" font-size="12" text-anchor="end">{p["stack"]}</text>'
    )
    for i, line in enumerate(p["tagline"]):
        body.append(
            f'<text x="{x0}" y="{82 + i*21}" class="sans muted" font-size="15">{escape(line)}</text>'
        )

    # pipeline
    fs = 11.5
    ch = fs * MONO_CH
    widths = [len(n) * ch + 22 for n, _ in p["nodes"]]
    gap = (W - 2 * x0 - sum(widths)) / (len(widths) - 1)
    ny, nh = 142, 28
    xs, x = [], x0
    for w in widths:
        xs.append(x)
        x += w + gap

    n = len(p["nodes"])
    hop = 0.45
    for i, ((label, kind), nx, w) in enumerate(zip(p["nodes"], xs, widths)):
        colour = t[kind]
        if i < n - 1:
            ax1, ax2 = nx + w + 4, xs[i + 1] - 4
            body.append(
                f'<line x1="{ax1:.1f}" x2="{ax2:.1f}" y1="{ny+nh/2}" y2="{ny+nh/2}" '
                f'stroke="{t["faint"]}" stroke-width="1.4" stroke-dasharray="3 2" class="flow"/>'
                f'<path d="M{ax2-4:.1f},{ny+nh/2-3.5} L{ax2:.1f},{ny+nh/2} L{ax2-4:.1f},{ny+nh/2+3.5}" '
                f'fill="none" stroke="{t["faint"]}" stroke-width="1.4"/>'
            )
        if p.get("stacked") and label.endswith("×N"):
            for k in range(p["stacked"], 0, -1):
                body.append(
                    f'<rect x="{nx+3*k:.1f}" y="{ny-3*k}" width="{w:.1f}" height="{nh}" rx="7" '
                    f'fill="{t["panel"]}" stroke="{colour}" stroke-opacity="{0.25+0.15*(2-k)}"/>'
                )
        dash = ' stroke-dasharray="3 3"' if kind == "io" else ""
        body.append(
            f'<rect x="{nx:.1f}" y="{ny}" width="{w:.1f}" height="{nh}" rx="7" fill="{t["panel"]}" '
            f'stroke="{colour}" stroke-width="1.3"{dash}/>'
        )
        # a soft highlight travels along the pipeline
        body.append(
            f'<rect x="{nx:.1f}" y="{ny}" width="{w:.1f}" height="{nh}" rx="7" fill="{colour}" '
            f'fill-opacity="0.18" opacity="0" style="animation:ping {n*hop:.2f}s linear '
            f'{i*hop:.2f}s infinite"/>'
        )
        body.append(
            f'<text x="{nx + w/2:.1f}" y="{ny+18.5}" class="mono {kind}" font-size="{fs}" '
            f'text-anchor="middle" font-weight="600">{escape(label)}</text>'
        )

    # self-correction loop drawn under the pipeline
    a, b, label = p["loop"]
    xa = xs[a] + widths[a] / 2
    xb = xs[b] + widths[b] / 2
    yb = ny + nh + 4
    depth = 30
    lw = len(label) * 11 * MONO_CH
    if abs(xa - xb) > lw + 40:
        lx, anchor = (xa + xb) / 2, "middle"
        mask = f'<rect x="{lx - lw/2 - 8:.1f}" y="{yb+depth*0.75-9}" width="{lw+16:.1f}" height="16" fill="{t["bg"]}"/>'
    else:  # short hop: put the label beside the arc instead of on it
        lx, anchor, mask = max(xa, xb) + 14, "start", ""
    body.append(
        f'<path d="M{xa:.1f},{yb} C{xa:.1f},{yb+depth} {xb:.1f},{yb+depth} {xb:.1f},{yb+3}" '
        f'fill="none" stroke="{t["gold"]}" stroke-width="1.3" stroke-dasharray="4 3" class="flow"/>'
        f'<path d="M{xb-4:.1f},{yb+9} L{xb:.1f},{yb+3} L{xb+4:.1f},{yb+9}" fill="none" '
        f'stroke="{t["gold"]}" stroke-width="1.3"/>'
        + mask
        + f'<text x="{lx:.1f}" y="{yb+depth*0.75+3}" class="mono gold" font-size="11" '
        f'text-anchor="{anchor}">{escape(label)}</text>'
    )

    # proof points
    px = x0
    for item in p["proof"]:
        body.append(
            f'<text x="{px}" y="{h-26}" class="mono" font-size="12">'
            f'<tspan class="human">✓</tspan> <tspan class="muted">{escape(item)}</tspan></text>'
        )
        px += (len(item) + 2) * 12 * MONO_CH + 26
    body.append(
        f'<text x="{W-x0}" y="{h-26}" class="mono faint" font-size="12" text-anchor="end">'
        f"view repo ↗</text>"
    )
    return svg(h, "\n".join(body), css, f"{p['name']}: {' '.join(p['tagline'])}")


# -------------------------------------------------------------------- stack

STACK = [
    ("agents", ["LangGraph", "LangChain", "Google ADK", "Pydantic"]),
    ("models", ["Claude", "Gemini", "GPT", "Ollama"]),
    ("retrieval", ["Qdrant", "hybrid RAG", "Tavily"]),
    ("serving", ["FastAPI", "SSE", "Streamlit"]),
    ("ml / cv", ["PyTorch", "TensorFlow", "scikit-learn", "OpenCV", "Detectron2"]),
    ("core", ["Python", "C++", "SQL", "Git"]),
]


def stack(t):
    lh = 38
    h = 44 + len(STACK) * lh + 8
    x0, xc = 32, 156
    fs = 12.5
    ch = fs * MONO_CH
    css = base_style(t) + "@keyframes in{from{opacity:0}to{opacity:1}}"
    body = [frame(t, h, dots=False)]
    for r, (group, items) in enumerate(STACK):
        y = 34 + r * lh
        body.append(
            f'<g style="animation:in .5s ease-out {r*0.12:.2f}s both">'
            f'<text x="{x0}" y="{y+17}" class="mono faint" font-size="12">{group}</text>'
        )
        x = xc
        for item in items:
            w = len(item) * ch + 22
            body.append(
                f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="{t["panel"]}" '
                f'stroke="{t["line"]}"/>'
                f'<text x="{x + w/2:.1f}" y="{y+17}" class="mono text" font-size="{fs}" '
                f'text-anchor="middle">{escape(item)}</text>'
            )
            x += w + 8
        body.append("</g>")
        if r < len(STACK) - 1:
            body.append(
                f'<line x1="{x0}" x2="{W-x0}" y1="{y+lh-6}" y2="{y+lh-6}" stroke="{t["line"]}" '
                f'stroke-dasharray="2 4"/>'
            )
    return svg(h, "\n".join(body), css, "Stack: " + "; ".join(f"{g}: {', '.join(i)}" for g, i in STACK))


# ------------------------------------------------------------------- footer

def footer(t):
    h = 120
    css = base_style(t) + """
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
.cursor{animation:blink 1s step-end infinite}
"""
    line = "the llm proposes. the code decides."
    fs = 20
    ch = fs * MONO_CH
    width = len(line) * ch
    x = (W - width) / 2
    body = [
        frame(t, h),
        f'<text x="{x:.1f}" y="62" class="mono text" font-size="{fs}">'
        f'the <tspan class="llm">llm</tspan> proposes. the <tspan class="gold">code</tspan> decides.</text>',
        f'<rect x="{x + width + 4:.1f}" y="46" width="{ch:.1f}" height="21" class="gold cursor"/>',
        f'<text x="{W/2}" y="92" class="mono faint" font-size="11.5" text-anchor="middle" '
        f'letter-spacing="1.5">EXIT 0 · ALL CLAIMS GROUNDED</text>',
    ]
    return svg(h, "\n".join(body), css, "The LLM proposes. The code decides.")


def main():
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"hero-{name}.svg").write_text(hero(t))
        (OUT / f"stack-{name}.svg").write_text(stack(t))
        (OUT / f"footer-{name}.svg").write_text(footer(t))
        for p in PROJECTS:
            (OUT / f"card-{p['slug']}-{name}.svg").write_text(card(t, p))
    print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)


if __name__ == "__main__":
    main()
