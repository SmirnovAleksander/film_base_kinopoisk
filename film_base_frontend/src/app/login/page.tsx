"use client";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth";
import styles from "./page.module.css";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

type LoginForm = { username: string; password: string };

export default function LoginPage() {
  const router = useRouter();
  const { login, loading, error } = useAuthStore();
  const { register, handleSubmit, formState: { errors, isSubmitting, isValid }, setFocus } = useForm<LoginForm>({
    defaultValues: { username: "", password: "" },
    mode: "onChange",
  });
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => { setFocus("username"); }, [setFocus]);

  const onSubmit = handleSubmit(async (data) => {
    const ok = await login(data.username, data.password);
    if (ok) router.push("/films");
  });

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Вход</h1>
      <form className={styles.form} onSubmit={onSubmit} noValidate>
        <input className={styles.input} placeholder="Email или логин" autoComplete="username" {...register("username", { required: "Укажите email или логин" })} />
        {errors.username ? <div className={styles.error}>{errors.username.message}</div> : null}
        <div className={styles.inputRow}>
          <input className={styles.input} type={showPassword ? "text" : "password"} placeholder="Пароль" autoComplete="current-password" {...register("password", { required: "Укажите пароль", minLength: { value: 6, message: "Минимум 6 символов" } })} />
          <button type="button" className={styles.toggle} onClick={() => setShowPassword((v) => !v)}>{showPassword ? "Скрыть" : "Показать"}</button>
        </div>
        {errors.password ? <div className={styles.error}>{errors.password.message}</div> : null}
        {error ? <div className={styles.error}>{error}</div> : null}
        <div className={styles.hint}>Используйте email или логин. Пароль не короче 6 символов.</div>
        <button className={styles.button} disabled={loading || isSubmitting || !isValid}>
          {loading || isSubmitting ? "Входим..." : "Войти"}
        </button>
      </form>
    </div>
  );
}


