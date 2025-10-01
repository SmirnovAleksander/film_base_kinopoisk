"use client";
import Link from "next/link";
import styles from "./Header.module.css";
import { useAuthStore } from "@/store/auth";

export default function Header() {
  const { user, logout } = useAuthStore();
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          FilmBase
        </Link>
        <nav className={styles.nav}>
          <Link href="/films" className={styles.link}>Фильмы</Link>
          <Link href="/login" className={styles.link}>Войти</Link>
          <Link href="/register" className={styles.link}>Регистрация</Link>
        </nav>
        <div className={styles.user}>
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


