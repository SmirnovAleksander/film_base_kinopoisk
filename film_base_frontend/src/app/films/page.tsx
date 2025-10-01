"use client";
import { useEffect, useState } from "react";
import { useFilmsStore } from "@/store/films";
import styles from "./page.module.css";

export default function FilmsPage() {
  const { items, page, pageSize, loading, list, search } = useFilmsStore();
  const [q, setQ] = useState("");

  useEffect(() => {
    list(1, 20);
  }, [list]);

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
            <div key={f.id} className={styles.card}>
              {f.poster ? <img className={styles.poster} src={f.poster} alt={f.title} /> : <div className={styles.noPoster} />}
              <div className={styles.cardTitle}>{f.title}</div>
              <div className={styles.meta}>KP: {f.rating_kp ?? "-"}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


