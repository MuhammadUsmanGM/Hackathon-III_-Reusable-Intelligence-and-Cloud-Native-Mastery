'use client';

import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// Define types
interface User {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'teacher' | 'admin';
}

interface AppState {
  currentUser: User | null;
  theme: 'light' | 'dark';
  notifications: Array<{
    id: string;
    message: string;
    type: 'info' | 'success' | 'warning' | 'error';
    timestamp: Date;
  }>;
  isLoading: boolean;
}

interface Action {
  type: string;
  payload?: any;
}

// Initial state
const initialState: AppState = {
  currentUser: null,
  theme: 'dark',
  notifications: [],
  isLoading: false,
};

// Reducer
const appReducer = (state: AppState, action: Action): AppState => {
  switch (action.type) {
    case 'SET_CURRENT_USER':
      return { ...state, currentUser: action.payload };

    case 'SET_THEME':
      return { ...state, theme: action.payload };

    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [
          ...state.notifications,
          {
            id: Date.now().toString(),
            message: action.payload.message,
            type: action.payload.type,
            timestamp: new Date()
          }
        ]
      };

    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(notification => notification.id !== action.payload)
      };

    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };

    case 'TOGGLE_THEME':
      return { ...state, theme: state.theme === 'light' ? 'dark' : 'light' };

    default:
      return state;
  }
};

// Create context
interface AppContextProps {
  state: AppState;
  dispatch: React.Dispatch<Action>;
  setUser: (user: User) => void;
  toggleTheme: () => void;
  addNotification: (message: string, type: 'info' | 'success' | 'warning' | 'error') => void;
  removeNotification: (id: string) => void;
  setLoading: (loading: boolean) => void;
}

const AppContext = createContext<AppContextProps | undefined>(undefined);

// Provider component
export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  const setUser = (user: User) => {
    dispatch({ type: 'SET_CURRENT_USER', payload: user });
  };

  const toggleTheme = () => {
    dispatch({ type: 'TOGGLE_THEME' });
  };

  const addNotification = (message: string, type: 'info' | 'success' | 'warning' | 'error') => {
    dispatch({ type: 'ADD_NOTIFICATION', payload: { message, type } });
  };

  const removeNotification = (id: string) => {
    dispatch({ type: 'REMOVE_NOTIFICATION', payload: id });
  };

  const setLoading = (loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  };

  const value = {
    state,
    dispatch,
    setUser,
    toggleTheme,
    addNotification,
    removeNotification,
    setLoading
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook to use the context
export const useAppContext = (): AppContextProps => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};