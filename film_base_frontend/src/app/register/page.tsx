"use client";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth";
import styles from "./page.module.css";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

type RegisterForm = { email: string; username?: string; password: string };

export default function RegisterPage() {
  const router = useRouter();
  const { register: registerAuth, loading, error } = useAuthStore();
  const { register, handleSubmit, formState: { errors, isSubmitting, isValid }, setFocus, watch } = useForm<RegisterForm>({
    defaultValues: { email: "", username: "", password: "" },
    mode: "onChange",
  });
  const [showPassword, setShowPassword] = useState(false);
  const password = watch("password");
  useEffect(() => { setFocus("email"); }, [setFocus]);

  const onSubmit = handleSubmit(async (data) => {
    const ok = await registerAuth(data.email, data.password, data.username);
    if (ok) router.push("/login");
  });

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Регистрация</h1>
      <form className={styles.form} onSubmit={onSubmit} noValidate>
        <input className={styles.input} placeholder="Email" autoComplete="email" {...register("email", { required: "Укажите email", pattern: { value: /.+@.+\..+/, message: "Некорректный email" } })} />
        {errors.email ? <div className={styles.error}>{errors.email.message}</div> : null}
        <input className={styles.input} placeholder="Логин" {...register("username")} />
        <div className={styles.inputRow}>
          <input className={styles.input} type={showPassword ? "text" : "password"} placeholder="Пароль" autoComplete="new-password" {...register("password", { required: "Укажите пароль", minLength: { value: 6, message: "Минимум 6 символов" } })} />
          <button type="button" className={styles.toggle} onClick={() => setShowPassword((v) => !v)}>{showPassword ? "Скрыть" : "Показать"}</button>
        </div>
        {errors.password ? <div className={styles.error}>{errors.password.message}</div> : null}
        <div className={styles.hint}>Пароль не короче 6 символов.</div>
        {error ? <div className={styles.error}>{error}</div> : null}
        <button className={styles.button} disabled={loading || isSubmitting || !isValid}>{loading || isSubmitting ? "Создаём..." : "Зарегистрироваться"}</button>
      </form>
    </div>
  );
}


