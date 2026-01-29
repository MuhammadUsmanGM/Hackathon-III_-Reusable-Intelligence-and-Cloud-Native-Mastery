'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { FiBook, FiCode, FiMessageSquare, FiUser, FiSettings, FiSun, FiMoon, FiSend, FiRefreshCw, FiPlay } from 'react-icons/fi';

// Dynamically import Monaco Editor to avoid SSR issues
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), {
  ssr: false,
  loading: () => <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">Loading editor...</div>
});

export default function Home() {
  const [code, setCode] = useState<string>('// Welcome to LearnFlow\n// Write your Python code here\nprint("Hello, World!")');
  const [output, setOutput] = useState<string>('Click "Run" to execute your code');
  const [input, setInput] = useState<string>('');
  const [chatMessages, setChatMessages] = useState<{role: string, content: string}[]>([
    {role: 'assistant', content: 'Hello! I\'m your Python tutor. How can I help you today?'}
  ]);
  const [currentMessage, setCurrentMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');

  // Toggle theme
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  // Handle sending messages to AI
  const handleSendMessage = async () => {
    if (!currentMessage.trim()) return;

    const newMessage = { role: 'user', content: currentMessage };
    setChatMessages(prev => [...prev, newMessage]);
    setCurrentMessage('');
    setIsLoading(true);

    try {
      // Simulate API call to backend
      setTimeout(() => {
        const aiResponse = {
          role: 'assistant',
          content: `I received your message: "${currentMessage}". As your Python tutor, I can help explain concepts, debug code, or provide exercises.`
        };
        setChatMessages(prev => [...prev, aiResponse]);
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      setChatMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }]);
      setIsLoading(false);
    }
  };

  // Handle running code
  const handleRunCode = () => {
    setOutput('Running your code...\n\n// This would connect to the backend to execute Python code securely');
  };

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-emerald-50 text-gray-900'} transition-colors duration-200`}>
      {/* Header */}
      <header className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-emerald-600'} shadow-lg`}>
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <FiBook className="text-white text-xl" />
            <h1 className="text-xl font-bold text-white">LearnFlow</h1>
          </div>
          <nav className="hidden md:block">
            <ul className="flex space-x-6">
              <li><Link href="/" className="text-white hover:text-emerald-200 transition-colors">Home</Link></li>
              <li><Link href="/lessons" className="text-white hover:text-emerald-200 transition-colors">Lessons</Link></li>
              <li><Link href="/exercises" className="text-white hover:text-emerald-200 transition-colors">Exercises</Link></li>
              <li><Link href="/dashboard" className="text-white hover:text-emerald-200 transition-colors">Dashboard</Link></li>
            </ul>
          </nav>
          <button
            onClick={toggleTheme}
            className={`p-2 rounded-full ${theme === 'dark' ? 'bg-gray-700 text-yellow-300' : 'bg-emerald-500 text-gray-800'}`}
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <FiSun /> : <FiMoon />}
          </button>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 flex flex-col lg:flex-row gap-6">
        {/* Main Content Area */}
        <main className="flex-1">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Code Editor Section */}
            <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-4`}>
              <div className="flex justify-between items-center mb-3">
                <h2 className="text-lg font-semibold text-emerald-500">Code Editor</h2>
                <button
                  onClick={handleRunCode}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg flex items-center"
                >
                  <FiPlay className="mr-2" /> Run Code
                </button>
              </div>
              <div className="border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden h-80">
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
              <div className="mt-3">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Program input (if required)"
                  className={`w-full p-2 border rounded ${theme === 'dark' ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-300'}`}
                  rows={2}
                />
              </div>
            </div>

            {/* Output Console */}
            <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-4`}>
              <h2 className="text-lg font-semibold text-emerald-500 mb-3">Output</h2>
              <div className={`h-80 p-3 font-mono text-sm rounded border ${theme === 'dark' ? 'bg-gray-900 border-gray-700' : 'bg-gray-100 border-gray-300'} overflow-auto`}>
                <pre>{output}</pre>
              </div>
            </div>
          </div>

          {/* AI Tutor Chat */}
          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-4`}>
            <div className="flex items-center mb-3">
              <FiMessageSquare className="text-emerald-500 mr-2" />
              <h2 className="text-lg font-semibold text-emerald-500">AI Tutor Assistant</h2>
              <button
                onClick={() => setChatMessages([{role: 'assistant', content: 'Hello! I\'m your Python tutor. How can I help you today?'}])}
                className="ml-auto flex items-center text-sm bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 px-3 py-1 rounded"
              >
                <FiRefreshCw className="mr-1" /> Clear
              </button>
            </div>

            <div className={`h-64 overflow-y-auto mb-3 p-3 rounded border ${theme === 'dark' ? 'bg-gray-900 border-gray-700' : 'bg-gray-100 border-gray-300'}`}>
              {chatMessages.map((msg, index) => (
                <div
                  key={index}
                  className={`mb-3 p-2 rounded-lg max-w-[80%] ${
                    msg.role === 'user'
                      ? 'bg-emerald-500 text-white ml-auto'
                      : `${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`
                  }`}
                >
                  {msg.content}
                </div>
              ))}
              {isLoading && (
                <div className={`p-2 rounded-lg ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-emerald-500 mr-2"></div>
                    <span>Thinking...</span>
                  </div>
                </div>
              )}
            </div>

            <div className="flex">
              <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask your Python tutor..."
                className={`flex-1 p-2 border rounded-l-lg ${theme === 'dark' ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-300'}`}
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading}
                className="bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white px-4 py-2 rounded-r-lg flex items-center"
              >
                <FiSend />
              </button>
            </div>
          </div>
        </main>

        {/* Sidebar */}
        <aside className="lg:w-80">
          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-4 mb-6`}>
            <h2 className="text-lg font-semibold text-emerald-500 mb-3">Learning Progress</h2>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Python Basics</span>
                  <span>75%</span>
                </div>
                <div className={`w-full h-2 rounded-full ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                  <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '75%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Control Flow</span>
                  <span>40%</span>
                </div>
                <div className={`w-full h-2 rounded-full ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                  <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '40%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Functions</span>
                  <span>20%</span>
                </div>
                <div className={`w-full h-2 rounded-full ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                  <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '20%' }}></div>
                </div>
              </div>
            </div>
          </div>

          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-4`}>
            <h2 className="text-lg font-semibold text-emerald-500 mb-3">Quick Actions</h2>
            <div className="space-y-2">
              <button className="w-full text-left p-2 hover:bg-emerald-100 dark:hover:bg-gray-700 rounded flex items-center">
                <FiBook className="mr-2 text-emerald-500" /> Start New Lesson
              </button>
              <button className="w-full text-left p-2 hover:bg-emerald-100 dark:hover:bg-gray-700 rounded flex items-center">
                <FiCode className="mr-2 text-emerald-500" /> Practice Exercise
              </button>
              <button className="w-full text-left p-2 hover:bg-emerald-100 dark:hover:bg-gray-700 rounded flex items-center">
                <FiSettings className="mr-2 text-emerald-500" /> Settings
              </button>
            </div>
          </div>
        </aside>
      </div>

      <footer className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-emerald-700'} text-white py-6 mt-8`}>
        <div className="container mx-auto px-4 text-center">
          <p>© 2026 LearnFlow - AI-Powered Python Tutoring Platform</p>
        </div>
      </footer>
    </div>
  );
}
