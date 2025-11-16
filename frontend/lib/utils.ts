import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date, format: 'short' | 'long' | 'relative' = 'short'): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(d.getTime())) {
    return 'Неизвестная дата';
  }

  switch (format) {
    case 'relative':
      return formatRelativeDate(d);
    case 'long':
      return d.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      });
    case 'short':
    default:
      return d.toLocaleDateString('ru-RU');
  }
}

export function formatRelativeDate(date: Date): string {
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (diffInSeconds < 60) {
    return 'только что';
  }
  
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    return `${diffInMinutes} мин. назад`;
  }
  
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return `${diffInHours} ч. назад`;
  }
  
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays === 1) {
    return 'вчера';
  }
  
  if (diffInDays < 7) {
    return `${diffInDays} дн. назад`;
  }
  
  return formatDate(date, 'short');
}

export function formatDurationMinutes(minutes: number): string {
  if (minutes < 60) {
    return `${minutes} мин`;
  }
  
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  
  if (remainingMinutes === 0) {
    return `${hours} ч`;
  }
  
  return `${hours} ч ${remainingMinutes} мин`;
}

export function formatDuration(duration: string | null | undefined): string {
  if (!duration || typeof duration !== 'string') {
    return '';
  }
  const cleanDuration = duration.trim().toLowerCase();
  
  // Если строка содержит только цифры, считаем что это минуты
  if (/^\d+$/.test(cleanDuration)) {
    const minutes = parseInt(cleanDuration, 10);
    return formatDurationMinutes(minutes);
  }
  
  // Извлекаем минуты из различных форматов
  // Форматы: "120 мин", "2 ч 30 мин", "2h 30m", "2:30"
  let minutes = 0;
  
  // Формат "часы:минуты" (например "2:30")
  const timeMatch = cleanDuration.match(/(\d+):(\d+)/);
  if (timeMatch) {
    const hours = parseInt(timeMatch[1], 10);
    const mins = parseInt(timeMatch[2], 10);
    minutes = hours * 60 + mins;
  } else {
    // Формат "X ч Y мин" или "Xh Ym" или "X hours Y minutes"
    const hourMinuteMatch = cleanDuration.match(/(\d+)\s*(?:ч|ч\.|h|hours?)\s*(\d+)?\s*(?:мин|м\.|m|minutes?)?/);
    if (hourMinuteMatch) {
      const hours = parseInt(hourMinuteMatch[1], 10);
      const mins = hourMinuteMatch[2] ? parseInt(hourMinuteMatch[2], 10) : 0;
      minutes = hours * 60 + mins;
    } else {
      // Формат "X мин" или "Xm" или "X минут"
      const minuteOnlyMatch = cleanDuration.match(/(\d+)\s*(?:мин|м\.|m|minutes?)/);
      if (minuteOnlyMatch) {
        minutes = parseInt(minuteOnlyMatch[1], 10);
      } else {
        // Если ничего не нашли, пробуем извлечь любое число
        const anyNumberMatch = cleanDuration.match(/(\d+)/);
        if (anyNumberMatch) {
          minutes = parseInt(anyNumberMatch[1], 10);
        }
      }
    }
  }
  
  // Если удалось извлечь минуты, форматируем их
  if (minutes > 0) {
    return formatDurationMinutes(minutes);
  }
  
  // Если не удалось извлечь, возвращаем исходную строку с небольшой очисткой
  return duration.trim() || '';
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.slice(0, maxLength).trim() + '...';
}


//Форматирование рейтинга для отображения
export function formatRating(rating: number | null | undefined, maxRating: number = 10): string {
  if (!rating || rating <= 0) {
    return 'Нет оценки';
  }
  
  return `${rating.toFixed(1)}/${maxRating}`;
}

//Получение цвета рейтинга на основе значения
export function getRatingColor(rating: number, maxRating: number = 10): string {
  const percentage = (rating / maxRating) * 100;
  
  if (percentage >= 80) {
    return 'text-green-500';
  } else if (percentage >= 60) {
    return 'text-yellow-500';
  } else if (percentage >= 40) {
    return 'text-orange-500';
  } else {
    return 'text-red-500';
  }
}