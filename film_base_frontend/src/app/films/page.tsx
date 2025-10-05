"use client";
import { useEffect, useState } from "react";
import { useFilmsStore } from "@/store/films";
import styles from "./page.module.css";
import { resolveMediaUrl } from "@/lib/utils/url";
import Link from "next/link";
import { useShallow } from "zustand/react/shallow";
import type { FilmsState } from "../../store/films";
import {useTheme} from "next-themes";

const VISIBLE_COUNT = 3;

export default function FilmsPage() {
    const { items, page, pageSize, loading, list, search, totalKnown} = useFilmsStore(
        useShallow((s: FilmsState) => ({
            items: s.items,
            page: s.page,
            pageSize: s.pageSize,
            loading: s.loading,
            list: s.list,
            search: s.search,
            totalKnown: s.totalKnown
        }))
    );
    const { theme, systemTheme } = useTheme();
    const currentTheme = theme === "system" ? systemTheme : theme;

    const [q, setQ] = useState("");
    const [brokenPosters, setBrokenPosters] = useState<Record<string | number, boolean>>({});
    const [visiblePages, setVisiblePages] = useState<number[]>(
        Array.from({ length: VISIBLE_COUNT }, (_, i) => i + 1)
    );
    const [showStartButton, setShowStartButton] = useState(false);
    const totalItems = totalKnown;
    let totalPages = null;
    if (totalItems !== undefined) {
        totalPages = Math.ceil(totalItems / pageSize);
    }

    useEffect(() => {
        list(page ?? 1, pageSize);
        if (page && page >= visiblePages[visiblePages.length - 1]) {
            let newVisible = [...visiblePages];
            const last = visiblePages[visiblePages.length - 1];
            const next = last + 1;
            newVisible = newVisible.slice(1).concat(next);

            setVisiblePages(newVisible);
            if (page && page > VISIBLE_COUNT) {
                setShowStartButton(true);
            }
        }
    }, []);

    const goToPage = (newPage: number) => {
        list(newPage, pageSize);
    };

    const handlePageClick = (p: number) => {
        const lastVisible = visiblePages[visiblePages.length - 1];

        if (p === lastVisible && totalPages !== null && totalPages > 3) {
            const next = lastVisible + 1;
            setVisiblePages((prev) => prev.slice(1).concat(next));
            setShowStartButton(true);
        }

        goToPage(p);
    };

    const handleNext = () => {
        const current = page ?? 1;
        const lastVisible = visiblePages[visiblePages.length - 1];

        if (current === lastVisible) {
            const next = lastVisible + 1;
            setVisiblePages((prev) => prev.slice(1).concat(next));
            setShowStartButton(true);
            goToPage(next);
        } else {
            const next = current + 1;
            goToPage(next);
        }
    };

    const handleStart = () => {
        setVisiblePages(Array.from({ length: VISIBLE_COUNT }, (_, i) => i + 1));
        setShowStartButton(false);
        goToPage(1);
    };

    const renderPager = () => {
        return (
            <div className={styles.pagerContent}>
                {showStartButton ? (
                    <button
                        className={styles.pagerContent__item}
                        onClick={handleStart}
                        aria-label="К началу"
                    >
                        К началу
                    </button>
                ) : null}

                {visiblePages.map((p) => (
                    totalPages != null && p <= totalPages && (
                        <button
                            key={p}
                            className={styles.pagerContent__item}
                            style={page === p ?
                                currentTheme === "dark" ?
                                    {background: "rgba(255, 255, 255, 0.15)"}
                                    : {background: "rgba(0, 0, 0, 0.15)"}
                                : {}
                            }
                            onClick={() => handlePageClick(p)}
                        >
                            {p}
                        </button>
                    )
                ))}
                {totalPages != null && page + 1 <= totalPages  ?(
                    <button className={styles.pagerContent__item} onClick={handleNext}>
                        Дальше
                    </button>
                ) : null}

            </div>
        );
    };

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Фильмы</h1>

            <div className={styles.searchRow}>
                <input
                    className={styles.input}
                    placeholder="Поиск по названию"
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                />
                <button className={styles.button} onClick={() => search(q, 1, 20)}>
                    Искать
                </button>
            </div>

            {loading ? (
                <div>Загрузка...</div>
            ) : (
                <div className={styles.grid}>
                    {items.map((f) => (
                        <Link key={f.id} href={`/films/${f.id}`} className={styles.card}>
                            {!brokenPosters[f.id] && f.poster ? (
                                <img
                                    className={styles.poster}
                                    src={resolveMediaUrl(f.poster) || ""}
                                    alt={f.title}
                                    onError={() => setBrokenPosters((prev) => ({ ...prev, [f.id]: true }))}
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
                                {f.full_description ? <div className={styles.desc}>{f.full_description}</div> : null}
                            </div>
                        </Link>
                    ))}
                </div>
            )}

            <div className={styles.pagerContent}>{renderPager()}</div>
        </div>
    );
}
