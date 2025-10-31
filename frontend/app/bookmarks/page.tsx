'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { Heart, Trash2, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useUserInteractionsStore } from '@/store';
import { FilmCard } from '@/components/film/FilmCard';
import { ROUTES } from '@/lib/config';

export default function BookmarksPage() {
  const {
    bookmarks,
    isLoadingBookmarks,
    fetchBookmarks,
    removeBookmark,
    bookmarksPage,
    bookmarksTotalCount,
  } = useUserInteractionsStore();

  useEffect(() => {
    fetchBookmarks(1);
  }, [fetchBookmarks]);

  const handleRemoveBookmark = async (filmId: number) => {
    try {
      await removeBookmark(filmId);
    } catch (error) {
      console.error('Failed to remove bookmark:', error);
    }
  };

  const handlePageChange = async (page: number) => {
    await fetchBookmarks(page);
  };

  const totalPages = Math.ceil(bookmarksTotalCount / 20);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <div className="flex items-center gap-4 mb-4">
          <Heart className="h-8 w-8 text-red-500" />
          <div>
            <h1 className="text-3xl font-bold">Мои закладки</h1>
            <p className="text-muted-foreground">
              {bookmarksTotalCount} фильмов сохранено
            </p>
          </div>
        </div>
      </div>

      {bookmarks.length > 0 ? (
        <div className="space-y-8">
          {/* Список закладок */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
            {bookmarks.map((bookmark) => (
              <div key={bookmark.id} className="group relative">
                {bookmark.film ? (
                  <FilmCard 
                    film={bookmark.film} 
                    showActions={true}
                  />
                ) : (
                  <div className="aspect-[2/3] bg-muted rounded-lg flex items-center justify-center">
                    <span className="text-muted-foreground">Фильм не найден</span>
                  </div>
                )}
                
                {/* Кнопка удаления */}
                <Button
                  size="icon"
                  variant="destructive"
                  className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => handleRemoveBookmark(bookmark.film_id)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>

          {/* Пагинация */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2">
              <Button
                variant="outline"
                onClick={() => handlePageChange(bookmarksPage - 1)}
                disabled={bookmarksPage === 1}
              >
                Предыдущая
              </Button>
              
              <div className="flex items-center gap-1">
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  let pageNum;
                  if (totalPages <= 5) {
                    pageNum = i + 1;
                  } else if (bookmarksPage <= 3) {
                    pageNum = i + 1;
                  } else if (bookmarksPage >= totalPages - 2) {
                    pageNum = totalPages - 4 + i;
                  } else {
                    pageNum = bookmarksPage - 2 + i;
                  }
                  
                  return (
                    <Button
                      key={pageNum}
                      variant={bookmarksPage === pageNum ? "default" : "outline"}
                      size="sm"
                      onClick={() => handlePageChange(pageNum)}
                    >
                      {pageNum}
                    </Button>
                  );
                })}
              </div>
              
              <Button
                variant="outline"
                onClick={() => handlePageChange(bookmarksPage + 1)}
                disabled={bookmarksPage === totalPages}
              >
                Следующая
              </Button>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-16">
          <Heart className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">Пока нет закладок</h3>
          <p className="text-muted-foreground mb-6 max-w-md mx-auto">
            Сохраняйте фильмы, которые хотите посмотреть позже, нажав на иконку сердца
          </p>
          <Button asChild>
            <Link href={ROUTES.FILMS}>
              <Plus className="h-4 w-4 mr-2" />
              Найти фильмы
            </Link>
          </Button>
        </div>
      )}
    </div>
  );
}