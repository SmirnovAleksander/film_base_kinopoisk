'use client';

import { useState, useEffect } from 'react';
import { AuthAPI } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function ResetPasswordPage() {
  const [token, setToken] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    }
  }, []);

  const validatePassword = (pwd: string): string[] => {
    const errors: string[] = [];
    if (pwd.length < 8) {
      errors.push('Пароль должен содержать минимум 8 символов');
    }
    if (!/(?=.*[a-z])/.test(pwd)) {
      errors.push('Пароль должен содержать минимум одну строчную букву');
    }
    if (!/(?=.*[A-Z])/.test(pwd)) {
      errors.push('Пароль должен содержать минимум одну заглавную букву');
    }
    if (!/(?=.*\d)/.test(pwd)) {
      errors.push('Пароль должен содержать минимум одну цифру');
    }
    return errors;
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Валидация
    if (!token) {
      setError('Токен сброса пароля обязателен');
      return;
    }

    if (!password) {
      setError('Пароль обязателен');
      return;
    }

    if (password !== confirmPassword) {
      setError('Пароли не совпадают');
      return;
    }

    const passwordErrors = validatePassword(password);
    if (passwordErrors.length > 0) {
      setError(passwordErrors.join('. '));
      return;
    }

    setIsResetting(true);

    try {
      await AuthAPI.resetPassword(token, password);
      setMessage('Пароль успешно изменен! Вы можете войти в систему.');
      setTimeout(() => {
        router.push('/(auth)/login');
      }, 3000);
    } catch (error: any) {
      console.error('Error resetting password:', error);
      setError('Ошибка сброса пароля. Проверьте токен и попробуйте еще раз.');
    } finally {
      setIsResetting(false);
    }
  };

  const handleRequestReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const email = (e.target as any).email.value;
    if (!email) {
      setError('Email обязателен');
      return;
    }

    setIsLoading(true);

    try {
      await AuthAPI.requestPasswordReset(email);
      setMessage('Инструкции по сбросу пароля отправлены на вашу почту');
    } catch (error: any) {
      console.error('Error requesting password reset:', error);
      setError('Ошибка отправки инструкций по сбросу пароля');
    } finally {
      setIsLoading(false);
    }
  };

  const showResetForm = !!token;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            {showResetForm ? 'Сброс пароля' : 'Восстановление пароля'}
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
            <>
              {showResetForm ? (
                // Форма сброса пароля
                <form onSubmit={handleResetPassword} className="space-y-4">
                  <div>
                    <Label htmlFor="token">Токен сброса</Label>
                    <Input
                      id="token"
                      type="text"
                      placeholder="Токен из email"
                      value={token}
                      onChange={(e) => setToken(e.target.value)}
                      disabled={isResetting}
                      required
                    />
                  </div>

                  <div>
                    <Label htmlFor="password">Новый пароль</Label>
                    <Input
                      id="password"
                      type="password"
                      placeholder="Введите новый пароль"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      disabled={isResetting}
                      required
                    />
                    <p className="text-xs text-gray-600 mt-1">
                      Минимум 8 символов, должен содержать заглавные и строчные буквы, цифры
                    </p>
                  </div>

                  <div>
                    <Label htmlFor="confirmPassword">Подтвердите пароль</Label>
                    <Input
                      id="confirmPassword"
                      type="password"
                      placeholder="Повторите пароль"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      disabled={isResetting}
                      required
                    />
                  </div>

                  <Button
                    type="submit"
                    disabled={isResetting}
                    className="w-full"
                  >
                    {isResetting ? 'Изменяем пароль...' : 'Изменить пароль'}
                  </Button>

                  <div className="text-center">
                    <Link 
                      href="/(auth)/login" 
                      className="text-sm text-blue-600 hover:text-blue-500"
                    >
                      Вернуться ко входу
                    </Link>
                  </div>
                </form>
              ) : (
                // Форма запроса сброса пароля
                <form onSubmit={handleRequestReset} className="space-y-4">
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="Введите ваш email"
                      disabled={isLoading}
                      required
                    />
                  </div>

                  <Button
                    type="submit"
                    disabled={isLoading}
                    className="w-full"
                  >
                    {isLoading ? 'Отправляем...' : 'Отправить инструкции'}
                  </Button>

                  <div className="text-center">
                    <Link 
                      href="/(auth)/login" 
                      className="text-sm text-blue-600 hover:text-blue-500"
                    >
                      Вернуться ко входу
                    </Link>
                  </div>
                </form>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}