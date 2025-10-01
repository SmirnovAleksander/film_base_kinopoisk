"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api/client";
import { FilmDetails, SimilarFilm, WatchProvider } from "@/lib/types";
import styles from "./page.module.css";
import Link from "next/link";
import { resolveMediaUrl } from "@/lib/utils/url";

type FilmStuff = { id: number; kinopoisk_id: number | null; name: string; english_name: string | null; photo: string | null; role: string };

export default function FilmDetailsPage() {
  const params = useParams<{ id: string }>();
  const id = Number(params.id);
  const [film, setFilm] = useState<FilmDetails | null>(null);
  const [providers, setProviders] = useState<WatchProvider[]>([]);
  const [similar, setSimilar] = useState<SimilarFilm[]>([]);
  const [loading, setLoading] = useState(true);
  const [stuff, setStuff] = useState<FilmStuff[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const [f, p, s, st] = await Promise.all([
          api.get(`/films/${id}`),
          api.get(`/films/${id}/watch-providers`),
          api.get(`/films/${id}/similar`),
          api.get(`/films/${id}/stuff`),
        ]);
        setFilm(f.data);
        setProviders(p.data || []);
        setSimilar(s.data || []);
        setStuff(st.data || []);
      } finally {
        setLoading(false);
      }
    }
    if (id) load();
  }, [id]);

  if (loading) return <div className={styles.container}>Загрузка...</div>;
  if (!film) return <div className={styles.container}>Фильм не найден</div>;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        {film.poster ? (
          <img className={styles.poster} src={resolveMediaUrl(film.poster) || ""} alt={film.title} />
        ) : (
          <div className={styles.noPoster} />
        )}
        <div className={styles.info}>
          <h1 className={styles.title}>{film.title}</h1>
          {film.original_title ? <div className={styles.sub}>{film.original_title}</div> : null}
          <div className={styles.meta}>
            <span>Год: {film.year ?? "-"}</span>
            <span>Длительность: {film.duration ?? "-"}</span>
            <span>Возраст: {film.age_rating ?? "-"}</span>
          </div>
          <div className={styles.ratings}>
            <span className={styles.badge}>KP {film.rating_kp ?? "-"}</span>
            <span className={styles.badge}>IMDb {film.rating_imdb ?? "-"}</span>
          </div>
          {film.tagline ? <div className={styles.tagline}>«{film.tagline}»</div> : null}
          {film.full_description ? <p className={styles.desc}>{film.full_description}</p> : null}
        </div>
      </div>

      {providers.length ? (
        <section className={styles.section}>
          <h2 className={styles.h2}>Где смотреть</h2>
          <div className={styles.providers}>
            {providers.map((p) => (
              <a key={p.name} href={p.url} target="_blank" rel="noreferrer" className={styles.provider}>
                {p.logo ? <img src={resolveMediaUrl(p.logo) || ""} alt={p.name} /> : null}
                <span>{p.name}</span>
              </a>
            ))}
          </div>
        </section>
      ) : null}

      {similar.length ? (
        <section className={styles.section}>
          <h2 className={styles.h2}>Похожие фильмы</h2>
          <ul className={styles.similar}>
            {similar.map((s) => (
              <li key={s.kinopoisk_id}>{s.title}</li>
            ))}
          </ul>
        </section>
      ) : null}

      {stuff.length ? (
        <section className={styles.section}>
          <h2 className={styles.h2}>Участники</h2>
          <div className={styles.stuffGrid}>
            {stuff
              .filter((u) => u.role === "actor" || u.role === "director")
              .map((u) => (
                <Link key={u.id} href={`/stuff/${u.id}`} className={styles.stuffCard}>
                  {u.photo ? (
                    <img src={resolveMediaUrl(u.photo) || ""} alt={u.name} />
                  ) : (
                    <div className={styles.stuffNoPhoto} />
                  )}
                  <div className={styles.stuffName}>{u.name}</div>
                  <div className={styles.stuffRole}>{u.role}</div>
                </Link>
              ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}


