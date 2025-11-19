import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const token = request.cookies.get('film-base-token')?.value;
    const { pathname } = request.nextUrl;

    const protectedRoutes = ['/profile', '/bookmarks', '/history', '/admin'];

    const authRoutes = ['/login', '/register', '/forgot-password', '/reset-password'];

    const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route));
    const isAuthRoute = authRoutes.some(route => pathname.startsWith(route));

    if (isProtectedRoute && !token) {
        const url = new URL('/login', request.url);
        url.searchParams.set('redirect', pathname);
        return NextResponse.redirect(url);
    }

    if (isAuthRoute && token) {
        return NextResponse.redirect(new URL('/', request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: [
        '/profile/:path*',
        '/bookmarks/:path*',
        '/history/:path*',
        '/admin/:path*',
        '/login',
        '/register',
        '/forgot-password',
        '/reset-password',
    ],
};
