"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/auth";

export default function VerifyEmailPage() {
  const sp = useSearchParams();
  const token = sp.get("token") || "";
  const { verifyEmail } = useAuthStore();
  const [status, setStatus] = useState<string>("Подтверждаем...");
  const router = useRouter();

  useEffect(() => {
    async function run() {
      const ok = token ? await verifyEmail(token) : false;
      setStatus(ok ? "Email подтверждён" : "Не удалось подтвердить");
      setTimeout(() => router.push("/profile"), 1500);
    }
    run();
  }, [token, verifyEmail, router]);

  return <div style={{ padding: 24 }}>{status}</div>;
}


