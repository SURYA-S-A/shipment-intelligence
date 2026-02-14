# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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