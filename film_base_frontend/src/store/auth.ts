import { create } from "zustand";
import Cookies from "js-cookie";
import api from "@/lib/api/client";
import { UserMe } from "@/lib/types";

type AuthState = {
  user: UserMe | null;
  loading: boolean;
  error: string | null;
  login: (loginOrEmail: string, password: string) => Promise<boolean>;
  register: (email: string, password: string, username?: string) => Promise<boolean>;
  fetchMe: () => Promise<void>;
  logout: () => Promise<void>;
};

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  loading: false,
  error: null,
  async login(loginOrEmail, password) {
    set({ loading: true, error: null });
    try {
      const form = new URLSearchParams();
      form.set("username", loginOrEmail);
      form.set("password", password);
      const resp = await api.post("/auth/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      const { access_token, refresh_token } = resp.data || {};
      if (access_token) Cookies.set("access_token", access_token);
      if (refresh_token) Cookies.set("refresh_token", refresh_token);
      await get().fetchMe();
      set({ loading: false });
      return true;
    } catch (e: any) {
      const msg = parseError(e);
      set({ loading: false, error: msg });
      return false;
    }
  },
  async register(email, password, username) {
    set({ loading: true, error: null });
    try {
      // Бэкенд ожидает query-параметры для простых типов, иначе 422
      await api.post("/auth/register", null, { params: { email, password, username } });
      set({ loading: false });
      return true;
    } catch (e: any) {
      const msg = parseError(e);
      set({ loading: false, error: msg });
      return false;
    }
  },
  async fetchMe() {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<UserMe>("/users/me");
      set({ user: resp.data, loading: false });
    } catch (e: any) {
      set({ user: null, loading: false });
    }
  },
  async logout() {
    try {
      const refresh = Cookies.get("refresh_token");
      if (refresh) {
        await api.post("/auth/logout", { refresh_token: refresh });
      }
    } catch {}
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    set({ user: null });
  },
}));

function parseError(e: any): string {
  const data = e?.response?.data;
  if (!data) return "Unexpected error";
  if (typeof data?.detail === "string") return data.detail;
  if (Array.isArray(data?.detail)) {
    const msgs = data.detail.map((d: any) => d?.msg || JSON.stringify(d)).join(", ");
    return msgs || "Validation error";
  }
  return data?.message || data?.error || "Request error";
}


