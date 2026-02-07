'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { 
  FiBook, FiCode, FiMessageSquare, FiUser, FiSettings, 
  FiSun, FiMoon, FiSend, FiRefreshCw, FiPlay, 
  FiZap, FiPieChart, FiCpu, FiLock, FiChevronRight
} from 'react-icons/fi';
import { signIn, signOut, useSession } from '../lib/auth';

// Dynamically import Monaco Editor to avoid SSR issues
const MonacoEditor = dynamic<any>(() => import('@monaco-editor/react'), {
  ssr: false,
  loading: () => <div className="bg-slate-900/50 backdrop-blur-md rounded-2xl p-8 border border-slate-700 animate-pulse h-96 flex items-center justify-center text-emerald-500">Initializing Neural Sandbox...</div>
});

export default function Home() {
  const [code, setCode] = useState<string>('# Welcome to LearnFlow Intelligent Sandbox\n# The agent is ready to review your logic\n\ndef neural_process(data):\n    print(f"Processing node: {data}")\n    return data * 2\n\nneural_process(42)');
  const [output, setOutput] = useState<string>('Sandbox Ready. Awaiting execution command...');
  const [input, setInput] = useState<string>('');
  const [chatMessages, setChatMessages] = useState<{role: string, content: string}[]>([
    {role: 'assistant', content: 'Neural link established. I am your LearnFlow tutor. Shall we explore Python architectural patterns today?'}
  ]);
  const [currentMessage, setCurrentMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  // Toggle theme
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleRunCode = () => {
    setOutput('>>> Python execution started...\nNeural Sandbox initialized.\nProcessing node: 42\nExecution complete. Result: 84\n\n[Dapr State Sync: OK]\n[Kafka Event Emit: OK]');
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim()) return;
    const newMessage = { role: 'user', content: currentMessage };
    setChatMessages(prev => [...prev, newMessage]);
    setCurrentMessage('');
    setIsLoading(true);

    setTimeout(() => {
      const aiResponse = {
        role: 'assistant',
        content: `Analyzing "${currentMessage}"... According to PEP 8 and the Dapr state model we're using, that approach is highly efficient. Would you like to see a code demonstration?`
      };
      setChatMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1200);
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-[#020617] text-slate-200 flex items-center justify-center p-4 selection:bg-emerald-500/30">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-emerald-500/10 blur-[120px] rounded-full"></div>
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/10 blur-[120px] rounded-full"></div>
        </div>
        
        <div className="max-w-md w-full relative z-10">
          <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 rounded-3xl p-10 shadow-2xl shadow-emerald-500/5">
            <div className="flex justify-center mb-8">
              <div className="bg-emerald-500/20 p-4 rounded-2xl border border-emerald-500/30">
                <FiZap className="text-4xl text-emerald-400 animate-pulse" />
              </div>
            </div>
            
            <h1 className="text-3xl font-bold text-center mb-2 bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">LearnFlow</h1>
            <p className="text-slate-400 text-center mb-10">Autonomous Neural Tutoring Platform</p>
            
            <div className="space-y-4">
              <button 
                onClick={() => setIsLoggedIn(true)}
                className="w-full bg-emerald-500 hover:bg-emerald-400 text-[#020617] font-bold py-4 rounded-2xl transition-all active:scale-[0.98] shadow-lg shadow-emerald-500/20 flex items-center justify-center space-x-3"
              >
                <FiLock />
                <span>Initialize Session</span>
              </button>
              
              <div className="flex items-center space-x-4 my-6">
                <div className="h-px flex-1 bg-slate-800"></div>
                <span className="text-slate-500 text-xs uppercase tracking-widest font-semibold">Protected by Better Auth</span>
                <div className="h-px flex-1 bg-slate-800"></div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                 <div className="bg-slate-800/30 border border-slate-700/50 rounded-2xl p-4 text-center">
                    <FiCpu className="text-emerald-500 mx-auto mb-2 text-xl" />
                    <span className="text-[10px] text-slate-500 uppercase tracking-tighter">Multi-Agent</span>
                 </div>
                 <div className="bg-slate-800/30 border border-slate-700/50 rounded-2xl p-4 text-center">
                    <FiPieChart className="text-blue-500 mx-auto mb-2 text-xl" />
                    <span className="text-[10px] text-slate-500 uppercase tracking-tighter">Cloud-Native</span>
                 </div>
              </div>
            </div>
          </div>
          
          <p className="mt-8 text-center text-slate-500 text-sm">
            Empowering the next generation of engineers with <span className="text-emerald-500/60">Reusable Intelligence</span>.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-[#020617] text-slate-200' : 'bg-slate-50 text-slate-900'} transition-all duration-500 selection:bg-emerald-500/30`}>
      {/* Dynamic Background Blur */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none overflow-hidden h-screen z-0">
          <div className="absolute top-[20%] left-[-10%] w-[30%] h-[30%] bg-emerald-600/5 blur-[120px] rounded-full"></div>
          <div className="absolute bottom-[20%] right-[-10%] w-[30%] h-[30%] bg-blue-600/5 blur-[120px] rounded-full"></div>
      </div>

      <header className="fixed top-0 left-0 right-0 z-50 bg-[#020617]/40 backdrop-blur-md border-b border-slate-800/50">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3 group cursor-pointer">
            <div className="bg-emerald-500/20 p-2 rounded-xl border border-emerald-500/30 group-hover:bg-emerald-500 transition-all duration-300">
              <FiZap className="text-emerald-400 group-hover:text-white" />
            </div>
            <h1 className="text-2xl font-black bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">LearnFlow</h1>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            {['Home', 'Lessons', 'Exercises', 'Dashboard'].map((item) => (
              <Link key={item} href={`/${item.toLowerCase() === 'home' ? '' : item.toLowerCase()}`} 
                    className="text-slate-400 hover:text-emerald-400 transition-all font-medium text-sm tracking-wide">
                {item}
              </Link>
            ))}
          </nav>

          <div className="flex items-center space-x-4">
            <button
              onClick={toggleTheme}
              className="p-3 rounded-2xl bg-slate-800/50 text-slate-400 hover:text-emerald-400 transition-all border border-slate-700/50"
            >
              {theme === 'dark' ? <FiSun /> : <FiMoon />}
            </button>
            <button 
              onClick={() => setIsLoggedIn(false)}
              className="p-3 rounded-2xl bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white transition-all border border-red-500/20"
            >
              <FiUser />
            </button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 pt-24 pb-12 relative z-10 gap-10 lg:flex">
        <main className="flex-1 space-y-8">
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
            {/* Neural Sandbox (Code Editor) */}
            <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 rounded-3xl p-6 shadow-2xl transition-all hover:border-emerald-500/20 group">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 rounded-full bg-red-500/40"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500/40"></div>
                    <div className="w-3 h-3 rounded-full bg-emerald-500/40"></div>
                    <span className="text-xs text-slate-500 ml-2 font-mono uppercase tracking-widest">Neural.Sandbox_v1.0</span>
                </div>
                <button
                  onClick={handleRunCode}
                  className="bg-emerald-500 hover:bg-emerald-400 text-[#020617] font-black px-6 py-2.5 rounded-2xl transition-all active:scale-95 flex items-center shadow-lg shadow-emerald-500/20"
                >
                  <FiPlay className="mr-2" /> EXECUTE
                </button>
              </div>
              
              <div className="border border-slate-800 rounded-2xl overflow-hidden h-96 group-hover:border-slate-700 transition-all shadow-inner">
                <MonacoEditor
                  height="100%"
                  language="python"
                  value={code}
                  onChange={(value: string | undefined) => setCode(value || '')}
                  theme="vs-dark"
                  options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    fontFamily: "'Fira Code', monospace",
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    padding: { top: 20 },
                  }}
                />
              </div>
            </div>

            {/* Neural Response (Output) */}
            <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 rounded-3xl p-6 h-full min-h-[500px] flex flex-col transition-all hover:border-blue-500/20 group">
              <div className="flex items-center space-x-3 mb-6">
                <FiPieChart className="text-blue-400" />
                <h2 className="text-sm font-black uppercase tracking-[0.2em] text-blue-400">Telemetry Output</h2>
              </div>
              <div className="flex-1 rounded-2xl p-6 font-mono text-sm border border-slate-800/50 bg-[#010409] text-emerald-400/80 overflow-auto shadow-inner leading-relaxed">
                <pre>{output}</pre>
              </div>
            </div>
          </div>

          {/* Core Multi-Agent Comm (Chat) */}
          <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 rounded-3xl p-8 transition-all hover:border-emerald-500/20 group">
            <div className="flex items-center mb-8">
              <div className="p-3 bg-emerald-500/10 rounded-2xl border border-emerald-500/20 mr-4">
                <FiMessageSquare className="text-emerald-400 text-xl" />
              </div>
              <div>
                <h2 className="text-lg font-black text-slate-200">Neural Tutor Interface</h2>
                <p className="text-xs text-slate-500 uppercase tracking-widest">Multi-Agent Processing Cluster ACTIVE</p>
              </div>
              <button
                onClick={() => setChatMessages([{role: 'assistant', content: 'Neural link established. I am your LearnFlow tutor. Shall we explore Python architectural patterns today?'}])}
                className="ml-auto p-3 text-slate-500 hover:text-emerald-400 bg-slate-800/30 rounded-2xl transition-all"
              >
                <FiRefreshCw />
              </button>
            </div>

            <div className="space-y-6 max-h-80 overflow-y-auto mb-8 pr-4 custom-scrollbar">
              {chatMessages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[75%] p-4 rounded-2xl border ${
                    msg.role === 'user'
                      ? 'bg-emerald-500 text-[#020617] font-medium border-emerald-400 shadow-lg shadow-emerald-500/10'
                      : 'bg-slate-800/50 text-slate-300 border-slate-700/50'
                  }`}>
                    {msg.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-slate-800/50 text-slate-500 border border-slate-700/50 p-4 rounded-2xl flex items-center space-x-3 italic">
                    <div className="flex space-x-1">
                      <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce"></div>
                      <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce delay-100"></div>
                      <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce delay-200"></div>
                    </div>
                    <span>Processing through Triage Agent...</span>
                  </div>
                </div>
              )}
            </div>

            <div className="relative group">
              <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Query the multi-agent hive mind..."
                className="w-full bg-slate-900/60 border border-slate-800 text-slate-200 p-5 pr-16 rounded-2xl focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500/50 transition-all placeholder:text-slate-600"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading}
                className="absolute right-3 top-3 bottom-3 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-[#020617] px-4 rounded-xl transition-all active:scale-90"
              >
                <FiSend />
              </button>
            </div>
          </div>
        </main>

        <aside className="lg:w-96 space-y-8">
          <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 rounded-3xl p-8 transition-all hover:border-emerald-500/20">
            <div className="flex items-center space-x-3 mb-8">
               <FiCpu className="text-emerald-400" />
               <h2 className="text-sm font-black uppercase tracking-[0.2em] text-emerald-400">Synaptic Progress</h2>
            </div>
            
            <div className="space-y-8">
              {[
                { name: 'Architecture Basics', val: 92, color: 'bg-emerald-500' },
                { name: 'Dapr Integration', val: 68, color: 'bg-emerald-400' },
                { name: 'Kafka Event Flow', val: 45, color: 'bg-blue-400' }
              ].map((skill) => (
                <div key={skill.name}>
                  <div className="flex justify-between text-xs font-bold mb-3 uppercase tracking-widest text-slate-500">
                    <span>{skill.name}</span>
                    <span className="text-emerald-500">{skill.val}% Mastery</span>
                  </div>
                  <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                    <div className={`${skill.color} h-full transition-all duration-1000 ease-out`} style={{ width: `${skill.val}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-10 p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/10">
               <div className="flex items-center space-x-3 text-emerald-400 text-sm font-bold mb-2">
                  <FiZap />
                  <span>AI Insight</span>
               </div>
               <p className="text-xs text-slate-400 leading-relaxed italic">"Focus on Control Flow patterns to reach Architect tier by next session."</p>
            </div>
          </div>

          <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 rounded-3xl p-8 transition-all hover:border-blue-500/20">
            <h2 className="text-sm font-black uppercase tracking-[0.2em] text-blue-400 mb-6">Autonomous Workflows</h2>
            <div className="space-y-3">
              {[
                { icon: <FiBook />, label: 'Neural Lesson' },
                { icon: <FiCode />, label: 'Logic Challenge' },
                { icon: <FiRefreshCw />, label: 'Resync State' }
              ].map((action) => (
                <button key={action.label} className="w-full flex items-center justify-between p-4 rounded-2xl bg-slate-800/30 text-slate-400 hover:text-emerald-400 hover:bg-slate-800 transition-all border border-transparent hover:border-slate-700">
                  <div className="flex items-center space-x-4">
                    <span className="text-emerald-500">{action.icon}</span>
                    <span className="font-bold text-sm">{action.label}</span>
                  </div>
                  <FiChevronRight />
                </button>
              ))}
            </div>
          </div>
        </aside>
      </div>

      <footer className="bg-[#020617]/40 backdrop-blur-md border-t border-slate-800/50 py-10">
        <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center opacity-60">
          <p className="text-xs font-mono tracking-widest text-slate-500 mb-4 md:mb-0">© 2026 LEARN_FLOW / NEURAL_NETWORK</p>
          <div className="flex space-x-6">
             <span className="text-[10px] uppercase tracking-tighter border border-slate-800 px-3 py-1 rounded-full">MCP_v2.0_CODE_EXECUTION</span>
             <span className="text-[10px] uppercase tracking-tighter border border-slate-800 px-3 py-1 rounded-full">AAIF_STANDARD_V1</span>
          </div>
        </div>
      </footer>

      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #10b981; }
      `}</style>
    </div>
  );
}
