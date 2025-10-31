'use client';

import Link from 'next/link';
import { ROUTES } from '@/lib/config';
import { RegisterForm } from '@/components/auth';

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 py-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link href={ROUTES.HOME} className="inline-flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">FB</span>
            </div>
            <span className="text-2xl font-bold">Film Base</span>
          </Link>
          <p className="text-muted-foreground mt-2">
            Создайте новый аккаунт
          </p>
        </div>

        <RegisterForm />

        {/* Дополнительная информация */}
        <div className="mt-8 text-center">
          <p className="text-xs text-muted-foreground">
            Создавая аккаунт, вы соглашаетесь с нашими{' '}
            <Link href="" className="underline hover:text-foreground">
              Условиями использования
            </Link>{' '}
            и{' '}
            <Link href="" className="underline hover:text-foreground">
              Политикой конфиденциальности
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}