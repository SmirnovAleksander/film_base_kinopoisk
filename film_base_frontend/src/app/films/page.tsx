"use client";
import { useEffect, useState } from "react";
import { useFilmsStore } from "@/store/films";
import styles from "./page.module.css";
import { resolveMediaUrl } from "@/lib/utils/url";
import Link from "next/link";
import {useShallow} from "zustand/react/shallow";
import type {FilmsState} from "../../store/films"

export default function FilmsPage() {
  const { items, page, pageSize, loading, list, search } = useFilmsStore(
      useShallow((s:FilmsState) => ({
          items: s.items,
          page: s.page,
          pageSize: s.pageSize,
          loading: s.loading,
          list: s.list,
          search: s.search
      }))
  );
  const [q, setQ] = useState("");
  const [imgError, setImgError] = useState(false);

  useEffect(() => {
    list(1, 20);
  }, []);

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Фильмы</h1>
      <div className={styles.searchRow}>
        <input className={styles.input} placeholder="Поиск по названию" value={q} onChange={(e) => setQ(e.target.value)} />
        <button className={styles.button} onClick={() => search(q, 1, 20)}>Искать</button>
      </div>
      {loading ? (
        <div>Загрузка...</div>
      ) : (
        <div className={styles.grid}>
          {items.map((f) => (
            <Link key={f.id} href={`/films/${f.id}`} className={styles.card}>
                {!imgError && f.poster ? (
                    <img
                        className={styles.poster}
                        src={resolveMediaUrl(f.poster) || ""}
                        alt={f.title}
                        onError={() => setImgError(true)}
                    />
                ) : (
                    <div className={styles.noPoster}>Нет постера</div>
                )}
              <div className={styles.content}>
                <div className={styles.cardTitle}>{f.title}</div>
                <div className={styles.sub}>{f.original_title || ""}</div>
                <div className={styles.ratings}>
                  <span>Год: {f.year ?? "-"}</span>
                  <span>Длительность: {f.duration ?? "-"}</span>
                  <span>KP: {f.rating_kp ?? "-"}</span>
                  <span>IMDb: {f.rating_imdb ?? "-"}</span>
                </div>
                {f.full_description ? (
                  <div className={styles.desc}>{f.full_description}</div>
                ) : null}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}


