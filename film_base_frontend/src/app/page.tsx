"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useAuthStore } from "@/store/auth";
import { useFilmsStore } from "@/store/films";
import { resolveMediaUrl } from "@/lib/utils/url";

export default function Home() {
    const user = useAuthStore((s) => s.user);
    const films = useFilmsStore((s) => s.items);
    const list = useFilmsStore((s) => s.list);
    const loading = useFilmsStore((s) => s.loading);

    const [currentIndex, setCurrentIndex] = useState<number>(0);
    const imgARef = useRef<HTMLImageElement | null>(null);
    const imgBRef = useRef<HTMLImageElement | null>(null);
    const activeSlotRef = useRef<"A" | "B">("A");
    const intervalRef = useRef<number | null>(null);
    const switchTimeoutRef = useRef<number | null>(null);

    useEffect(() => {
        if (!films || films.length === 0) list(1, 20).catch(() => {});
    }, []);

    const setImgSlot = (slotRef: HTMLImageElement | null, src: string, alt: string) => {
        if (!slotRef) return;
        slotRef.src = src;
        slotRef.alt = alt;
        slotRef.style.transition = "none";
        slotRef.style.opacity = "0";
    };

    const doCrossfade = (
        newSlotRef: HTMLImageElement | null,
        oldSlotRef: HTMLImageElement | null,
        durationMs = 1000
    ) => {
        if (!newSlotRef) return;
        void newSlotRef.offsetWidth;
        newSlotRef.style.transition = `opacity ${durationMs}ms ease-in-out`;
        newSlotRef.style.opacity = "1";
        if (oldSlotRef) {
            oldSlotRef.style.transition = `opacity ${durationMs}ms ease-in-out`;
            oldSlotRef.style.opacity = "0";
        }
    };

    useEffect(() => {
        if (intervalRef.current) clearInterval(intervalRef.current);
        if (!films || films.length === 0) return;

        const initIfNeeded = () => {
            const a = imgARef.current;
            const b = imgBRef.current;
            const cur = films[currentIndex];
            if (!cur) return;
            const activeIsA = activeSlotRef.current === "A";
            const activeRef = activeIsA ? a : b;
            const inactiveRef = activeIsA ? b : a;
            if (activeRef && (activeRef.src === "" || activeRef.src == null)) {
                const url = resolveMediaUrl(cur.poster) || "";
                setImgSlot(activeRef, url, cur.title || "");
                setTimeout(() => {
                    if (activeRef) {
                        activeRef.style.transition = "opacity 600ms ease-in-out";
                        activeRef.style.opacity = "1";
                    }
                }, 50);
                if (inactiveRef) inactiveRef.style.opacity = "0";
            }
        };

        initIfNeeded();

        const id = window.setInterval(() => {
            if (!films || films.length === 0) return;
            let next = Math.floor(Math.random() * films.length);
            if (films.length > 1 && next === currentIndex) next = (next + 1) % films.length;

            const isAActive = activeSlotRef.current === "A";
            const activeRef = isAActive ? imgARef.current : imgBRef.current;
            const inactiveRef = isAActive ? imgBRef.current : imgARef.current;

            const nextFilm = films[next];
            const src = resolveMediaUrl(nextFilm.poster) || "";

            setImgSlot(inactiveRef, src, nextFilm.title || "");

            if (switchTimeoutRef.current) clearTimeout(switchTimeoutRef.current);
            switchTimeoutRef.current = window.setTimeout(() => {
                doCrossfade(inactiveRef, activeRef, 1000);
                activeSlotRef.current = isAActive ? "B" : "A";
                setCurrentIndex(next);
            }, 60);
        }, 5000);

        intervalRef.current = id as unknown as number;
        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current);
            if (switchTimeoutRef.current) clearTimeout(switchTimeoutRef.current);
        };
    }, [films, currentIndex]);

    if (!films || films.length === 0) {
        return (
            <div className="container" style={{ padding: 24 }}>
                <h1 style={{ fontSize: 28, marginBottom: 12 }}>Добро пожаловать в FilmBase</h1>
                <p className="muted" style={{ marginBottom: 16 }}>
                    Каталог фильмов с авторизацией, поиском и закладками.
                </p>
                <div style={{ display: "flex", gap: 12 }}>
                    <Link className="btn" href="/films">Перейти к фильмам</Link>
                    {!user && <Link className="btn" href="/login">Войти</Link>}
                </div>
                <div style={{ marginTop: 24, textAlign: "center", color: "#888" }}>
                    {loading ? "Загрузка фильмов..." : "Нет данных фильмов"}
                </div>
            </div>
        );
    }

    const currentFilm = films[currentIndex];

    return (
        <div
            className="container"
            style={{
                padding: 24,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
            }}
        >
            <h1 style={{ fontSize: 28, marginBottom: 12 }}>Добро пожаловать в FilmBase</h1>
            <p className="muted" style={{ marginBottom: 16 }}>
                Каталог фильмов с авторизацией, поиском и закладками.
            </p>

            {/* --- КЛИКАБЕЛЬНЫЙ СЛАЙДШОУ --- */}
            <Link
                href={`/films/${currentFilm?.id}`}
                style={{
                    width: "100%",
                    maxWidth: 1000,
                    height: 460,
                    position: "relative",
                    overflow: "hidden",
                    borderRadius: 12,
                    boxShadow: "0 8px 30px rgba(0,0,0,0.35)",
                    marginBottom: 18,
                    background: "#111",
                    marginTop: 40,
                    cursor: "pointer",
                    display: "block",
                }}
            >
                {/* слот A */}
                <img
                    ref={imgARef}
                    key="slot-a"
                    src=""
                    alt=""
                    style={{
                        position: "absolute",
                        inset: 0,
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        objectPosition: "center",
                        transition: "opacity 1s ease-in-out",
                        opacity: activeSlotRef.current === "A" ? 1 : 0,
                    }}
                />

                {/* слот B */}
                <img
                    ref={imgBRef}
                    key="slot-b"
                    src=""
                    alt=""
                    style={{
                        position: "absolute",
                        inset: 0,
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        objectPosition: "center",
                        transition: "opacity 1s ease-in-out",
                        opacity: activeSlotRef.current === "B" ? 1 : 0,
                    }}
                />

                {/* overlay с текстом */}
                <div
                    style={{
                        position: "absolute",
                        left: 0,
                        right: 0,
                        bottom: 0,
                        padding: "20px 24px",
                        background:
                            "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.65) 60%, rgba(0,0,0,0.85) 100%)",
                        color: "#fff",
                    }}
                >
                    <h2 style={{ margin: 0, fontSize: 28 }}>{currentFilm?.title}</h2>
                    <div style={{ marginTop: 6, opacity: 0.9 }}>
                        {currentFilm?.year ? `Год: ${currentFilm.year}` : null}
                        {currentFilm?.duration ? ` • ${currentFilm.duration} мин` : null}
                    </div>
                </div>
            </Link>

            <div style={{ display: "flex", gap: 12 }}>
                <Link className="btn" href="/films">Перейти к фильмам</Link>
                {!user && <Link className="btn" href="/login">Войти</Link>}
            </div>
        </div>
    );
}
