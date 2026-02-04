'use client';

import { useState, useEffect, useCallback } from 'react';
import { AuthAPI } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function VerifyEmailPage() {
  const [token, setToken] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleVerify = useCallback(async (verificationToken?: string) => {
    const tokenToUse = verificationToken || token;
    if (!tokenToUse) {
      setError('Токен верификации обязателен');
      return;
    }

    setIsVerifying(true);
    setError('');

    try {
      await AuthAPI.verifyEmail(tokenToUse);
      setMessage('Email успешно подтвержден! Вы можете войти в систему.');
      setTimeout(() => {
        router.push('/login');
      }, 3000);
    } catch (error: any) {
      console.error('Error verifying email:', error);
      setError('Ошибка верификации email. Проверьте токен и попробуйте еще раз.');
    } finally {
      setIsVerifying(false);
    }
  }, [token, router]);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
      handleVerify(tokenFromUrl);
    }
  }, [handleVerify]);

  const handleRequestNewToken = async () => {
    setIsLoading(true);
    setError('');

    try {
      await AuthAPI.requestVerificationEmail();
      setMessage('Новый токен верификации отправлен на вашу почту');
    } catch (error: any) {
      console.error('Error requesting verification:', error);
      setError('Ошибка отправки токена верификации');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            Подтверждение email
          </CardTitle>
        </CardHeader>
        <CardContent>
          {message && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
              {message}
            </div>
          )}

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {!message && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="token">Токен верификации</Label>
                <Input
                  id="token"
                  type="text"
                  placeholder="Введите токен верификации"
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  disabled={isVerifying}
                />
              </div>

              <Button
                onClick={() => handleVerify()}
                disabled={isVerifying || !token}
                className="w-full"
              >
                {isVerifying ? 'Проверяем...' : 'Подтвердить email'}
              </Button>

              <div className="text-center">
                <p className="text-sm text-gray-600 mb-2">
                  Не получили токен верификации?
                </p>
                <Button
                  variant="outline"
                  onClick={handleRequestNewToken}
                  disabled={isLoading}
                  className="w-full"
                >
                  {isLoading ? 'Отправляем...' : 'Отправить новый токен'}
                </Button>
              </div>

              <div className="text-center">
                <Link
                  href="/login"
                  className="text-sm text-blue-600 hover:text-blue-500"
                >
                  Вернуться ко входу
                </Link>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}