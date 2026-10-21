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

PROFILE = [
    ("role", "AI engineer · LLM agents, RAG and evals"),
    ("focus", "agents that check their own work before they act"),
    ("building", None),  # rotates through BUILDING
    ("studying", "B.Tech in Artificial Intelligence"),
    ("based in", "Nagpur, India"),
]
BUILDING = [
    "multi-agent systems",
    "RAG pipelines with citations",
    "LLM evals and guardrails",
    "MCP tools for agents",
    "human-in-the-loop workflows",
]


def hero(t):
    h = 400
    fs = 14
    x0, xv, y0, lh = 40, 150, 222, 30

    css = base_style(t) + """
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
.pulse{animation:pulse 1.6s ease-in-out infinite}
.cursor{animation:blink 1s step-end infinite}
"""
    body = [frame(t, h)]

    body.append(
        f'<text x="{x0}" y="44" class="mono faint" font-size="12">~/umangbagadi03 '
        f'<tspan class="muted">$</tspan> <tspan class="text">whoami</tspan></text>'
        f'<circle cx="{W-112}" cy="40" r="4" class="human pulse"/>'
        f'<text x="{W-100}" y="44" class="mono muted" font-size="12">building</text>'
        f'<text x="{x0-2}" y="112" class="sans text" font-size="50" font-weight="700" '
        f'letter-spacing="-1.5">Umang Bagadi</text>'
        f'<text x="{x0}" y="150" class="sans muted" font-size="19">I build LLM agents that '
        f'<tspan class="gold" font-weight="600">prove their work</tspan> before they act.</text>'
        f'<line x1="{x0}" x2="{W-x0}" y1="{y0-36}" y2="{y0-36}" stroke="{t["line"]}"/>'
    )

    for i, (key, value) in enumerate(PROFILE):
        y = y0 + i * lh
        g = (
            f'<g style="animation:in .45s ease-out {0.3 + i*0.35:.2f}s both">'
            f'<text x="{x0}" y="{y}" class="mono gold" font-size="{fs}">›</text>'
            f'<text x="{x0+20}" y="{y}" class="mono faint" font-size="{fs}">{escape(key)}</text>'
        )
        if value is not None:
            g += f'<text x="{xv}" y="{y}" class="mono text" font-size="{fs}">{escape(value)}</text>'
        else:
            n, per = len(BUILDING), 2.4
            cycle = n * per
            for k, word in enumerate(BUILDING):
                a0 = k * per / cycle * 100
                a1 = a0 + 0.3 / cycle * 100
                a2 = (k + 1) * per / cycle * 100 - 0.3 / cycle * 100
                a3 = (k + 1) * per / cycle * 100
                css += (
                    f"@keyframes w{k}{{0%,{a0:.2f}%{{opacity:0;transform:translateY(6px)}}"
                    f"{a1:.2f}%,{a2:.2f}%{{opacity:1;transform:none}}"
                    f"{a3:.2f}%,100%{{opacity:0;transform:translateY(-6px)}}}}"
                    f".w{k}{{opacity:{1 if k == 0 else 0};animation:w{k} {cycle}s linear infinite}}"
                )
                g += (
                    f'<text x="{xv}" y="{y}" class="mono llm w{k}" font-size="{fs}" '
                    f'font-weight="600">{escape(word)}</text>'
                )
        body.append(g + "</g>")

    yc = y0 + len(PROFILE) * lh
    body.append(
        f'<text x="{x0}" y="{yc}" class="mono gold" font-size="{fs}">›</text>'
        f'<rect x="{x0+20}" y="{yc-12}" width="{fs*MONO_CH:.1f}" height="15" class="gold cursor"/>'
    )
    return svg(h, "\n".join(body), css,
               "Umang Bagadi. I build LLM agents that prove their work before they act. "
               "AI engineer working on LLM agents, RAG and evals. B.Tech in AI, Nagpur, India.")


# ------------------------------------------------------------- capabilities

