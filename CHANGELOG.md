# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

# [1.0.0] - 2026-02-23

### Added
- Implemented full multi-agent orchestration pipeline using LangGraph.
- Added four specialized agents: Retrieval, Analysis, Response, and Escalation.
- Retrieval Agent with structured output for fetching customer data, shipment events (via RAG), and TMS data.
- Analysis Agent with LLM + tool-calling; autonomously selects tools based on context.
  - Tool: `check_weather` for weather impact analysis.
- Response Agent with structured output for risk classification.
- Escalation Agent with tool-calling for notifications and ticketing:
  - Tools: `send_sms`, `send_email`, `create_support_ticket`.
- Ingestion step before the pipeline for email/SMS/call events — embeds and stores in Qdrant before triggering agents. TMS events bypass ingestion and trigger the pipeline directly.
- Agent orchestrator with LangGraph DAG-based workflow and shared state management.
- Progress tracking per shipment — pipeline writes progress to `progress/{shipment_id}.txt` for demo purposes.
- Added mock data folder (`mock_data/`) with sample shipment events and data for local testing.
- Static frontend served via nginx with three pages:
  - `index.html` — landing page with links to both UIs.
  - `agents-ui.html` — agent pipeline trigger and manual progress monitor.
  - `rag-chatbot-ui.html` — RAG chatbot interface.
- Frontend `config.js` for centralized API base URL and endpoint configuration.
- Docker setup for frontend using `nginx:alpine`.
- Added `shipment-intelligence-ui` service to `docker-compose.yaml`.
- Workflow diagrams added to `docs/`:
  - `agent-workflow.png` — LangGraph agent pipeline diagram.
  - `rag-pipeline.png` — RAG pipeline diagram.
- Comprehensive `README.md` with system overview, ASCII pipeline diagram, tech stack, project structure, getting started guide, API endpoint reference with curl examples, and useful Docker commands.

### Changed
- Updated `docker-compose.yaml` to include frontend service alongside API and Qdrant.
- Qdrant URL updated to internal Docker network hostname (`http://qdrant:6333`).
- Progress fetch in agents UI changed to fully manual — removed auto-polling after pipeline trigger.
- Frontend log divider text color fixed for visibility in dark theme.

### Notes
- Both the multi-agent pipeline and RAG chatbot are fully integrated and containerized.
- Progress tracking and logging are file-based for demo purposes; intended to be replaced with a database or message queue in real-time.

---

## [0.2.0] - 2026-02-14

### Added
- Implemented RAG-based shipment intelligence workflow.
- Added LangChain and Qdrant dependencies in `pyproject.toml`.
- Introduced provider abstraction for:
  - LLM
  - Embeddings
  - Vector store
- Added centralized configuration management using `settings.py`.
- Defined provider constants in `constants.py`.
- Implemented dependency wiring in `dependencies.py`.
- Created embedding provider logic.
- Created LLM provider logic using `init_chat_model`.
- Implemented Qdrant client factory for local and remote modes.
- Developed `VectorStoreManager` for embedding and similarity search.
- Built shipment RAG pipeline using LangGraph.
- Defined prompt templates for shipment analysis.
- Implemented RAG service layer for:
  - Shipment event ingestion
  - Shipment investigation queries
- Added request/response schemas with validation.
- Introduced RAG state management for graph workflow.

### Changed
- Refactored health endpoint structure for modular routing.
- Improved project modularization with clear infrastructure separation.

### Notes
- This release introduces a functional RAG-based shipment investigation system.
- Shipment events can now be ingested and queried with contextual reasoning.
- Architecture supports pluggable LLM and embedding providers.

---

## [0.1.0] - 2026-02-13

### Added
- Initial project scaffolding for Shipment Intelligence API
- `pyproject.toml` for dependency and project configuration
- FastAPI application bootstrap (`main.py`)
- Health check endpoint (`/health`)
- Basic router registration structure

### Notes
- This release establishes the foundational API structure.
- Business logic, workflows, and other modules will be added in subsequent versions.