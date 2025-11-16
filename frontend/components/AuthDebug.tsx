'use client';

import { useState } from 'react';
import { AuthAPI } from '@/lib/api/auth.api';
import { useAuth } from '@/hooks/use-auth';

export function AuthDebug() {
  const [isVisible, setIsVisible] = useState(false);
  const { isAuthenticated, user, token, isLoading } = useAuth();

  const runDiagnostics = () => {
    console.log('🔍 AuthAPI Token:', AuthAPI.getAuthToken() ? `${AuthAPI.getAuthToken()!.substring(0, 20)}...` : 'null');
    console.log('🔍 AuthAPI User:', AuthAPI.getUserData());
    console.log('🔍 AuthAPI isTokenValid:', AuthAPI.isTokenValid());
    console.log('🔍 AuthAPI localStorage available:', AuthAPI.isLocalStorageAvailable());
    
    console.log('🔍 Store State:', {
      isAuthenticated,
      user: user ? `${user.username} (${user.id})` : null,
      token: token ? `${token.substring(0, 20)}...` : null,
      isLoading
    });
  };

  if (process.env.NODE_ENV === 'production' || process.env.NEXT_PUBLIC_ENV === 'production') {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <button
        onClick={() => setIsVisible(!isVisible)}
        className="bg-red-500 text-white px-3 py-1 rounded text-xs mb-2"
      >
        Debug Auth
      </button>
      
      {isVisible && (
        <div className="bg-black text-white p-4 rounded text-xs max-w-md">
          <h3 className="font-bold mb-2">Auth Status:</h3>
          <div className="space-y-1">
            <div>Authenticated: {isAuthenticated ? '✅' : '❌'}</div>
            <div>Loading: {isLoading ? '⏳' : '✅'}</div>
            <div>User: {user?.username || 'None'}</div>
            <div>Token: {token ? `${token.substring(0, 10)}...` : 'None'}</div>
          </div>
          
          <button
            onClick={runDiagnostics}
            className="bg-blue-500 text-white px-2 py-1 rounded text-xs mt-2 mr-2"
          >
            Run Diagnostics
          </button>
          
          <button
            onClick={() => {
              AuthAPI.clearAuthData();
              window.location.reload();
            }}
            className="bg-yellow-500 text-black px-2 py-1 rounded text-xs mt-2"
          >
            Clear & Reload
          </button>
        </div>
      )}
    </div>
  );
}