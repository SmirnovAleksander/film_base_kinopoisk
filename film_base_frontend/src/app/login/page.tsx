"use client";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth";
import styles from "./page.module.css";
import { useForm } from "react-hook-form";

type LoginForm = { username: string; password: string };

export default function LoginPage() {
  const router = useRouter();
  const { login, loading, error } = useAuthStore();
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
    defaultValues: { username: "", password: "" },
    mode: "onSubmit",
  });

  const onSubmit = handleSubmit(async (data) => {
    const ok = await login(data.username, data.password);
    if (ok) router.push("/films");
  });

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Вход</h1>
      <form className={styles.form} onSubmit={onSubmit}>
        <input className={styles.input} placeholder="Email или логин" {...register("username", { required: "Укажите email или логин" })} />
        {errors.username ? <div className={styles.error}>{errors.username.message}</div> : null}
        <input className={styles.input} type="password" placeholder="Пароль" {...register("password", { required: "Укажите пароль" })} />
        {errors.password ? <div className={styles.error}>{errors.password.message}</div> : null}
        {error ? <div className={styles.error}>{error}</div> : null}
        <button className={styles.button} disabled={loading}>
          {loading ? "Входим..." : "Войти"}
        </button>
      </form>
    </div>
  );
}


