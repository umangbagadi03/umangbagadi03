<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img alt="Umang Bagadi. I build LLM agents that prove their work before they act. An agent trace runs: the LLM proposes a root cause, code checks the claim against evidence, code checks policy, a human approves, code verifies recovery." src="assets/hero-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/umang-bagadi"><b>LinkedIn</b></a> &nbsp;·&nbsp;
  <a href="https://x.com/BagadiUmang"><b>X / Twitter</b></a> &nbsp;·&nbsp;
  <a href="#what-i-build"><b>What I build</b></a> &nbsp;·&nbsp;
  <a href="#how-i-build"><b>How I build</b></a>
</p>

Most agent demos trust whatever the model writes. Mine don't. I treat an LLM like a smart but fallible junior engineer: it reads, ranks and explains, and plain, tested code decides what counts as true, what's allowed, and whether it worked.

## What I build

<sub>🟪 the LLM proposes &nbsp; 🟨 code decides &nbsp; 🟩 a human approves</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/skills-dark.svg">
  <img alt="Agent workflows: multi-step LangGraph agents with planners, parallel workers, critics and checkpointed state. Grounding: every claim cites its evidence and code checks it. Guardrails: read-only tools by default, policy checks before any change, prompt-injection quarantine. Human-in-the-loop: agents pause for approval and resume later. Evaluation: adversarial scenarios scored on outcome, safety and grounding. Retrieval and models: hybrid RAG on Qdrant; Claude, Gemini, GPT or local Ollama behind one provider layer." src="assets/skills-light.svg" width="100%">
</picture>

## How I build

**01 · The LLM proposes, the code decides.**
Models read, rank and explain. Verdicts, policies and "did it work?" are deterministic code you can unit-test.

**02 · Every claim cites its evidence.**
If a sentence can't point to the log line, source or label it came from, confidence drops and a human takes over.

**03 · Nothing irreversible without a human.**
Agents start with read-only tools. Changes pass a policy check, then pause for approval, even across restarts.

**04 · If it isn't evaluated, it doesn't work.**
Adversarial scenarios (red herrings, failed first fixes, prompt injection, no-answer cases) run before I trust a demo.

## The GenAI stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img alt="The GenAI stack I build with. Models: Claude, GPT, Gemini, Llama via Ollama, LiteLLM, Hugging Face. Orchestration: LangGraph, LangChain, Google ADK, MCP, Instructor, Pydantic. Retrieval: Qdrant, sqlite-vec, hybrid BM25 plus dense search, sentence-transformers. Ingestion: Docling, pdfplumber, Trafilatura, Tavily search. Evals and tracing: Langfuse, LangSmith, OpenTelemetry, Prometheus, pytest evals. Serving: FastAPI, SSE streaming, Streamlit, Postgres, SQLite. ML foundations: PyTorch, Transformers, scikit-learn, TensorFlow, OpenCV. Core: Python, C++, SQL, Git." src="assets/stack-light.svg" width="100%">
</picture>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <img alt="The LLM proposes. The code decides." src="assets/footer-light.svg" width="100%">
</picture>

<p align="center"><sub>My latest projects are pinned below ↓</sub></p>
