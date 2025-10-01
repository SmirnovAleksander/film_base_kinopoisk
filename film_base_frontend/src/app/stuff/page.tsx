"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api/client";
import styles from "./page.module.css";
import Link from "next/link";
import { resolveMediaUrl } from "@/lib/utils/url";

type StuffItem = { id: number; kinopoisk_id: number | null; name: string; english_name: string | null; photo: string | null };

export default function StuffListPage() {
  const [items, setItems] = useState<StuffItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const r = await api.get("/stuff", { params: { page: 1, page_size: 40 } });
        setItems(r.data?.items || []);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Персоны</h1>
      {loading ? (
        <div>Загрузка...</div>
      ) : (
        <div className={styles.grid}>
          {items.map((p) => (
            <Link key={p.id} href={`/stuff/${p.id}`} className={styles.card}>
              {p.photo ? (
                <img className={styles.photo} src={resolveMediaUrl(p.photo) || ""} alt={p.name} />
              ) : (
                <div className={styles.noPhoto} />
              )}
              <div className={styles.name}>{p.name}</div>
              {p.english_name ? <div className={styles.sub}>{p.english_name}</div> : null}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}


