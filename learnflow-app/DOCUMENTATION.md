# LearnFlow Application Documentation

## Overview
LearnFlow is an AI-powered Python tutoring platform built using agentic infrastructure with Claude Code and Goose. The platform features a multi-agent architecture for personalized learning experiences.

## Architecture

### Frontend
- **Framework**: Next.js 15 with TypeScript
- **Styling**: Tailwind CSS with emerald green theme
- **Code Editor**: Monaco Editor for Python code editing
- **Icons**: React Icons
- **State Management**: React Context API

### Backend
- **Framework**: FastAPI with Python 3.9+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Message Queue**: Apache Kafka for event-driven architecture
- **AI Agents**: Multi-agent system for tutoring (Triage, Concepts, Code Review, Debug, Exercise, Progress)

## Features

### AI Tutoring Agents
1. **Triage Agent**: Assesses student needs and routes to appropriate agents
2. **Concepts Agent**: Explains Python programming concepts with examples
3. **Code Review Agent**: Reviews Python code and suggests improvements
4. **Debug Agent**: Helps students debug their Python code
5. **Exercise Agent**: Generates Python programming exercises and evaluates solutions
6. **Progress Agent**: Tracks and analyzes student progress

### Learning Components
- Interactive Python code editor with Monaco Editor
- Exercise system with automated evaluation
- Progress tracking and analytics
- Personalized learning recommendations
- Achievement system
- Dark/light mode support

## Project Structure

```
learnflow-app/
├── backend/
│   ├── main.py                 # Main FastAPI application
│   ├── models/                 # Data models (User, Lesson, Progress)
│   ├── api/                    # API routes (v1)
│   │   └── v1/
│   │       ├── tutor.py        # Tutoring endpoints
│   │       ├── code.py         # Code execution endpoints
│   │       ├── progress.py     # Progress tracking endpoints
│   │       ├── users.py        # User management endpoints
│   │       └── lessons.py      # Lesson management endpoints
│   ├── services/               # Business logic services
│   │   ├── ai/                 # AI agent services
│   │   ├── code_execution/     # Secure code execution
│   │   ├── kafka/              # Kafka event handling
│   │   ├── database/           # Database operations
│   │   └── learnflow_service.py # Main service orchestrator
│   ├── agents/                 # AI agent implementations
│   │   ├── agent_manager.py    # Coordinates multi-agent system
│   │   ├── triage_agent.py     # Initial assessment agent
│   │   ├── concepts_agent.py   # Concept explanation agent
│   │   ├── code_review_agent.py # Code review agent
│   │   ├── debug_agent.py      # Debugging agent
│   │   ├── exercise_agent.py   # Exercise generation agent
│   │   └── progress_agent.py   # Progress tracking agent
│   ├── requirements.txt        # Python dependencies
│   ├── start_services.sh       # Linux/Mac startup script
│   └── start_services.bat      # Windows startup script
└── frontend/
    ├── app/                    # Next.js app directory
    │   ├── page.tsx            # Main dashboard page
    │   ├── layout.tsx          # Root layout
    │   ├── lessons/            # Lessons page
    │   ├── exercises/          # Exercises page
    │   ├── dashboard/          # Dashboard page
    │   └── globals.css         # Global styles
    ├── api/                    # Next.js API routes
    │   ├── tutor/route.ts      # Tutor API endpoint
    │   ├── code/route.ts       # Code execution API endpoint
    │   └── progress/route.ts   # Progress API endpoint
    ├── utils/                  # Utility functions
    │   └── api.ts              # API utility functions
    ├── context/                # React Context providers
    │   └── AppContext.tsx      # Global app state
    ├── package.json            # Node.js dependencies
    └── README.md               # Frontend documentation
```

## Installation & Setup

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- Docker (for Kafka and PostgreSQL)

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd learnflow-app/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Access the frontend at `http://localhost:3000`

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd learnflow-app/backend
   ```

2. Run the startup script:
   ```bash
   # On Windows
   start_services.bat

   # On Linux/Mac
   ./start_services.sh
   ```

3. Access the API at `http://localhost:8000`
4. API documentation available at `http://localhost:8000/docs`

### Infrastructure Setup (Docker Compose)
1. Use the provided docker-compose.yml for local development:
   ```bash
   cd learnflow-app
   docker-compose up -d
   ```

## API Endpoints

### Tutor API
- `POST /api/v1/tutor/` - Process tutoring requests
- `POST /api/v1/tutor/explain-concept` - Get concept explanations
- `POST /api/v1/tutor/review-code` - Review code
- `POST /api/v1/tutor/debug-code` - Debug code

### Code Execution API
- `POST /api/v1/code/` - Execute Python code
- `POST /api/v1/code/evaluate-exercise` - Evaluate exercise solutions

### Progress API
- `GET /api/v1/progress/{user_id}` - Get user progress
- `POST /api/v1/progress/update` - Update user progress
- `GET /api/v1/progress/{user_id}/recommendations` - Get learning recommendations

### Users API
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{user_id}` - Get user by ID

### Lessons API
- `GET /api/v1/lessons/` - Get all lessons
- `GET /api/v1/lessons/{lesson_id}` - Get specific lesson
- `POST /api/v1/lessons/` - Create new lesson

## Security Features

### Code Execution Sandbox
- Timeout limits (10 seconds)
- Memory limits (100MB)
- Dangerous operation detection (imports, system calls, etc.)
- Input/output buffering

### Data Validation
- Input sanitization
- Type validation using Pydantic
- Rate limiting (to be implemented)

## Development

### Adding New AI Agents
1. Create a new agent class in `backend/agents/`
2. Implement the required interface
3. Register the agent in `backend/agents/__init__.py`
4. Update the `AgentManager` to include the new agent
5. Add corresponding API endpoints if needed

### Adding New Lessons
1. Create lesson content with proper formatting
2. Add to the database through the lessons API
3. Ensure proper categorization and difficulty levels

## Deployment

### Frontend
The frontend is built with Next.js and can be deployed to:
- Vercel (recommended)
- Netlify
- Any static hosting service

### Backend
The backend can be deployed as:
- Docker containers
- Cloud functions
- Traditional server deployment

## Skills Integration

The LearnFlow application leverages the skills in the `skills-library`:
- **agents-md-gen**: Generate AGENTS.md for repository documentation
- **k8s-foundation**: Check cluster health and basic deployments
- **kafka-k8s-setup**: Deploy Kafka on Kubernetes
- **postgres-k8s-setup**: Deploy PostgreSQL on Kubernetes
- **fastapi-dapr-agent**: Deploy FastAPI services with Dapr
- **mcp-code-execution**: Implement MCP with code execution pattern
- **nextjs-k8s-deploy**: Deploy Next.js applications
- **docusaurus-deploy**: Deploy documentation sites

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Hackathon III: Reusable Intelligence and Cloud-Native Mastery challenge.