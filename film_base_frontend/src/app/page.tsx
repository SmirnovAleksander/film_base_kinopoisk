// app/page.tsx
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
    }, [films, list]);

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
        }, 5500);

        intervalRef.current = id as unknown as number;
        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current);
            if (switchTimeoutRef.current) clearTimeout(switchTimeoutRef.current);
        };
    }, [films, currentIndex]);

    const currentFilm = films?.[currentIndex];

    return (
        <div className="pageRoot">
            <img
                ref={imgARef}
                className="bgImg"
                src=""
                alt=""
                style={{ opacity: activeSlotRef.current === "A" ? 1 : 0 }}
            />
            <img
                ref={imgBRef}
                className="bgImg"
                src=""
                alt=""
                style={{ opacity: activeSlotRef.current === "B" ? 1 : 0 }}
            />

            <div className="overlay" />

            <main className="heroWrap">
                <div className="heroCard">
                    <h1 className="title">FilmBase</h1>
                    <p className="lead">Каталог фильмов с авторизацией, поиском и закладками.</p>

                    <div className="ctaRow">
                        <Link className="btn" href="/films">Перейти к фильмам</Link>
                        {!user && <Link className="btn" href="/login">Войти</Link>}
                    </div>

                    <div className="now">
                        {currentFilm ? `Сейчас: ${currentFilm.title}` : (loading ? "Загрузка..." : "Нет фильмов")}
                    </div>
                </div>
            </main>
        </div>
    );
}
