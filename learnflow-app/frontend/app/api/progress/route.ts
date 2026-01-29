import { NextRequest, NextResponse } from 'next/server';

// In-memory storage for demo purposes (would be replaced with database in production)
let mockProgressData: Record<string, any> = {
  'student-1': {
    userId: 'student-1',
    lessonsCompleted: 5,
    exercisesCompleted: 12,
    currentStreak: 3,
    totalTimeSpent: 120, // minutes
    achievements: ['First Steps', 'Bug Finder', 'Code Warrior'],
    progress: [
      { lesson: 'Python Basics', completed: true, score: 95 },
      { lesson: 'Variables and Data Types', completed: true, score: 87 },
      { lesson: 'Control Flow', completed: true, score: 92 },
      { lesson: 'Functions', completed: false, score: null },
      { lesson: 'Object-Oriented Programming', completed: false, score: null }
    ]
  }
};

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const userId = searchParams.get('userId') || 'student-1';

  try {
    const progress = mockProgressData[userId] || {
      userId,
      lessonsCompleted: 0,
      exercisesCompleted: 0,
      currentStreak: 0,
      totalTimeSpent: 0,
      achievements: [],
      progress: []
    };

    return NextResponse.json(progress);
  } catch (error) {
    console.error('Error in progress API:', error);
    return NextResponse.json(
      { error: 'Failed to retrieve progress data' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { userId, lessonId, exerciseId, score, completed } = body;

    // Update mock progress data
    if (!mockProgressData[userId]) {
      mockProgressData[userId] = {
        userId,
        lessonsCompleted: 0,
        exercisesCompleted: 0,
        currentStreak: 0,
        totalTimeSpent: 0,
        achievements: [],
        progress: []
      };
    }

    const userProgress = mockProgressData[userId];

    if (lessonId && completed) {
      // Update lesson progress
      const existingLesson = userProgress.progress.find((p: any) => p.lesson === lessonId);
      if (existingLesson) {
        existingLesson.completed = completed;
        existingLesson.score = score;
      } else {
        userProgress.progress.push({ lesson: lessonId, completed, score });
      }
      userProgress.lessonsCompleted += 1;
    }

    if (exerciseId && score !== undefined) {
      userProgress.exercisesCompleted += 1;
    }

    userProgress.lastUpdated = new Date().toISOString();

    return NextResponse.json({
      message: 'Progress updated successfully',
      progress: userProgress
    });
  } catch (error) {
    console.error('Error in progress API:', error);
    return NextResponse.json(
      { error: 'Failed to update progress' },
      { status: 500 }
    );
  }
}