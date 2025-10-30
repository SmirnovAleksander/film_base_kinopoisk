import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

// Интерфейс для данных пользователя
interface UserData {
  id: number;
  email: string;
  is_superuser: boolean;
  is_active: boolean;
  is_verified: boolean;
  username: string;
  first_name?: string | null;
  last_name?: string | null;
  created_at: string;
  updated_at: string;
}

// 1. Укажем защищенные и публичные маршруты
const protectedRoutes = ['/profile', '/bookmarks', '/history', '/admin'];
const publicRoutes = ['/login', '/register', '/verify-email', '/reset-password', '/films', '/media', '/stuff'];
const adminRoutes = ['/admin'];

// 2. Функция для извлечения данных пользователя из cookies
async function getUserDataFromCookies(): Promise<UserData | null> {
  try {
    const userCookie = (await cookies()).get('film-base-user');
    if (!userCookie) return null;
    
    return JSON.parse(userCookie.value) as UserData;
  } catch (error) {
    console.error('Failed to parse user data from cookies:', error);
    return null;
  }
}

// 3. Функция для проверки аутентификации
async function isAuthenticated(): Promise<boolean> {
  const sessionCookie = (await cookies()).get('film-base-token');
  const userCookie = (await cookies()).get('film-base-user');
  return !!(sessionCookie && userCookie);
}

export default async function middleware(req: NextRequest) {
  // 4. Проверим, является ли текущий маршрут защищенным или публичным
  const path = req.nextUrl.pathname;
  const isProtectedRoute = protectedRoutes.some(route =>
    path === route || path.startsWith(route + '/')
  );
  const isAdminRoute = adminRoutes.some(route =>
    path === route || path.startsWith(route + '/')
  );
  const isPublicRoute = publicRoutes.includes(path);

  // 5. Проверяем аутентификацию для защищенных маршрутов
  if (isProtectedRoute) {
    const authenticated = await isAuthenticated();
    
    // Перенаправляем на /login, если пользователь не авторизован
    if (!authenticated) {
      const loginUrl = new URL('/login', req.nextUrl);
      loginUrl.searchParams.set('redirect', path);
      return NextResponse.redirect(loginUrl);
    }

    // 6. Дополнительная проверка для административных маршрутов
    if (isAdminRoute) {
      const userData = await getUserDataFromCookies();
      
      // Проверяем, что пользователь существует и является суперюзером
      if (!userData || !userData.is_superuser) {
        console.warn(`Access denied to ${path} - user is not a superuser`);
        // Перенаправляем на профиль для несуперюзеров
        return NextResponse.redirect(new URL('/profile', req.nextUrl));
      }
    }
  }

  // 7. Перенаправляем на главную, если пользователь авторизован и находится на странице логина
  if (
    isPublicRoute &&
    (await isAuthenticated()) &&
    (path === '/login' || path === '/register')
  ) {
    return NextResponse.redirect(new URL('/', req.nextUrl));
  }

  return NextResponse.next();
}

// Маршруты, на которых middleware не должен работать
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
};