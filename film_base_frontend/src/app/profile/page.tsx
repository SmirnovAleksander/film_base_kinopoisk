"use client";
import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/auth";
import styles from "./page.module.css";

export default function ProfilePage() {
  const { user, fetchMe, requestEmailVerify, logout, logoutAll } = useAuthStore();
  const [sent, setSent] = useState(false);

  useEffect(() => {
    fetchMe();
  }, [fetchMe]);

  async function onVerify() {
    const ok = await requestEmailVerify();
    setSent(ok);
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Профиль</h1>
      {!user ? (
        <div>Не авторизованы</div>
      ) : (
        <div className={styles.card}>
          <div className={styles.row}><span>ID</span><span>{user.id}</span></div>
          <div className={styles.row}><span>Email</span><span>{user.email}</span></div>
          <div className={styles.row}><span>Логин</span><span>{user.username || "—"}</span></div>
          <div className={styles.row}><span>Подтверждение</span><span>{user.is_email_verified ? "Подтверждён" : "Не подтверждён"}</span></div>
          <div className={styles.actions}>
            {!user.is_email_verified ? (
              <button className={styles.button} onClick={onVerify}>{sent ? "Письмо отправлено" : "Подтвердить email"}</button>
            ) : null}
            <button className={styles.button} onClick={logout}>Выйти</button>
            <button className={styles.button} onClick={logoutAll}>Выйти везде</button>
          </div>
        </div>
      )}
    </div>
  );
}


