"use client";
import Link from "next/link";
import styles from "./Header.module.css";
import { useAuthStore } from "@/store/auth";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export default function Header() {
  const { user, logout } = useAuthStore();
  const { theme, setTheme, systemTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const current = theme === "system" ? systemTheme : theme;
  const label = mounted ? (current === "dark" ? "Светлая" : "Тёмная") : "Тема";
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          FilmBase
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
          <button className={styles.button} onClick={() => setTheme(current === "dark" ? "light" : "dark")} suppressHydrationWarning>
            {label}
          </button>
          {user ? (
            <>
              <span className={styles.username}>{user.username || user.email}</span>
              <button className={styles.button} onClick={logout}>Выйти</button>
            </>
          ) : null}
        </div>
      </div>
    </header>
  );
}


