# Spec-Kit Plus: LearnFlow Platform Specification

## 1. System Intent
LearnFlow is an autonomous, AI-powered Python tutoring platform designed to facilitate mastery of programming concepts through real-time agentic interaction and event-driven microservices.

## 2. Architectural Specs
- **Logic Isolation**: All AI reasoning must be handled by specialized agents (Triage, Concepts, Review, Debug, Exercise, Progress).
- **Event Mesh**: All student interactions must emit events to **Apache Kafka**.
- **State Resilience**: Student progress and session data must be managed via **Dapr State Store (Redis)**.
- **Identity**: Authentication must follow the **Better Auth** standard for Next.js.

## 3. High-Level Requirements
### RL-1: Real-time Tutoring
The system shall provide a multi-modal chat interface where a Triage Agent routes queries to the most efficient specialist agent.

### RL-2: Neural Sandbox
The system shall provide a Monaco-based code editor with secure execution and immediate AI feedback.

### RL-3: Struggle Detection (Key Metric)
The Progress Agent shall monitor session telemetry (Kafka stream) and trigger a `STRUGGLE_ALERT` if:
- > 3 consecutive logic errors.
- < 50% mastery on dynamic quizzes.
- > 10 minutes of inactivity on a complex exercise.

## 4. Skills Library Specs
All infrastructure (Kafka, Postgres, Dapr) and service deployments (FastAPI, Next.js) MUST be executed using **MCP Code Execution Skills** to maintain a compact context window and maximize agentic autonomy.

---
*Generated via Spec-Kit Plus Protocol v1.0*
