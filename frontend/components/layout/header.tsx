'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Search,
  Film,
  Heart,
  User,
  LogOut,
  Menu,
  Sun,
  History,
  Moon,
  Monitor,
  Settings
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
import { useAuth } from '@/hooks';
import { useTheme as useNextTheme } from 'next-themes';
import { ROUTES } from '@/lib/config';
import { FilmsAPI } from '@/lib/api';
import Image from 'next/image';

export function Header() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const { user, logout, isAuthenticated } = useAuth();
  const { setTheme } = useNextTheme();
  const router = useRouter();

  // Эффект для живого поиска с debounce
  useEffect(() => {
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    if (searchQuery.trim().length > 0) {
      setIsSearching(true);
      searchTimeoutRef.current = setTimeout(async () => {
        try {
          const response = await FilmsAPI.searchFilms({
            query: searchQuery.trim(),
            page_size: 5
          });
          setSearchResults(response.items);
        } catch (error) {
          console.error('Search error:', error);
          setSearchResults([]);
        } finally {
          setIsSearching(false);
        }
      }, 500); // 500ms delay
    } else {
      setSearchResults([]);
      setIsSearching(false);
    }

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [searchQuery]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`${ROUTES.FILMS}?search=${encodeURIComponent(searchQuery.trim())}`);
      setIsSearchOpen(false);
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
    { name: 'Закладки', href: ROUTES.BOOKMARKS, icon: Heart, requireAuth: true },
    { name: 'История', href: ROUTES.HISTORY, icon: History },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
      <div className="container mx-auto flex h-16 items-center max-w-7xl px-4">
        {/* Логотип */}
        <Link href={ROUTES.HOME} className="flex items-center space-x-2 mr-6">
          <Film className="h-6 w-6 text-primary" />
          <span className="font-bold text-xl">Film Base</span>
        </Link>

        {/* Поиск - десктоп */}
        <div className="flex-1 max-w-md mr-6 hidden md:block relative">
          <form onSubmit={handleSearch} className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Поиск фильмов..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setIsSearchOpen(true);
              }}
              onFocus={() => setIsSearchOpen(true)}
              className="pl-10"
            />
          </form>

          {/* Выпадающий список результатов */}
          {isSearchOpen && searchQuery.trim().length > 0 && (
            <>
              <div
                className="fixed inset-0 z-40 bg-transparent"
                onClick={() => setIsSearchOpen(false)}
              />
              <div className="absolute top-full left-0 right-0 mt-2 bg-popover border rounded-md shadow-lg overflow-hidden z-50">
                {isSearching ? (
                  <div className="p-4 text-center text-sm text-muted-foreground">
                    Поиск...
                  </div>
                ) : searchResults.length > 0 ? (
                  <div className="max-h-[400px] overflow-y-auto">
                    {searchResults.map((film) => (
                      <Link
                        key={film.id}
                        href={ROUTES.FILM_DETAILS(film.id)}
                        className="flex items-start gap-3 p-3 hover:bg-accent transition-colors"
                        onClick={() => {
                          setIsSearchOpen(false);
                          setSearchQuery('');
                        }}
                      >
                        {film.poster ? (
                          <div className="relative w-10 h-14 shrink-0">
                            <Image
                              src={film.poster}
                              alt={film.title || 'Film'}
                              fill
                              className="object-cover rounded-sm"
                              sizes="40px"
                              unoptimized
                            />
                          </div>
                        ) : (
                          <div className="w-10 h-14 bg-muted rounded-sm flex items-center justify-center shrink-0">
                            <Film className="h-4 w-4 text-muted-foreground" />
                          </div>
                        )}
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">
                            {film.title || film.original_title}
                          </p>
                          <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                            {film.year && <span>{film.year}</span>}
                            {film.rating_kp && (
                              <span className="text-green-500 font-medium">
                                {film.rating_kp}
                              </span>
                            )}
                          </div>
                        </div>
                      </Link>
                    ))}
                    <Link
                      href={`${ROUTES.FILMS}?search=${encodeURIComponent(searchQuery.trim())}`}
                      className="block p-3 text-center text-sm text-primary hover:bg-accent border-t"
                      onClick={() => setIsSearchOpen(false)}
                    >
                      Показать все результаты
                    </Link>
                  </div>
                ) : (
                  <div className="p-4 text-center text-sm text-muted-foreground">
                    Ничего не найдено
                  </div>
                )}
              </div>
            </>
          )}
        </div>

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