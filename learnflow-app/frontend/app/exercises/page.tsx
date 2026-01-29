'use client';

import { useState } from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { FiBook, FiCode, FiCheck, FiX, FiStar, FiClock, FiArrowLeft, FiSun, FiMoon, FiPlay } from 'react-icons/fi';

// Dynamically import Monaco Editor to avoid SSR issues
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), {
  ssr: false,
  loading: () => <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">Loading editor...</div>
});

export default function ExercisesPage() {
  const [selectedExercise, setSelectedExercise] = useState<number | null>(null);
  const [code, setCode] = useState<string>('');
  const [output, setOutput] = useState<string>('');
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');
  const [attempts, setAttempts] = useState<number>(0);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const exercises = [
    {
      id: 1,
      title: "Print Statement",
      difficulty: "Beginner",
      description: "Write a program that prints 'Hello, World!'",
      starterCode: "print('')  # Fill in the string to print",
      solution: "print('Hello, World!')",
      hint: "Use the print() function with a string inside",
      completed: true
    },
    {
      id: 2,
      title: "Variable Assignment",
      difficulty: "Beginner",
      description: "Create a variable called 'name' and assign it your name, then print it",
      starterCode: "# Create a variable called 'name' and assign your name to it\n\n# Print the variable\n",
      solution: "name = 'Alice'\nprint(name)",
      hint: "Use the = operator to assign a value to a variable",
      completed: false
    },
    {
      id: 3,
      title: "Even or Odd",
      difficulty: "Intermediate",
      description: "Write a program that takes a number and prints 'even' if it's even, 'odd' if it's odd",
      starterCode: "num = int(input('Enter a number: '))\n\n# Check if the number is even or odd\n",
      solution: "num = int(input('Enter a number: '))\nif num % 2 == 0:\n    print('even')\nelse:\n    print('odd')",
      hint: "Use the modulo operator (%) to check divisibility by 2",
      completed: false
    }
  ];

  const handleRunCode = () => {
    // Simulate code execution
    setOutput('Running your code...\n\n// This would connect to the backend to execute Python code securely');

    // Increment attempts
    setAttempts(prev => prev + 1);
  };

  const handleSubmit = () => {
    // Simulate checking solution
    setIsCorrect(Math.random() > 0.5); // Random for demo

    if (isCorrect) {
      setOutput('Success! Your solution is correct.');
    } else {
      setOutput('Not quite right. Try again!');
    }
  };

  const selectedExerciseData = selectedExercise ? exercises.find(e => e.id === selectedExercise) : null;

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-emerald-50 text-gray-900'} transition-colors duration-200`}>
      {/* Header */}
      <header className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-emerald-600'} shadow-lg`}>
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="flex items-center space-x-2">
            <FiCode className="text-white text-xl" />
            <h1 className="text-xl font-bold text-white">LearnFlow Exercises</h1>
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
          <h1 className="text-3xl font-bold text-emerald-600">Practice Exercises</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Exercises List */}
          <div className={`lg:col-span-1 ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
            <h2 className="text-xl font-semibold text-emerald-500 mb-4">Exercises</h2>
            <div className="space-y-3">
              {exercises.map((exercise) => (
                <div
                  key={exercise.id}
                  className={`p-4 rounded-lg cursor-pointer transition-all ${
                    selectedExercise === exercise.id
                      ? 'bg-emerald-500 text-white'
                      : theme === 'dark'
                        ? 'bg-gray-700 hover:bg-gray-600'
                        : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                  onClick={() => {
                    setSelectedExercise(exercise.id);
                    setCode(exercise.starterCode);
                    setOutput('');
                    setIsCorrect(null);
                  }}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-medium">{exercise.title}</h3>
                      <p className="text-sm opacity-80">{exercise.description}</p>
                      <div className="flex items-center mt-2">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          exercise.difficulty === 'Beginner'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                        }`}>
                          {exercise.difficulty}
                        </span>
                      </div>
                    </div>
                    {exercise.completed && (
                      <FiCheck className="text-green-500 text-xl" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Exercise Content and Editor */}
          <div className="lg:col-span-2">
            {selectedExerciseData ? (
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-2xl font-bold text-emerald-500">{selectedExerciseData.title}</h2>
                    <p className="text-gray-500 dark:text-gray-400">{selectedExerciseData.description}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    selectedExerciseData.difficulty === 'Beginner'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                  }`}>
                    {selectedExerciseData.difficulty}
                  </span>
                </div>

                <div className="mb-6">
                  <h3 className="font-semibold text-lg mb-2">Instructions:</h3>
                  <p>{selectedExerciseData.description}</p>

                  <div className="mt-4 flex items-center text-sm text-gray-500 dark:text-gray-400">
                    <FiClock className="mr-1" />
                    <span>Hints available: {selectedExerciseData.hint ? 'Yes' : 'No'}</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                  <div>
                    <h3 className="font-semibold mb-2">Code Editor</h3>
                    <div className="border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden h-64">
                      <MonacoEditor
                        height="100%"
                        language="python"
                        value={code}
                        onChange={(value) => setCode(value || '')}
                        theme={theme === 'dark' ? 'vs-dark' : 'light'}
                        options={{
                          minimap: { enabled: false },
                          fontSize: 14,
                          scrollBeyondLastLine: false,
                          automaticLayout: true,
                        }}
                      />
                    </div>
                    <div className="mt-3 flex space-x-3">
                      <button
                        onClick={handleRunCode}
                        className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg flex items-center"
                      >
                        <FiPlay className="mr-2" /> Run Code
                      </button>
                      <button
                        onClick={handleSubmit}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
                      >
                        Submit
                      </button>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-semibold mb-2">Output</h3>
                    <div className={`h-64 p-3 font-mono text-sm rounded border ${theme === 'dark' ? 'bg-gray-900 border-gray-700' : 'bg-gray-100 border-gray-300'} overflow-auto`}>
                      <pre>{output || '// Output will appear here after running your code'}</pre>
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  <h3 className="font-semibold mb-2">Hint</h3>
                  <div className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'}`}>
                    <p>{selectedExerciseData.hint}</p>
                  </div>
                </div>

                {isCorrect !== null && (
                  <div className={`mt-4 p-4 rounded-lg flex items-center ${
                    isCorrect ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                  }`}>
                    {isCorrect ? (
                      <>
                        <FiCheck className="mr-2 text-xl" /> Great job! Your solution is correct.
                      </>
                    ) : (
                      <>
                        <FiX className="mr-2 text-xl" /> Not quite right. Review the hint and try again.
                      </>
                    )}
                  </div>
                )}

                <div className="mt-4 flex justify-between items-center">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Attempts: {attempts}
                  </div>
                  <button className="text-emerald-500 hover:text-emerald-600 flex items-center">
                    <FiStar className="mr-1" /> Save to Favorites
                  </button>
                </div>
              </div>
            ) : (
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-12 text-center`}>
                <FiCode className="mx-auto text-emerald-500 text-5xl mb-4" />
                <h3 className="text-xl font-semibold text-emerald-500 mb-2">Select an Exercise</h3>
                <p className={`${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                  Choose an exercise from the list to start practicing
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