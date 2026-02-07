# LearnFlow: Autonomous AI-Powered Neural Tutoring

![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)
![Dapr](https://img.shields.io/badge/Dapr-1510C1?style=for-the-badge&logo=dapr&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)

LearnFlow is a state-of-the-art Python tutoring platform engineered for the **Hackathon III: Reusable Intelligence and Cloud-Native Mastery**. It leverages a sophisticated multi-agent architecture, real-time event streaming, and distributed state management to deliver a premium, autonomous learning experience.

## 🚀 Key Features

### 🧠 Multi-Agent Orchestration
A coordinated network of specialized AI agents (Triage, Concepts, Code Review, Debug, Exercise, Progress) that collaboratively guide the student through mastery.

### 🧪 Neural Sandbox
A high-performance interactive Python execution environment powered by **Monaco Editor**, featuring real-time AI logic analysis and telemetry sync.

### ⚡ Cloud-Native Core
*   **Dapr State Management**: Distributed state caching for student progress and architectural session persistence.
*   **Kafka Event Mesh**: Real-time telemetry streaming for **Struggle Detection** and behavior analysis.
*   **Kubernetes Ready**: Production-grade orchestration manifests for global scaling.

### 🛡️ Enterprise-Grade Auth
Standardized authentication flow using **Better Auth**, ensuring secure and seamless session management across the platform.

---

## 🏗️ System Architecture

### Frontend Layer
Built with **Next.js 15** and **Tailwind CSS**, the interface utilizes a proprietary **"Neural" Design System** featuring glassmorphism and high-fidelity micro-interactions.

### Intelligence Layer
The backend is a **FastAPI** microservice mesh integrated with the **Agentic AI Foundation (AAIF)** standards. It utilizes **Distributed Intelligence Units (Skills)** from our reusable library.

### Event & State Layer
- **Message Broker**: Apache Kafka for asynchronous telemetry and alert propagation.
- **State Store**: Redis (via Dapr sidecars) for low-latency progress tracking.
- **Database**: PostgreSQL for persistent structured data.

---

## 🤖 Agentic Infrastructure (Skills)

This project pioneers the **"Skills-as-a-Product"** philosophy. Every core infrastructure task — from Kubernetes cluster setup to Dapr configuration — is handled by **Reusable Intelligence Units** located in the `skills-library`.

- **MCP Code Execution**: Our agents use the Model Context Protocol to execute scripts, ensuring 100% deterministic results while maintaining a low token footprint.
- **AGENTS.md**: This repository is natively designed for AI agent collaboration, featuring comprehensive onboardings for Claude Code and Goose.

---

## 🤝 Contributing & Standards

LearnFlow follows the **Spec-Kit Plus** protocol for specification-driven development. For technical details on the agentic workflows, migration strategies, and cloud deployment, please refer to:

- [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)
- [DOCUMENTATION.md](./DOCUMENTATION.md)
- [AGENTS.md](./AGENTS.md)

---

Developed for **Hackathon III: Reusable Intelligence and Cloud-Native Mastery**.
*Empowering engineers through autonomous intelligence.*