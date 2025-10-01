"use client";
import { useForm } from "react-hook-form";
import { useAuthStore } from "@/store/auth";

type FormT = { email: string };

export default function ForgotPasswordPage() {
  const { requestPasswordReset } = useAuthStore();
  const { register, handleSubmit, formState: { errors, isSubmitting, isValid } } = useForm<FormT>({ mode: "onChange" });
  const onSubmit = handleSubmit(async (data) => {
    await requestPasswordReset(data.email);
    alert("Если email существует, письмо отправлено");
  });
  return (
    <div style={{ maxWidth: 420, margin: "24px auto", padding: "0 16px" }}>
      <h1 style={{ fontSize: 24, marginBottom: 12 }}>Восстановление пароля</h1>
      <form onSubmit={onSubmit} noValidate style={{ display: "grid", gap: 12 }}>
        <input placeholder="Ваш email" {...register("email", { required: "Укажите email" })} />
        {errors.email ? <div style={{ color: "#ef4444" }}>{errors.email.message}</div> : null}
        <button disabled={isSubmitting || !isValid}>Отправить письмо</button>
      </form>
    </div>
  );
}


