# 🚀 HACKATHON III QUICK START GUIDE

## 📋 **MINIMUM SETUP REQUIRED**

### **Step 1: Install Prerequisites**
```bash
# Install Docker Desktop (required)
# Download from: https://www.docker.com/products/docker-desktop/

# Install Node.js 18+ (for frontend)
# Download from: https://nodejs.org/

# Install Python 3.9+ (for backend)
# Download from: https://www.python.org/
```

### **Step 2: Start Infrastructure**
```bash
# Navigate to project directory
cd "C:\Users\Usman Mustafa\OneDrive\Desktop\Hackathon III_ Reusable Intelligence and Cloud-Native Mastery\learnflow-app"

# Start lightweight Docker Compose setup
docker-compose up -d
```

### **Step 3: Start Backend**
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start API server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **Step 4: Start Frontend**
```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### **Step 5: Access Applications**
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`

---

## 🎮 **QUICK DEMO WALKTHROUGH**

### **1. Visit LearnFlow Dashboard**
Go to `http://localhost:3000` and explore the dashboard

### **2. Try the Code Editor**
- Write some Python code in the Monaco Editor
- Click "Run Code" to execute
- See output in the console

### **3. Chat with AI Tutor**
- Type questions in the AI Tutor chat
- Try: "Explain variables in Python"
- Get instant responses from AI agents

### **4. Browse Lessons**
- Visit `http://localhost:3000/lessons`
- Select different Python lessons
- Practice coding exercises

### **5. Check Progress**
- Visit `http://localhost:3000/dashboard`
- View learning analytics and achievements

---

## 🛠️ **QUICK COMMANDS REFERENCE**

### **Infrastructure**
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Check service status
docker-compose ps
```

### **Backend (in learnflow-app/backend/)**
```bash
# Start development server
uvicorn main:app --reload

# Install dependencies
pip install -r requirements.txt
```

### **Frontend (in learnflow-app/frontend/)**
```bash
# Start development server
npm run dev

# Install dependencies
npm install

# Build for production
npm run build
```

---

## 🚨 **QUICK TROUBLESHOOTING**

### **Services Not Starting**
1. Check Docker Desktop is running
2. Verify all ports are available (8000, 3000, 5432, 9092)
3. Restart Docker and try again

### **Backend Connection Issues**
1. Ensure Docker Compose services are running
2. Check `docker-compose ps` shows all services UP
3. Verify PostgreSQL and Kafka are accessible

### **Frontend Connection Issues**
1. Confirm backend is running on `http://localhost:8000`
2. Check browser console for CORS errors
3. Verify API endpoints are accessible

---

## 🎯 **QUICK EVALUATION CHECKLIST**

### **✅ Skills Library (in skills-library/)**
- [ ] 8 skills implemented with MCP Code Execution
- [ ] All SKILL.md and REFERENCE.md files present
- [ ] All scripts functional

### **✅ LearnFlow Application**
- [ ] Frontend loads at `http://localhost:3000`
- [ ] Backend API works at `http://localhost:8000`
- [ ] Code execution works
- [ ] AI tutor responds to queries
- [ ] Progress tracking functional

### **✅ Architecture**
- [ ] Microservice architecture implemented
- [ ] Event-driven with Kafka
- [ ] Database integration working
- [ ] Token efficiency achieved

---

## ⚡ **TIME ESTIMATED FOR COMPLETE SETUP: 15-20 MINUTES**

1. **Prerequisites Installation**: 5-10 minutes
2. **Infrastructure Start**: 3-5 minutes
3. **Backend Start**: 2-3 minutes
4. **Frontend Start**: 2-3 minutes
5. **System Verification**: 3-5 minutes

---

## 🏆 **YOU'RE READY TO GO!**

Your Hackathon III submission is complete and ready for evaluation. Enjoy exploring the complete LearnFlow AI-powered Python tutoring platform!