'use client';

import { useState, useEffect } from 'react';
import { MediaAPI } from '@/lib/api';
import { Media } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';

export default function MediaPage() {
  const [media, setMedia] = useState<Media[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [types, setTypes] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedType, setSelectedType] = useState<string>('');
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    loadMedia();
  }, [currentPage, selectedCategory, selectedType]);

  const loadInitialData = async () => {
    try {
      setIsLoading(true);
      const [categoriesData, typesData] = await Promise.all([
        MediaAPI.getMediaCategories(),
        MediaAPI.getMediaTypes()
      ]);
      setCategories(categoriesData.categories);
      setTypes(typesData.types);
    } catch (error) {
      console.error('Error loading initial data:', error);
    }
  };

  const loadMedia = async () => {
    try {
      setIsLoading(true);
      const response = await MediaAPI.getMedia(
        currentPage,
        20,
        selectedCategory || undefined,
        selectedType || undefined
      );
      setMedia(response.media);
      setTotalPages(response.pagination.pages);
    } catch (error) {
      console.error('Error loading media:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCategoryChange = (value: string) => {
    setSelectedCategory(value === 'all' ? '' : value);
    setCurrentPage(1);
  };

  const handleTypeChange = (value: string) => {
    setSelectedType(value === 'all' ? '' : value);
    setCurrentPage(1);
  };

  const clearFilters = () => {
    setSelectedCategory('');
    setSelectedType('');
    setCurrentPage(1);
  };

  if (isLoading && media.length === 0) {
    return (
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">Медиа контент</h1>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 9 }).map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-6 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-4 w-full mb-2" />
                <Skeleton className="h-4 w-2/3" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Медиа контент</h1>
      
      <div className="space-y-6">
        {/* Фильтры */}
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <Label htmlFor="category">Категория</Label>
            <Select value={selectedCategory} onValueChange={handleCategoryChange}>
              <SelectTrigger>
                <SelectValue placeholder="Все категории" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все категории</SelectItem>
                {categories.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <div>
            <Label htmlFor="type">Тип</Label>
            <Select value={selectedType} onValueChange={handleTypeChange}>
              <SelectTrigger>
                <SelectValue placeholder="Все типы" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все типы</SelectItem>
                {types.map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <div className="flex items-end">
            <Button
              variant="outline"
              onClick={clearFilters}
              className="w-full"
            >
              Сбросить фильтры
            </Button>
          </div>
        </div>

        {/* Список медиа */}
        {media.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">
              Медиа контент не найден
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {media.map((item) => (
              <Card key={item.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="aspect-w-16 aspect-h-9 w-full mb-4">
                    {item.image ? (
                      <img
                        src={item.image}
                        alt={item.title || 'Медиа'}
                        className="object-cover rounded-md w-full h-48"
                      />
                    ) : (
                      <div className="bg-gray-200 rounded-md w-full h-48 flex items-center justify-center">
                        <span className="text-gray-400">Нет изображения</span>
                      </div>
                    )}
                  </div>
                  <CardTitle className="text-lg line-clamp-2">
                    {item.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {item.category && (
                      <Badge variant="secondary">{item.category}</Badge>
                    )}
                    
                    {item.type && (
                      <Badge variant="outline">{item.type}</Badge>
                    )}
                    
                    {item.card_type && (
                      <Badge variant="outline">{item.card_type}</Badge>
                    )}
                    
                    <p className="text-sm text-gray-600">
                      Дата создания: {new Date(item.parsed_at).toLocaleDateString()}
                    </p>
                    
                    {item.date && (
                      <p className="text-sm text-gray-600">
                        Дата: {new Date(item.date).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Пагинация */}
        {totalPages > 1 && (
          <div className="flex justify-center space-x-2">
            <Button
              variant="outline"
              disabled={currentPage === 1}
              onClick={() => setCurrentPage(currentPage - 1)}
            >
              Предыдущая
            </Button>
            
            <div className="flex space-x-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const page = i + 1;
                return (
                  <Button
                    key={page}
                    variant={currentPage === page ? "default" : "outline"}
                    onClick={() => setCurrentPage(page)}
                  >
                    {page}
                  </Button>
                );
              })}
            </div>
            
            <Button
              variant="outline"
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage(currentPage + 1)}
            >
              Следующая
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}