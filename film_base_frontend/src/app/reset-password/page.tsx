"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { useAuthStore } from "@/store/auth";

type ResetForm = { password: string };

export default function ResetPasswordPage() {
  const sp = useSearchParams();
  const token = sp.get("token") || "";
  const router = useRouter();
  const { resetPassword } = useAuthStore();
  const { register, handleSubmit, formState: { errors, isSubmitting, isValid } } = useForm<ResetForm>({ mode: "onChange" });

  const onSubmit = handleSubmit(async (data) => {
    const ok = await resetPassword(token, data.password);
    if (ok) router.push("/login");
  });

  return (
    <div style={{ maxWidth: 420, margin: "24px auto", padding: "0 16px" }}>
      <h1 style={{ fontSize: 24, marginBottom: 12 }}>Сброс пароля</h1>
      <form onSubmit={onSubmit} noValidate style={{ display: "grid", gap: 12 }}>
        <input type="password" placeholder="Новый пароль" {...register("password", { required: "Укажите пароль", minLength: { value: 6, message: "Минимум 6 символов" } })} />
        {errors.password ? <div style={{ color: "#ef4444" }}>{errors.password.message}</div> : null}
        <button disabled={isSubmitting || !isValid}>Изменить</button>
      </form>
    </div>
  );
}


