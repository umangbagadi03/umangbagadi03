<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img alt="Umang Bagadi. I build LLM agents that prove their work before they act. An agent trace runs: the LLM proposes a root cause, code checks the claim against evidence, code checks policy, a human approves, code verifies recovery." src="assets/hero-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/umang-bagadi"><b>LinkedIn</b></a> &nbsp;·&nbsp;
  <a href="https://x.com/BagadiUmang"><b>X / Twitter</b></a> &nbsp;·&nbsp;
  <a href="#selected-work"><b>Selected work</b></a> &nbsp;·&nbsp;
  <a href="#how-i-build"><b>How I build</b></a>
</p>

Most agent demos trust whatever the model writes. Mine don't. I treat an LLM like a smart but fallible junior engineer: it reads, ranks and explains, and plain, tested code decides what counts as true, what's allowed, and whether it worked.

## Selected work

<sub>🟪 the LLM proposes &nbsp; 🟨 code decides &nbsp; 🟩 a human approves &nbsp; ⤺ the agent corrects itself</sub>

<a href="https://github.com/umangbagadi03/incidentpilot">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-incidentpilot-dark.svg">
    <img alt="IncidentPilot: an on-call agent for production incidents that fact-checks its own root cause and changes nothing until a policy check and a human approve." src="assets/card-incidentpilot-light.svg" width="100%">
  </picture>
</a>

<a href="https://github.com/umangbagadi03/argus">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-argus-dark.svg">
    <img alt="Argus: a multi-agent research assistant that plans, researches in parallel, writes a cited report, critiques its own draft and loops back to fill gaps." src="assets/card-argus-light.svg" width="100%">
  </picture>
</a>

<a href="https://github.com/umangbagadi03/kasauti">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-kasauti-dark.svg">
    <img alt="Kasauti: scan a packaged-food label and get a personalised health verdict. Deterministic rules decide; the LLM only reads and explains." src="assets/card-kasauti-light.svg" width="100%">
  </picture>
</a>

## How I build

**01 · The LLM proposes, the code decides.**
Models read, rank and explain. Verdicts, policies and "did it work?" are deterministic code you can unit-test.

**02 · Every claim cites its evidence.**
If a sentence can't point to the log line, source or label it came from, confidence drops and a human takes over.

**03 · Nothing irreversible without a human.**
Agents investigate with read-only tools. Changes pass a policy check, then pause for approval, even across restarts.

**04 · If it isn't evaluated, it doesn't work.**
Adversarial scenarios (red herrings, failed first fixes, prompt injection, no-answer cases) run before I trust a demo.

## Stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img alt="Agents: LangGraph, LangChain, Google ADK, Pydantic. Models: Claude, Gemini, GPT, Ollama. Retrieval: Qdrant, hybrid RAG, Tavily. Serving: FastAPI, SSE, Streamlit. ML and CV: PyTorch, TensorFlow, scikit-learn, OpenCV, Detectron2. Core: Python, C++, SQL, Git." src="assets/stack-light.svg" width="100%">
</picture>

<details>
<summary><b>Before agents: the 2021–2023 archive</b></summary>
<br>

Computer vision, NLP and classic ML, from my first years of building.

| Project | What it is |
|---|---|
| [Dino game with facial recognition](https://github.com/umangbagadi03/Dino-game-using-facial-recognition) | Chrome's T-Rex game, played with facial expressions via OpenCV |
| [AIPS-3 semantic search](https://github.com/umangbagadi03/AIPS-3) | AI-powered smart search: find the exact passage in a book or PDF |
| [Auto-ML app](https://github.com/umangbagadi03/Auto-ML-App) | Bring a dataset; it handles features, model selection and tuning |
| [MLOps](https://github.com/umangbagadi03/MLOPS) | A reproducible ML pipeline versioned with DVC |
| [Stock market forecasting](https://github.com/umangbagadi03/Stock-Market-Forecasting) | Stacked-LSTM price forecasting |
| [Twitter sentiment analysis](https://github.com/umangbagadi03/Twitter_Sentiment_Analysis) | NLP sentiment classifier for tweets |
| [Song recommender](https://github.com/umangbagadi03/Song-Recommendation-System) | Spotify-style song recommendations, served as a web app |
| [SMS spam classifier](https://github.com/umangbagadi03/SMS-SPAM-CLASSIFIER) | Spam vs ham with classic NLP features |
| [Data structures & algorithms](https://github.com/umangbagadi03/Data_Structure_Algorithm) | C++ solutions from my DSA practice |

</details>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <img alt="The LLM proposes. The code decides." src="assets/footer-light.svg" width="100%">
</picture>