SKILLS = [
    # title, role colour, two-line description
    ("Agent workflows", "llm", ["Multi-step LangGraph agents: planners, parallel",
                                "workers, critics and checkpointed state."]),
    ("Grounding", "code", ["Every claim cites its evidence and code checks it.",
                           "Weak support lowers confidence automatically."]),
    ("Guardrails", "code", ["Read-only tools by default, policy checks before",
                            "any change, prompt-injection quarantine."]),
    ("Human-in-the-loop", "human", ["Agents pause for approval and resume later,",
                                    "even after a restart."]),
    ("Evaluation", "code", ["Adversarial scenarios scored on outcome, safety",
                            "and grounding before anything ships."]),
    ("Retrieval & models", "llm", ["Hybrid RAG on Qdrant. Claude, Gemini, GPT or a",
                                   "local Ollama model behind one provider layer."]),
]


def skills(t):
    cols, pad, gutter = 2, 32, 16
    tw = (W - 2 * pad - gutter) / cols
    th, vgap = 104, 14
    rows = (len(SKILLS) + cols - 1) // cols
    h = 2 * 28 + rows * th + (rows - 1) * vgap
    n = len(SKILLS)
    step = 0.9
    css = base_style(t) + f"""
@keyframes in{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}
@keyframes bar{{0%{{transform:scaleX(0)}}{100/n:.2f}%{{transform:scaleX(1)}}{100/n+6:.2f}%,100%{{transform:scaleX(1);opacity:0}}}}
"""
    body = [frame(t, h, dots=False)]
    for i, (title, kind, desc) in enumerate(SKILLS):
        x = pad + (i % cols) * (tw + gutter)
        y = 28 + (i // cols) * (th + vgap)
        colour = t[kind]
        body.append(
            f'<g style="animation:in .5s ease-out {i*0.1:.2f}s both">'
            f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{th}" rx="10" fill="{t["panel"]}" '
            f'stroke="{t["line"]}"/>'
            f'<rect x="{x+18:.1f}" y="{y}" width="28" height="2" fill="{colour}"/>'
            # a highlight sweeps across the tiles one after another
            f'<rect x="{x+18:.1f}" y="{y}" width="{tw-36:.1f}" height="2" fill="{colour}" '
            f'style="transform-box:fill-box;transform-origin:left;transform:scaleX(0);'
            f'animation:bar {n*step:.1f}s ease-out {i*step:.1f}s infinite"/>'
            f'<text x="{x+18:.1f}" y="{y+34}" class="mono gold" font-size="12" font-weight="600">'
            f"{i+1:02d}</text>"
            f'<text x="{x+44:.1f}" y="{y+35}" class="sans text" font-size="17" font-weight="700">'
            f"{escape(title)}</text>"
            f'<circle cx="{x+tw-22:.1f}" cy="{y+30}" r="4" fill="{colour}"/>'
        )
        for j, line in enumerate(desc):
            body.append(
                f'<text x="{x+18:.1f}" y="{y+62+j*20}" class="sans muted" font-size="13.5">'
                f"{escape(line)}</text>"
            )
        body.append("</g>")
    alt = "What I build: " + "; ".join(f"{s[0]}: {' '.join(s[2])}" for s in SKILLS)
    return svg(h, "\n".join(body), css, alt)


# -------------------------------------------------------------------- stack

# Layers of a GenAI system, from the model down to the foundations.
STACK = [
    ("models", "reason", ["Claude", "GPT", "Gemini", "Llama · Ollama", "LiteLLM", "Hugging Face"]),
    ("orchestration", "plan & act", ["LangGraph", "LangChain", "Google ADK", "MCP", "Instructor", "Pydantic"]),
    ("retrieval", "ground", ["Qdrant", "sqlite-vec", "hybrid BM25 + dense", "sentence-transformers"]),
    ("ingestion", "read", ["Docling", "pdfplumber", "Trafilatura", "Tavily search"]),
    ("evals & tracing", "observe", ["Langfuse", "LangSmith", "OpenTelemetry", "Prometheus", "pytest evals"]),
    ("serving", "ship", ["FastAPI", "SSE streaming", "Streamlit", "Postgres", "SQLite"]),
    ("ml foundations", "train", ["PyTorch", "Transformers", "scikit-learn", "TensorFlow", "OpenCV"]),
    ("core", "build", ["Python", "C++", "SQL", "Git"]),
]


def stack(t):
    n = len(STACK)
    lh, top = 40, 62
    h = top + n * lh + 14
    x0, rail, xc = 32, 168, 190
    fs = 12.5
    ch = fs * MONO_CH
    beat = 0.9  # seconds the pulse spends on each layer
    cycle = n * beat
    css = base_style(t) + f"""
@keyframes rail{{from{{transform:translateY(0)}}to{{transform:translateY({(n-1)*lh}px)}}}}
.pulse-dot{{animation:rail {cycle:.1f}s linear infinite}}
"""
    body = [frame(t, h)]
    body.append(
        f'<text x="{x0}" y="36" class="mono faint" font-size="11" letter-spacing="1.5">'
        f"THE GENAI STACK I BUILD WITH</text>"
        f'<text x="{W-x0}" y="36" class="mono faint" font-size="11" text-anchor="end" '
        f'letter-spacing="1.5">REQUEST ↓ THROUGH EVERY LAYER</text>'
    )
    y_first = top + 13
    body.append(
        f'<line x1="{rail}" x2="{rail}" y1="{y_first}" y2="{y_first+(n-1)*lh}" '
        f'stroke="{t["line"]}" stroke-width="2"/>'
    )

    for r, (layer, verb, items) in enumerate(STACK):
        y = top + r * lh
        cy = y + 13
        on = r / n * 100
        off = (r + 1) / n * 100
        css += (
            f"@keyframes r{r}{{0%,{max(on-0.01,0):.2f}%{{opacity:0}}{on+1:.2f}%,{off:.2f}%{{opacity:1}}"
            f"{min(off+4,100):.2f}%,100%{{opacity:0}}}}"
            f".r{r}{{opacity:0;animation:r{r} {cycle:.1f}s linear infinite}}"
        )
        body.append(
            f'<text x="{x0}" y="{cy+1}" class="mono muted" font-size="12">{escape(layer)}</text>'
            f'<text x="{x0}" y="{cy+15}" class="mono faint" font-size="10">{escape(verb)}</text>'
            f'<text x="{x0}" y="{cy+1}" class="mono gold r{r}" font-size="12" font-weight="600">'
            f"{escape(layer)}</text>"
            f'<circle cx="{rail}" cy="{cy}" r="4" fill="{t["bg"]}" stroke="{t["faint"]}" stroke-width="1.5"/>'
        )
        x = xc
        for k, item in enumerate(items):
            w = len(item) * ch + 22
            body.append(
                f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="{t["panel"]}" '
                f'stroke="{t["line"]}"/>'
                f'<g class="r{r}" style="animation-delay:{k*0.06:.2f}s">'
                f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="{t["gold"]}" '
                f'fill-opacity="0.12" stroke="{t["gold"]}" stroke-opacity="0.7"/></g>'
                f'<text x="{x + w/2:.1f}" y="{y+17}" class="mono text" font-size="{fs}" '
                f'text-anchor="middle">{escape(item)}</text>'
            )
            x += w + 8
        assert x - 8 <= W - x0, f"layer {layer!r} overflows by {x - 8 - (W - x0):.0f}px"

    body.append(
        f'<g class="pulse-dot"><circle cx="{rail}" cy="{y_first}" r="9" fill="{t["gold"]}" '
        f'fill-opacity="0.18"/><circle cx="{rail}" cy="{y_first}" r="4.5" fill="{t["gold"]}"/></g>'
    )
    alt = "The GenAI stack I build with. " + " ".join(
        f"{layer.capitalize()}: {', '.join(items)}." for layer, _, items in STACK
    )
    return svg(h, "\n".join(body), css, alt)


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
        (OUT / f"skills-{name}.svg").write_text(skills(t))
    print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)


if __name__ == "__main__":
    main()
