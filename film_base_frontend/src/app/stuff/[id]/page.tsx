"use client";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import api from "@/lib/api/client";
import styles from "./page.module.css";
import { resolveMediaUrl } from "@/lib/utils/url";

type StuffDetails = {
  id: number;
  kinopoisk_id: number | null;
  name: string;
  english_name: string | null;
  career: string | null;
  genres: string | null;
  height: string | null;
  birthday_day_month: string | null;
  birthday_year: string | null;
  zodiac: string | null;
  age: string | null;
  birthplace: string | null;
  spouse: string | null;
  children: string | null;
  total_films: string | null;
  career_start_year: string | null;
  career_end_year: string | null;
  photo: string | null;
};

export default function StuffDetailsPage() {
  const params = useParams<{ id: string }>();
  const id = Number(params.id);
  const [p, setP] = useState<StuffDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const r = await api.get(`/stuff/${id}`);
        setP(r.data);
      } finally {
        setLoading(false);
      }
    }
    if (id) load();
  }, [id]);

  if (loading) return <div className={styles.container}>Загрузка...</div>;
  if (!p) return <div className={styles.container}>Персона не найдена</div>;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        {p.photo ? <img className={styles.photo} src={resolveMediaUrl(p.photo) || ""} alt={p.name} /> : <div className={styles.noPhoto} />}
        <div className={styles.info}>
          <h1 className={styles.title}>{p.name}</h1>
          {p.english_name ? <div className={styles.sub}>{p.english_name}</div> : null}
          <div className={styles.meta}>
            <span>Возраст: {p.age ?? "-"}</span>
            <span>Рост: {p.height ?? "-"}</span>
            <span>Знак: {p.zodiac ?? "-"}</span>
          </div>
          <div className={styles.meta}>
            <span>Родился: {p.birthplace ?? "-"}</span>
            <span>ДР: {p.birthday_day_month} {p.birthday_year}</span>
          </div>
          {p.career ? <div>Карьера: {p.career}</div> : null}
          {p.genres ? <div>Жанры: {p.genres}</div> : null}
          <div className={styles.meta}>
            <span>Фильмов: {p.total_films ?? "-"}</span>
            <span>Годы активности: {p.career_start_year ?? "-"} — {p.career_end_year ?? "-"}</span>
          </div>
        </div>
      </div>
    </div>
  );
}


