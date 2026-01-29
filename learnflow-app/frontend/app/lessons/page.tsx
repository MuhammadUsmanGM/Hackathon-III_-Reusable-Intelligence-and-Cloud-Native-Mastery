'use client';

import { useState } from 'react';
import Link from 'next/link';
import { FiBook, FiPlay, FiCheck, FiArrowLeft, FiSun, FiMoon } from 'react-icons/fi';

export default function LessonsPage() {
  const [selectedLesson, setSelectedLesson] = useState<number | null>(null);
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const lessons = [
    {
      id: 1,
      title: "Python Basics",
      description: "Learn the fundamentals of Python programming",
      duration: "15 min",
      completed: true,
      content: `
# Python Basics

Python is a high-level, interpreted programming language known for its simplicity and readability.

## Variables and Data Types

In Python, you don't need to declare variable types explicitly:

\`\`\`python
name = "Alice"  # String
age = 25        # Integer
height = 5.6    # Float
is_student = True  # Boolean
\`\`\`

## Basic Operators

Python supports arithmetic operators like +, -, *, /, and %:

\`\`\`python
sum = 5 + 3
product = 4 * 6
remainder = 17 % 5
\`\`\`

## Try it yourself!

Write a program that prints your name and age.
      `
    },
    {
      id: 2,
      title: "Control Flow",
      description: "Master if statements, loops, and conditionals",
      duration: "20 min",
      completed: false,
      content: `
# Control Flow

Control flow statements allow you to execute different blocks of code based on certain conditions.

## If Statements

Use if, elif, and else to make decisions:

\`\`\`python
age = 18

if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager")
else:
    print("You are a child")
\`\`\`

## Loops

Python has two main types of loops: for and while.

### For Loop
\`\`\`python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
\`\`\`

### While Loop
\`\`\`python
count = 0
while count < 5:
    print(count)
    count += 1
\`\`\`

## Practice

Write a program that prints all even numbers from 1 to 20.
      `
    },
    {
      id: 3,
      title: "Functions",
      description: "Define and use functions to organize your code",
      duration: "25 min",
      completed: false,
      content: `
# Functions

Functions are reusable blocks of code that perform a specific task.

## Defining Functions

Use the def keyword to define a function:

\`\`\`python
def greet(name):
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")
print(message)  # Output: Hello, Alice!
\`\`\`

## Functions with Multiple Parameters

\`\`\`python
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(result)  # Output: 8
\`\`\`

## Default Parameters

\`\`\`python
def introduce(name, age=18):
    return f"My name is {name} and I am {age} years old."

print(introduce("Bob"))        # My name is Bob and I am 18 years old.
print(introduce("Carol", 22))  # My name is Carol and I am 22 years old.
\`\`\`

## Challenge

Write a function that takes a list of numbers and returns the largest number.
      `
    }
  ];

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-emerald-50 text-gray-900'} transition-colors duration-200`}>
      {/* Header */}
      <header className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-emerald-600'} shadow-lg`}>
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="flex items-center space-x-2">
            <FiBook className="text-white text-xl" />
            <h1 className="text-xl font-bold text-white">LearnFlow</h1>
          </Link>
          <button
            onClick={toggleTheme}
            className={`p-2 rounded-full ${theme === 'dark' ? 'bg-gray-700 text-yellow-300' : 'bg-emerald-500 text-gray-800'}`}
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <FiSun /> : <FiMoon />}
          </button>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center mb-6">
          <Link href="/" className="flex items-center text-emerald-500 hover:text-emerald-600 mr-4">
            <FiArrowLeft className="mr-1" /> Back to Dashboard
          </Link>
          <h1 className="text-3xl font-bold text-emerald-600">Python Curriculum</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Lessons List */}
          <div className={`lg:col-span-1 ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
            <h2 className="text-xl font-semibold text-emerald-500 mb-4">Lessons</h2>
            <div className="space-y-3">
              {lessons.map((lesson) => (
                <div
                  key={lesson.id}
                  className={`p-4 rounded-lg cursor-pointer transition-all ${
                    selectedLesson === lesson.id
                      ? 'bg-emerald-500 text-white'
                      : theme === 'dark'
                        ? 'bg-gray-700 hover:bg-gray-600'
                        : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                  onClick={() => setSelectedLesson(lesson.id)}
                >
                  <div className="flex items-center">
                    {lesson.completed ? (
                      <FiCheck className="text-green-500 mr-2" />
                    ) : (
                      <FiPlay className="text-emerald-500 mr-2" />
                    )}
                    <div>
                      <h3 className="font-medium">{lesson.title}</h3>
                      <p className="text-sm opacity-80">{lesson.description}</p>
                      <p className="text-xs opacity-60 mt-1">{lesson.duration}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Lesson Content */}
          <div className="lg:col-span-2">
            {selectedLesson ? (
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
                <div className="flex justify-between items-start mb-4">
                  <h2 className="text-2xl font-bold text-emerald-500">
                    {lessons.find(l => l.id === selectedLesson)?.title}
                  </h2>
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    theme === 'dark' ? 'bg-gray-700' : 'bg-emerald-100 text-emerald-800'
                  }`}>
                    {lessons.find(l => l.id === selectedLesson)?.duration}
                  </span>
                </div>

                <div className="prose prose-emerald max-w-none">
                  {lessons.find(l => l.id === selectedLesson)?.content.split('\n').map((line, idx) => {
                    if (line.startsWith('# ')) {
                      return <h1 key={idx} className="text-2xl font-bold mt-6 mb-4">{line.substring(2)}</h1>;
                    } else if (line.startsWith('## ')) {
                      return <h2 key={idx} className="text-xl font-semibold mt-5 mb-3">{line.substring(3)}</h2>;
                    } else if (line.startsWith('### ')) {
                      return <h3 key={idx} className="text-lg font-medium mt-4 mb-2">{line.substring(4)}</h3>;
                    } else if (line.startsWith('```')) {
                      if (!line.includes('```python')) {
                        return <pre key={idx} className="bg-gray-800 text-gray-100 p-4 rounded-lg my-3 overflow-x-auto"><code>{line}</code></pre>;
                      }
                      // This is a simplified representation - in a real app, we'd properly parse code blocks
                      return null;
                    } else if (line.trim() === '') {
                      return <br key={idx} />;
                    } else {
                      return <p key={idx} className="mb-3">{line}</p>;
                    }
                  })}
                </div>

                <div className="mt-8 flex justify-end">
                  <button className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg flex items-center">
                    <FiPlay className="mr-2" /> Start Coding
                  </button>
                </div>
              </div>
            ) : (
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-12 text-center`}>
                <FiBook className="mx-auto text-emerald-500 text-5xl mb-4" />
                <h3 className="text-xl font-semibold text-emerald-500 mb-2">Select a Lesson</h3>
                <p className={`${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                  Choose a lesson from the list to start learning
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      <footer className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-emerald-700'} text-white py-6 mt-8`}>
        <div className="container mx-auto px-4 text-center">
          <p>© 2026 LearnFlow - AI-Powered Python Tutoring Platform</p>
        </div>
      </footer>
    </div>
  );
}