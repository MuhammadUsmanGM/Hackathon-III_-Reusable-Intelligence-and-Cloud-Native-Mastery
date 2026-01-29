# LearnFlow - AI-Powered Python Tutoring Platform

LearnFlow is an innovative Python tutoring platform that leverages AI agents to provide personalized learning experiences. Built using agentic infrastructure with Claude Code and Goose, it demonstrates the power of reusable intelligence.

## 🚀 Features

- **Interactive Python Editor**: Monaco Editor integration for real-time code editing
- **AI Tutoring Agents**: Multi-agent system for personalized learning
- **Exercise System**: Automated exercise generation and evaluation
- **Progress Tracking**: Comprehensive progress analytics and reporting
- **Dark/Light Mode**: User-friendly theme switching
- **Real-time Feedback**: Instant feedback on code execution and debugging

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 15 with TypeScript
- **Styling**: Tailwind CSS with emerald green theme
- **Code Editor**: Monaco Editor
- **State Management**: React Context API

### Backend
- **Framework**: FastAPI with Python 3.9+
- **Database**: PostgreSQL with SQLAlchemy
- **Message Queue**: Apache Kafka
- **AI Agents**: Multi-agent architecture for tutoring

## 🛠️ Installation

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker (for Kafka and PostgreSQL)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd learnflow-app
   ```

2. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Set up the backend**
   ```bash
   cd ../backend
   ./start_services.sh  # On Linux/Mac
   # OR
   start_services.bat   # On Windows
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Infrastructure (Docker Compose)
```bash
cd learnflow-app
docker-compose up -d
```

## 🤖 AI Agent System

LearnFlow features a sophisticated multi-agent architecture:

- **Triage Agent**: Assesses student needs and routes appropriately
- **Concepts Agent**: Explains Python concepts with examples
- **Code Review Agent**: Provides improvement suggestions
- **Debug Agent**: Helps debug Python code
- **Exercise Agent**: Generates and evaluates exercises
- **Progress Agent**: Tracks and analyzes learning progress

## 📚 Usage

1. **Browse Lessons**: Navigate to the Lessons section to access Python tutorials
2. **Practice Coding**: Use the interactive code editor to practice
3. **Get Help**: Ask questions to the AI tutor assistant
4. **Track Progress**: Monitor your learning journey in the dashboard
5. **Complete Exercises**: Practice with auto-graded exercises

## 🧩 Skills Integration

This application demonstrates the use of reusable skills from the skills-library:
- **MCP Code Execution Pattern**: For efficient token usage
- **Infrastructure as Code**: Automated deployment of services
- **Agentic Workflows**: Autonomous AI agent operations

## 🚀 Deployment

### Frontend
Deploy the Next.js application to platforms like:
- Vercel
- Netlify
- Any static hosting service

### Backend
Deploy the FastAPI application as:
- Docker containers
- Cloud functions
- Traditional server deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the Hackathon III: Reusable Intelligence and Cloud-Native Mastery challenge.

## 📚 Documentation

For detailed documentation, see [DOCUMENTATION.md](./DOCUMENTATION.md).

---

Made with ❤️ for the Hackathon III: Reusable Intelligence and Cloud-Native Mastery