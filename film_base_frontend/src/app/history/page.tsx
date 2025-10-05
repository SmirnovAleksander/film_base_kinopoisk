"use client";
import { useEffect, useState } from "react";
import { useHistoryStore } from "@/store/history";
import { useAuthStore } from "@/store/auth";
import { FilmHistoryItem, HistoryStats } from "@/lib/types";
import { resolveMediaUrl } from "@/lib/utils/url";
import Link from "next/link";
import styles from "./page.module.css";

export default function HistoryPage() {
  const { user } = useAuthStore();
  const { 
    history, 
    stats, 
    loading, 
    error, 
    getHistory, 
    getHistoryStats, 
    clearHistory, 
    removeFilmFromHistory 
  } = useHistoryStore();
  
  const [showStats, setShowStats] = useState(false);

  useEffect(() => {
    if (user) {
      getHistory();
      getHistoryStats();
    }
  }, [user, getHistory, getHistoryStats]);

  if (!user) {
    return (
      <div className={styles.container}>
        <h1>История посещений</h1>
        <p>Для просмотра истории необходимо войти в систему</p>
      </div>
    );
  }

  const handleClearHistory = async () => {
    if (confirm("Вы уверены, что хотите очистить всю историю посещений?")) {
      try {
        await clearHistory();
      } catch (error) {
        console.error("Ошибка при очистке истории:", error);
      }
    }
  };

  const handleRemoveFilm = async (filmId: number) => {
    try {
      await removeFilmFromHistory(filmId);
    } catch (error) {
      console.error("Ошибка при удалении из истории:", error);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>История посещений</h1>
        <div className={styles.actions}>
          <button 
            onClick={() => setShowStats(!showStats)}
            className={styles.statsButton}
          >
            {showStats ? 'Скрыть статистику' : 'Показать статистику'}
          </button>
          {history?.history && history.history.length > 0 && (
            <button 
              onClick={handleClearHistory}
              className={styles.clearButton}
            >
              Очистить историю
            </button>
          )}
        </div>
      </div>

      {showStats && stats && (
        <div className={styles.stats}>
          <h2>Статистика</h2>
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.total_visits}</div>
              <div className={styles.statLabel}>Всего посещений</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.visits_7d}</div>
              <div className={styles.statLabel}>За 7 дней</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.visits_30d}</div>
              <div className={styles.statLabel}>За 30 дней</div>
            </div>
            {stats.favorite_genre && (
              <div className={styles.statCard}>
                <div className={styles.statValue}>{stats.favorite_genre_count}</div>
                <div className={styles.statLabel}>
                  Любимый жанр: {stats.favorite_genre}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {loading && <div className={styles.loading}>Загрузка истории...</div>}
      
      {error && <div className={styles.error}>Ошибка: {error}</div>}

      {history?.history && history.history.length > 0 ? (
        <div className={styles.historyList}>
          <h2>Последние посещения</h2>
          {history.history.map((item: FilmHistoryItem) => (
            <div key={`${item.film.id}-${item.visited_at}`} className={styles.historyItem}>
              <Link href={`/films/${item.film.id}`} className={styles.filmLink}>
                <div className={styles.filmPoster}>
                  {item.film.poster ? (
                    <img 
                      src={resolveMediaUrl(item.film.poster) || ""} 
                      alt={item.film.title}
                      className={styles.poster}
                    />
                  ) : (
                    <div className={styles.noPoster} />
                  )}
                </div>
                <div className={styles.filmInfo}>
                  <h3 className={styles.filmTitle}>{item.film.title}</h3>
                  {item.film.original_title && (
                    <p className={styles.originalTitle}>{item.film.original_title}</p>
                  )}
                  <div className={styles.filmMeta}>
                    {item.film.year && <span>Год: {item.film.year}</span>}
                    {item.film.rating_kp && <span>KP: {item.film.rating_kp}</span>}
                    {item.film.rating_imdb && <span>IMDb: {item.film.rating_imdb}</span>}
                  </div>
                  <p className={styles.visitedAt}>
                    Посещено: {formatDate(item.visited_at)}
                  </p>
                </div>
              </Link>
              <button
                onClick={() => handleRemoveFilm(item.film.id)}
                className={styles.removeButton}
                title="Удалить из истории"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      ) : (
        !loading && (
          <div className={styles.empty}>
            <h2>История пуста</h2>
            <p>Вы еще не посещали страницы фильмов</p>
            <Link href="/films" className={styles.browseLink}>
              Перейти к каталогу фильмов
            </Link>
          </div>
        )
      )}
    </div>
  );
}
