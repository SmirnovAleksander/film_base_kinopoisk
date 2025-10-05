"use client";
import { useEffect, useState } from "react";
import { useFilmsStore } from "@/store/films";
import styles from "./page.module.css";
import { resolveMediaUrl } from "@/lib/utils/url";
import Link from "next/link";
import { useShallow } from "zustand/react/shallow";
import type { FilmsState } from "../../store/films";
import { useTheme } from "next-themes";

const VISIBLE_COUNT = 3;

export default function FilmsPage() {
    const { items, page, pageSize, loading, list, search, totalKnown } = useFilmsStore(
        useShallow((s: FilmsState) => ({
            items: s.items,
            page: s.page,
            pageSize: s.pageSize,
            loading: s.loading,
            list: s.list,
            search: s.search,
            totalKnown: s.totalKnown,
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

    // локальная выбранная страница — мгновенная подсветка при клике
    const [selectedPageLocal, setSelectedPageLocal] = useState<number>(page ?? 1);
    useEffect(() => {
        setSelectedPageLocal(page ?? 1);
    }, [page]);

    const totalItems = totalKnown;
    const totalPages = totalItems ? Math.ceil(totalItems / pageSize) : null;

    // начальная загрузка
    useEffect(() => {
        list(page ?? 1, pageSize);
        if (page && page >= visiblePages[visiblePages.length - 1] && totalPages !== null && totalPages > page) {
            let newVisible = [...visiblePages];
            const last = visiblePages[visiblePages.length - 1];
            const next = last + 1;
            newVisible = newVisible.slice(1).concat(next);

            setVisiblePages(newVisible);
            if (page && page > VISIBLE_COUNT) {
                setShowStartButton(true);
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []); // оставляем как была начальная логика

    const goToPage = (newPage: number) => {
        list(newPage, pageSize);
    };

    // единый обработчик перехода — минимальные изменения логики внутри
    const selectPage = (target: number) => {
        if (totalPages !== null && (target < 1 || target > totalPages)) return;

        // мгновенно подсвечиваем целевую страницу
        setSelectedPageLocal(target);

        // корректируем видимую зону относительно target (минимальные изменения: slice/concat)
        setVisiblePages((prev) => {
            const firstVisible = prev[0];
            const lastVisible = prev[prev.length - 1];

            // если целевая справа или равна правой границе — сдвинуть вправо (как у тебя было)
            if (target >= lastVisible && lastVisible < (totalPages ?? Infinity)) {
                if (totalPages !== null && lastVisible >= totalPages) return prev;
                return prev.slice(1).concat(lastVisible + 1);
            }

            // если целевая слева или равна левой границе — сдвинуть влево
            if (target <= firstVisible && firstVisible > 1) {
                if (firstVisible <= 1) return prev;
                return [firstVisible - 1, ...prev.slice(0, -1)];
            }

            // иначе — внутри окна, не меняем
            return prev;
        });

        setShowStartButton(target > VISIBLE_COUNT);
        goToPage(target);
    };

    const handleStart = () => {
        setVisiblePages(Array.from({ length: VISIBLE_COUNT }, (_, i) => i + 1));
        setShowStartButton(false);
        setSelectedPageLocal(1);
        goToPage(1);
    };

    const renderPager = () => {
        const nextExists = totalPages != null && (page ?? 1) + 1 <= totalPages;

        return (
            <div className={styles.pagerContent}>
                {showStartButton ? (
                    <button className={styles.pagerContent__item} onClick={handleStart} aria-label="К началу">
                        К началу
                    </button>
                ) : null}

                {visiblePages.map((p) => (
                    totalPages != null && p <= totalPages && (
                        <button
                            key={p}
                            className={styles.pagerContent__item}
                            style={
                                selectedPageLocal === p
                                    ? currentTheme === "dark"
                                        ? { background: "rgba(255, 255, 255, 0.15)" }
                                        : { background: "rgba(0, 0, 0, 0.15)" }
                                    : {}
                            }
                            onClick={() => selectPage(p)}
                        >
                            {p}
                        </button>
                    )
                ))}

                {nextExists ? (
                    <button className={styles.pagerContent__item} onClick={() => selectPage((page ?? 1) + 1)}>
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
