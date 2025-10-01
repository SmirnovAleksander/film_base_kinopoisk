import Link from "next/link";

export default function Home() {
  return (
    <div className="container" style={{ padding: 24 }}>
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>Добро пожаловать в FilmBase</h1>
      <p className="muted" style={{ marginBottom: 16 }}>Каталог фильмов с авторизацией, поиском и закладками.</p>
      <div style={{ display: "flex", gap: 12 }}>
        <Link className="btn" href="/films">Перейти к фильмам</Link>
        <Link className="btn" href="/login">Войти</Link>
      </div>
    </div>
  );
}
