# Production Microservice Demo

This repository demonstrates a production-grade microservice architecture designed for high-performance data ingestion and indexing. It serves as a showcase of modern Python development practices, including robust dependency injection, configuration management, and optimized containerization.

## 🏗️ Architecture Overview

The system is designed as a distributed pipeline:

*   **`ingestapi`**: A FastAPI-based entry point that accepts data and dispatches tasks. It handles request validation and queues jobs for asynchronous processing.
*   **`ingestworker`**: A Celery worker that consumes tasks from the queue (Redis). It handles heavy lifting, data transformation, and storage operations.
*   **`indexapi`**: (Planned) A service dedicated to managing vector indices (Milvus).
*   **`searchapi`**: (Planned) A high-performance **Gin (Go)** server for serving user-facing search queries with low latency.
*   **`shared`**: A core library containing common utilities, configuration schemas, and shared domain logic to ensure consistency across services.

## 🧩 Code Patterns & Design Choices

### Dependency Injection (DI)
The project utilizes the `dependency-injector` library to manage component lifecycles and dependencies.
*   **Declarative Containers**: Services and resources are defined in `container.py` using `containers.DeclarativeContainer`.
*   **Wiring**: The `container.wire()` method is used to inject dependencies into FastAPI routers and Celery tasks, keeping business logic decoupled from infrastructure concerns.
*   **Singleton Pattern**: Heavy resources (like Storage clients or Database connections) are managed as Singletons to ensure efficient resource usage.

### Configuration Management
Configuration is handled via `pydantic-settings` with custom extensions for YAML support.
*   **Type Safety**: All configurations are defined as Pydantic models (`BaseConfig`), ensuring type safety and validation at startup.
*   **Hierarchical Loading**: The `BaseConfig` class in `shared/config` implements a custom source to load from YAML files (`conf/*.yaml`) while allowing overrides via environment variables (using `__` as a nested delimiter).
*   **Centralized Config**: Shared configuration logic resides in the `shared` library, promoting code reuse.

### Project Layout
The repository follows a monorepo-style structure:
*   **`shared/`**: Contains reusable code (logging, storage adapters, config logic).
*   **`service_name/`**: Each service has its own directory with a standard structure (`api/`, `service/`, `config/`, `container.py`).
*   **`conf/`**: Centralized location for service configuration files.

## 🐳 Docker Optimizations

The Dockerfiles are engineered for speed, security, and minimal footprint:

*   **Package Manager (`uv`)**: We use `uv` (by Astral) instead of pip/poetry for lightning-fast dependency resolution and installation.
*   **Multi-Stage Builds**:
    *   **Builder Stage**: Compiles dependencies and creates a virtual environment. It uses `RUN --mount=type=cache` to cache `uv` artifacts, significantly speeding up re-builds.
    *   **Final Stage**: A pristine `python:3.13-slim` image where only the pre-built `.venv` and application code are copied.
*   **Layer Caching**: Dependencies are installed (`uv sync --no-install-project`) *before* copying the source code. This ensures that changing application code does not invalidate the dependency layer.
*   **Bytecode Compilation**: The `--compile-bytecode` flag is used during installation to improve container startup time.
*   **Security**: Minimal runtime dependencies are installed, and apt caches are cleaned up (`rm -rf /var/lib/apt/lists/*`) to reduce attack surface and image size.

## 🚀 Todo / Roadmap

The following components and features are planned for implementation:

- [ ] **Frontend**: Develop a user interface (React/Next.js) for interacting with the ingestion and search APIs.
- [ ] **Search API**: Implement the `searchapi` using **Gin (Go)** to expose high-performance vector search capabilities.
- [ ] **Observability Stack**:
    -   Deploy **Grafana** for visualization.
    -   Configure **Loki** for log aggregation.
    -   Set up **Prometheus** for metrics collection.
    -   Implement **Grafana Alloy** for telemetry data forwarding.
- [ ] **Orchestration**:
    -   **Docker Compose**: Create a comprehensive `docker-compose.yml` to spin up the entire stack (Redis, Milvus, Observability, Services) with a single command.
    -   **Kubernetes**: Develop a production-ready **Helm Chart** to demonstrate Kubernetes deployment skills, including ingress, scaling policies, and resource limits.
