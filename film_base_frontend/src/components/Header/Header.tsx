// components/Header/Header.tsx
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./Header.module.css";
import { useAuthStore } from "@/store/auth";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import clsx from "clsx";


export default function Header() {
    const { user } = useAuthStore();
    const { theme, setTheme, systemTheme } = useTheme();
    const [mounted, setMounted] = useState(false);
    const pathname = usePathname();

    useEffect(() => setMounted(true), []);
    const current = theme === "system" ? systemTheme : theme;
    const label = mounted ? (current === "dark" ? "Светлая" : "Тёмная") : "Тема";

    const showThemeToggle = pathname !== "/";
    const headerClass = clsx(styles.header, {
        [styles.transparent]: pathname === "/",
    });

    return (
        <header className={headerClass}>
            <div className={styles.container}>
                <Link href="/" className={styles.logo}>
                    <span>🎬</span>
                    <span>FilmBase</span>
                </Link>

                <nav className={styles.nav}>
                    <Link href="/films" className={styles.link}>Фильмы</Link>
                    <Link href="/stuff" className={styles.link}>Персоны</Link>
                    {user && <Link href="/history" className={styles.link}>История</Link>}
                    <Link href="/profile" className={styles.link}>Профиль</Link>
                    {!user && <Link href="/login" className={styles.link}>Войти</Link>}
                    {!user && <Link href="/register" className={styles.link}>Регистрация</Link>}
                </nav>

                <div className={styles.user}>
                    {user && (
                        <Link href="/profile" className={styles.username}>
                            {user.username || user.email || ""}
                        </Link>
                    )}
                    {showThemeToggle && (
                        <button
                            className={styles.button}
                            onClick={() => setTheme(current === "dark" ? "light" : "dark")}
                            suppressHydrationWarning
                        >
                            {label}
                        </button>
                    )}
                </div>
            </div>
        </header>
    );
}