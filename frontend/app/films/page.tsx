'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination';
import { FilmCard, FilmCardSkeleton, FilmsFilters } from '@/components/film';
import { useFilmsStore } from '@/store';
import { FilmFilterParams } from '@/lib/types';

export default function FilmsPage() {
  const searchParams = useSearchParams();
  const {
    films,
    genres,
    countries,
    searchQuery,
    filters,
    isLoading,
    isSearching,
    currentPage,
    pageSize,
    totalCount,
    searchFilms,
    filterFilms,
    fetchGenres,
    fetchCountries,
    setSearchQuery,
    setFilters,
    setPage,
  } = useFilmsStore();

  // Инициализация данных
  useEffect(() => {
    fetchGenres();
    fetchCountries();
  }, [fetchGenres, fetchCountries]);

  // Обработка URL параметров при загрузке
  useEffect(() => {
    const search = searchParams.get('search');
    const genre = searchParams.get('genre');
    const country = searchParams.get('country');
    const startYear = searchParams.get('start_year');
    const endYear = searchParams.get('end_year');
    const minRating = searchParams.get('min_rating');
    const maxRating = searchParams.get('max_rating');

    if (search && search.trim()) {
      handleSearch(search.trim());
    } else {
      // Загружаем все фильмы
      filterFilms({ page: 1, page_size: pageSize });
    }

    // Применяем фильтры из URL
    if (genre || country || startYear || endYear || minRating || maxRating) {
      const filterParams: FilmFilterParams = {
        page: 1,
        page_size: pageSize,
        genre_id: genre ? parseInt(genre) : undefined,
        country_id: country ? parseInt(country) : undefined,
        start_year: startYear ? parseInt(startYear) : undefined,
        end_year: endYear ? parseInt(endYear) : undefined,
        min_rating: minRating ? parseFloat(minRating) : undefined,
        max_rating: maxRating ? parseFloat(maxRating) : undefined,
      };
      filterFilms(filterParams);
    }
  }, [searchParams]);

  // Обработчики для FilmsFilters
  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    await searchFilms({
      query: query.trim(),
      page: 1,
      page_size: pageSize,
    });
  };

  const handleFilterApply = async (filterParams: FilmFilterParams) => {
    setFilters(filterParams);
    await filterFilms(filterParams);
  };

  const handleFilterReset = () => {
    setFilters({});
    setSearchQuery('');
    filterFilms({ page: 1, page_size: pageSize });
  };

  const handleFilterRemove = async (key: keyof FilmFilterParams) => {
    const newFilters = { ...filters };
    delete newFilters[key];

    // Специальная обработка для поискового запроса
    if (key === 'query' as any) {
      setSearchQuery('');
      await filterFilms({ page: 1, page_size: pageSize });
      return;
    }

    setFilters(newFilters);
    await filterFilms({ ...newFilters, page: 1 });
  };

  const handlePageChange = async (page: number) => {
    setPage(page);
    if (searchQuery) {
      await searchFilms({
        query: searchQuery,
        page,
        page_size: pageSize,
      });
    } else if (Object.keys(filters).length > 0) {
      await filterFilms({ ...filters, page });
    } else {
      await filterFilms({ page, page_size: pageSize });
    }
  };

  const totalPages = Math.ceil(totalCount / pageSize);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">Каталог фильмов</h1>
        <p className="text-muted-foreground">
          Найдено фильмов: {totalCount}
        </p>
      </div>

      <FilmsFilters
        genres={genres}
        countries={countries}
        searchQuery={searchQuery}
        filters={filters}
        totalCount={totalCount}
        isLoading={isLoading}
        isSearching={isSearching}
        onSearch={handleSearch}
        onFilterApply={handleFilterApply}
        onFilterReset={handleFilterReset}
        onFilterRemove={handleFilterRemove}
        pageSize={pageSize}
      />

      {/* Список фильмов */}
      <div className="space-y-6">
        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
            {Array.from({ length: 12 }).map((_, i) => (
              <FilmCardSkeleton key={i} />
            ))}
          </div>
        ) : films.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
              {films.map((film) => (
                <FilmCard key={film.id} film={film} />
              ))}
            </div>

            {/* Пагинация */}
            {totalPages > 1 && (
              <Pagination>
                <PaginationContent>
                  <PaginationItem>
                    <PaginationPrevious
                      href="#"
                      onClick={(e: React.MouseEvent) => {
                        e.preventDefault();
                        if (currentPage > 1) {
                          handlePageChange(currentPage - 1);
                        }
                      }}
                    />
                  </PaginationItem>

                  {(() => {
                    const pageNumbers = [];
                    const showPages = Math.min(7, totalPages);

                    if (totalPages <= showPages) {
                      // Показываем все страницы если их мало
                      for (let i = 1; i <= totalPages; i++) {
                        pageNumbers.push(
                          <PaginationItem key={i}>
                            <PaginationLink
                              href="#"
                              isActive={currentPage === i}
                              onClick={(e: React.MouseEvent) => {
                                e.preventDefault();
                                handlePageChange(i);
                              }}
                            >
                              {i}
                            </PaginationLink>
                          </PaginationItem>
                        );
                      }
                    } else {
                      // Сложная логика для большого количества страниц
                      const startPage = Math.max(1, currentPage - 2);
                      const endPage = Math.min(totalPages, currentPage + 2);

                      // Первая страница
                      if (startPage > 1) {
                        pageNumbers.push(
                          <PaginationItem key={1}>
                            <PaginationLink
                              href="#"
                              isActive={currentPage === 1}
                              onClick={(e: React.MouseEvent) => {
                                e.preventDefault();
                                handlePageChange(1);
                              }}
                            >
                              1
                            </PaginationLink>
                          </PaginationItem>
                        );

                        if (startPage > 2) {
                          pageNumbers.push(<PaginationEllipsis key="ellipsis-start" />);
                        }
                      }

                      // Страницы вокруг текущей
                      for (let i = startPage; i <= endPage; i++) {
                        pageNumbers.push(
                          <PaginationItem key={i}>
                            <PaginationLink
                              href="#"
                              isActive={currentPage === i}
                              onClick={(e: React.MouseEvent) => {
                                e.preventDefault();
                                handlePageChange(i);
                              }}
                            >
                              {i}
                            </PaginationLink>
                          </PaginationItem>
                        );
                      }

                      // Последняя страница
                      if (endPage < totalPages) {
                        if (endPage < totalPages - 1) {
                          pageNumbers.push(<PaginationEllipsis key="ellipsis-end" />);
                        }

                        pageNumbers.push(
                          <PaginationItem key={totalPages}>
                            <PaginationLink
                              href="#"
                              isActive={currentPage === totalPages}
                              onClick={(e: React.MouseEvent) => {
                                e.preventDefault();
                                handlePageChange(totalPages);
                              }}
                            >
                              {totalPages}
                            </PaginationLink>
                          </PaginationItem>
                        );
                      }
                    }

                    return pageNumbers;
                  })()}

                  <PaginationItem>
                    <PaginationNext
                      href="#"
                      onClick={(e: React.MouseEvent) => {
                        e.preventDefault();
                        if (currentPage < totalPages) {
                          handlePageChange(currentPage + 1);
                        }
                      }}
                    />
                  </PaginationItem>
                </PaginationContent>
              </Pagination>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-lg">
              {isSearching ? 'Поиск не дал результатов' : 'Фильмы не найдены'}
            </p>
            <p className="text-muted-foreground mt-2">
              Попробуйте изменить параметры поиска или фильтры
            </p>
          </div>
        )}
      </div>
    </div>
  );
}