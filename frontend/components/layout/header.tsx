'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Search,
  Film,
  Heart,
  History,
  User,
  LogOut,
  Menu,
  Sun,
  Moon,
  Monitor,
  Settings,
  Image
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from '@/components/ui/sheet';
import { useAuth } from '@/hooks/use-auth';
import { useTheme as useNextTheme } from 'next-themes';
import { ROUTES } from '@/lib/config';

export function Header() {
  const [searchQuery, setSearchQuery] = useState('');
  const { user, logout, isAuthenticated } = useAuth();
  const { theme, setTheme } = useNextTheme();
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`${ROUTES.FILMS}?search=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      router.push(ROUTES.HOME);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const navigation = [
    { name: 'Фильмы', href: ROUTES.FILMS, icon: Film },
    { name: 'Медиа', href: ROUTES.MEDIA, icon: Image },
    { name: 'Закладки', href: ROUTES.BOOKMARKS, icon: Heart, requireAuth: true },
    { name: 'История', href: ROUTES.HISTORY, icon: History, requireAuth: true },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center max-w-7xl px-4">
        {/* Логотип */}
        <Link href={ROUTES.HOME} className="flex items-center space-x-2 mr-6">
          <Film className="h-6 w-6 text-primary" />
          <span className="font-bold text-xl">Film Base</span>
        </Link>

        {/* Поиск - десктоп */}
        <form onSubmit={handleSearch} className="flex-1 max-w-md mr-6 hidden md:block">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Поиск фильмов..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
        </form>

        {/* Навигация - десктоп */}
        <nav className="hidden md:flex items-center space-x-6 mr-6">
          {navigation.map((item) => {
            if (item.requireAuth && !isAuthenticated) return null;
            
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                href={item.href}
                className="flex items-center space-x-1 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                <Icon className="h-4 w-4" />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Правая часть */}
        <div className="flex items-center space-x-2 ml-auto">
          {/* Переключатель темы */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <Sun className="h-[1.2rem] w-[1.2rem] scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90" />
                <Moon className="absolute h-[1.2rem] w-[1.2rem] scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0" />
                <span className="sr-only">Переключить тему</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setTheme("light")}>
                <Sun className="mr-2 h-4 w-4" />
                Светлая
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setTheme("dark")}>
                <Moon className="mr-2 h-4 w-4" />
                Темная
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setTheme("system")}>
                <Monitor className="mr-2 h-4 w-4" />
                Системная
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Пользовательское меню */}
          {isAuthenticated ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={undefined} alt={user?.email} />
                    <AvatarFallback>
                      {user?.email?.charAt(0).toUpperCase() || 'U'}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <div className="flex items-center justify-start gap-2 p-2">
                  <div className="flex flex-col space-y-1 leading-none">
                    {user?.email && (
                      <p className="font-medium text-sm">{user.email}</p>
                    )}
                  </div>
                </div>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <Link href={ROUTES.PROFILE}>
                    <User className="mr-2 h-4 w-4" />
                    Профиль
                  </Link>
                </DropdownMenuItem>
                {user?.is_superuser && (
                  <>
                    <DropdownMenuItem asChild>
                      <Link href="/admin">
                        <Settings className="mr-2 h-4 w-4" />
                        Admin
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                  </>
                )}
                <DropdownMenuItem onClick={handleLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  Выйти
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <div className="flex items-center space-x-2">
              <Button asChild variant="ghost">
                <Link href={ROUTES.LOGIN}>Войти</Link>
              </Button>
              <Button asChild>
                <Link href={ROUTES.REGISTER}>Регистрация</Link>
              </Button>
            </div>
          )}

          {/* Мобильное меню */}
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="md:hidden">
                <Menu className="h-5 w-5" />
                <span className="sr-only">Меню</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[300px] sm:w-[400px]">
              <div className="flex flex-col space-y-4 mt-4">
                {/* Поиск - мобильный */}
                <form onSubmit={handleSearch} className="px-2">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      type="search"
                      placeholder="Поиск фильмов..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </form>

                {/* Навигация - мобильная */}
                <nav className="flex flex-col space-y-2 px-2">
                  {navigation.map((item) => {
                    if (item.requireAuth && !isAuthenticated) return null;
                    
                    const Icon = item.icon;
                    return (
                      <Link
                        key={item.name}
                        href={item.href}
                        className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-accent rounded-md transition-colors"
                      >
                        <Icon className="h-4 w-4" />
                        <span>{item.name}</span>
                      </Link>
                    );
                  })}
                </nav>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}