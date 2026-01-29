'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { FiBook, FiCode, FiBarChart2, FiClock, FiAward, FiUser, FiSun, FiMoon, FiPlay, FiCheck } from 'react-icons/fi';

export default function DashboardPage() {
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');
  const [stats, setStats] = useState({
    lessonsCompleted: 5,
    exercisesCompleted: 12,
    currentStreak: 3,
    totalTime: 120
  });

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const achievements = [
    { id: 1, title: 'First Steps', description: 'Complete your first lesson', icon: <FiBook />, earned: true },
    { id: 2, title: 'Bug Finder', description: 'Successfully debug 5 exercises', icon: <FiCode />, earned: true },
    { id: 3, title: 'Code Warrior', description: 'Complete 10 exercises', icon: <FiPlay />, earned: true },
    { id: 4, title: 'Consistency Master', description: '7-day learning streak', icon: <FiClock />, earned: false },
    { id: 5, title: 'Python Pro', description: 'Complete all basic lessons', icon: <FiAward />, earned: false }
  ];

  const recentActivity = [
    { id: 1, type: 'lesson', title: 'Python Basics', time: '2 hours ago', completed: true },
    { id: 2, type: 'exercise', title: 'Variables Exercise', time: '1 day ago', completed: true },
    { id: 3, type: 'lesson', title: 'Control Flow', time: '2 days ago', completed: true },
    { id: 4, type: 'exercise', title: 'If-Else Exercise', time: '3 days ago', completed: true }
  ];

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-emerald-50 text-gray-900'} transition-colors duration-200`}>
      {/* Header */}
      <header className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-emerald-600'} shadow-lg`}>
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <FiBarChart2 className="text-white text-xl" />
            <h1 className="text-xl font-bold text-white">LearnFlow Dashboard</h1>
          </div>
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
            <FiUser className="mr-1" /> Profile
          </Link>
          <h1 className="text-3xl font-bold text-emerald-600">Your Learning Dashboard</h1>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6 flex items-center`}>
            <div className="bg-emerald-100 dark:bg-emerald-900/30 p-3 rounded-lg mr-4">
              <FiBook className="text-emerald-500 text-2xl" />
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400 text-sm">Lessons Completed</p>
              <p className="text-2xl font-bold">{stats.lessonsCompleted}</p>
            </div>
          </div>

          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6 flex items-center`}>
            <div className="bg-emerald-100 dark:bg-emerald-900/30 p-3 rounded-lg mr-4">
              <FiCode className="text-emerald-500 text-2xl" />
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400 text-sm">Exercises Done</p>
              <p className="text-2xl font-bold">{stats.exercisesCompleted}</p>
            </div>
          </div>

          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6 flex items-center`}>
            <div className="bg-emerald-100 dark:bg-emerald-900/30 p-3 rounded-lg mr-4">
              <FiClock className="text-emerald-500 text-2xl" />
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400 text-sm">Current Streak</p>
              <p className="text-2xl font-bold">{stats.currentStreak} days</p>
            </div>
          </div>

          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6 flex items-center`}>
            <div className="bg-emerald-100 dark:bg-emerald-900/30 p-3 rounded-lg mr-4">
              <FiBarChart2 className="text-emerald-500 text-2xl" />
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400 text-sm">Total Time</p>
              <p className="text-2xl font-bold">{stats.totalTime} min</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Progress Overview */}
          <div className={`lg:col-span-2 ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
            <h2 className="text-xl font-semibold text-emerald-500 mb-4">Learning Progress</h2>

            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-1">
                  <span>Python Fundamentals</span>
                  <span>75%</span>
                </div>
                <div className={`w-full h-3 rounded-full ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                  <div className="bg-emerald-500 h-3 rounded-full" style={{ width: '75%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span>Control Flow</span>
                  <span>40%</span>
                </div>
                <div className={`w-full h-3 rounded-full ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                  <div className="bg-emerald-500 h-3 rounded-full" style={{ width: '40%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span>Functions</span>
                  <span>20%</span>
                </div>
                <div className={`w-full h-3 rounded-full ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                  <div className="bg-emerald-500 h-3 rounded-full" style={{ width: '20%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span>OOP Concepts</span>
                  <span>5%</span>
                </div>
                <div className={`w-full h-3 rounded-full ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                  <div className="bg-emerald-500 h-3 rounded-full" style={{ width: '5%' }}></div>
                </div>
              </div>
            </div>

            <div className="mt-6">
              <h3 className="font-medium text-emerald-500 mb-3">Continue Learning</h3>
              <div className="flex space-x-3">
                <button className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg flex items-center">
                  <FiPlay className="mr-2" /> Continue Lesson
                </button>
                <button className="border border-emerald-500 text-emerald-500 hover:bg-emerald-50 dark:hover:bg-gray-700 px-4 py-2 rounded-lg flex items-center">
                  <FiCode className="mr-2" /> Practice Exercise
                </button>
              </div>
            </div>
          </div>

          {/* Achievements & Recent Activity */}
          <div className="space-y-6">
            {/* Achievements */}
            <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
              <h2 className="text-xl font-semibold text-emerald-500 mb-4">Achievements</h2>
              <div className="space-y-3">
                {achievements.map((achievement) => (
                  <div
                    key={achievement.id}
                    className={`flex items-center p-3 rounded-lg ${
                      achievement.earned
                        ? 'bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800'
                        : `${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'}`
                    }`}
                  >
                    <div className={`p-2 rounded-lg mr-3 ${
                      achievement.earned
                        ? 'bg-emerald-100 dark:bg-emerald-800 text-emerald-500'
                        : 'bg-gray-200 dark:bg-gray-600 text-gray-400'
                    }`}>
                      {achievement.icon}
                    </div>
                    <div>
                      <h4 className={`font-medium ${
                        achievement.earned ? 'text-emerald-700 dark:text-emerald-300' : ''
                      }`}>{achievement.title}</h4>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{achievement.description}</p>
                    </div>
                    {achievement.earned && (
                      <FiCheck className="ml-auto text-emerald-500" />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Activity */}
            <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
              <h2 className="text-xl font-semibold text-emerald-500 mb-4">Recent Activity</h2>
              <div className="space-y-3">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-center p-3 rounded-lg hover:bg-emerald-50 dark:hover:bg-gray-700">
                    <div className="bg-emerald-100 dark:bg-emerald-900/30 p-2 rounded-lg mr-3">
                      {activity.type === 'lesson' ? <FiBook className="text-emerald-500" /> : <FiCode className="text-emerald-500" />}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium">{activity.title}</h4>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{activity.time}</p>
                    </div>
                    {activity.completed && (
                      <FiCheck className="text-emerald-500" />
                    )}
                  </div>
                ))}
              </div>
            </div>
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