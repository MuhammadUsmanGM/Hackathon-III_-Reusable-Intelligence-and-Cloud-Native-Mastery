// API utility functions for LearnFlow frontend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

interface ApiOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: any;
}

/**
 * Generic API request function
 */
export async function apiRequest<T>(
  endpoint: string,
  options: ApiOptions = {}
): Promise<T> {
  const {
    method = 'GET',
    headers = {},
    body = null
  } = options;

  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers
    },
    ...(body && { body: typeof body === 'string' ? body : JSON.stringify(body) })
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error);
    throw error;
  }
}

/**
 * Tutor/AI Agent API functions
 */

export interface TutorMessage {
  message: string;
  context?: Record<string, any>;
}

export interface TutorResponse {
  role: string;
  content: string;
  timestamp: string;
  context?: Record<string, any>;
}

export async function sendTutorMessage(message: string, context?: Record<string, any>): Promise<TutorResponse> {
  return apiRequest<TutorResponse>('/tutor', {
    method: 'POST',
    body: { message, context }
  });
}

/**
 * Code execution API functions
 */

export interface CodeExecutionRequest {
  code: string;
  input?: string;
  language?: string;
}

export interface CodeExecutionResponse {
  output: string;
  errors: string | null;
  status: 'success' | 'error';
  executionTime: number;
  timestamp: string;
}

export async function executeCode(code: string, input?: string): Promise<CodeExecutionResponse> {
  return apiRequest<CodeExecutionResponse>('/code', {
    method: 'POST',
    body: { code, input, language: 'python' }
  });
}

/**
 * Progress tracking API functions
 */

export interface ProgressData {
  userId: string;
  lessonsCompleted: number;
  exercisesCompleted: number;
  currentStreak: number;
  totalTimeSpent: number;
  achievements: string[];
  progress: Array<{
    lesson: string;
    completed: boolean;
    score: number | null;
  }>;
  [key: string]: any;
}

export interface ProgressUpdate {
  userId: string;
  lessonId?: string;
  exerciseId?: string;
  score?: number;
  completed?: boolean;
}

export async function getUserProgress(userId: string): Promise<ProgressData> {
  return apiRequest<ProgressData>(`/progress?userId=${userId}`, {
    method: 'GET'
  });
}

export async function updateProgress(update: ProgressUpdate): Promise<{ message: string; progress: ProgressData }> {
  return apiRequest<{ message: string; progress: ProgressData }>('/progress', {
    method: 'POST',
    body: update
  });
}

/**
 * Lesson management API functions
 */

export interface Lesson {
  id: number;
  title: string;
  description: string;
  duration: string;
  completed: boolean;
  content: string;
}

export async function getLessons(): Promise<Lesson[]> {
  // This would come from the backend in a real implementation
  // For now, returning a mock response
  return [
    {
      id: 1,
      title: "Python Basics",
      description: "Learn the fundamentals of Python programming",
      duration: "15 min",
      completed: true,
      content: "// Mock content for demonstration"
    },
    {
      id: 2,
      title: "Control Flow",
      description: "Master if statements, loops, and conditionals",
      duration: "20 min",
      completed: false,
      content: "// Mock content for demonstration"
    }
  ];
}