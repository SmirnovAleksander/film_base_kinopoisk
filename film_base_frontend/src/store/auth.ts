import { create } from "zustand";
import Cookies from "js-cookie";
import api from "@/lib/api/client";
import { UserMe } from "@/lib/types";
import { persist } from "zustand/middleware";

export type AuthState = {
  user: UserMe | null;
  loading: boolean;
  error: string | null;
  login: (loginOrEmail: string, password: string) => Promise<boolean>;
  register: (email: string, password: string, username?: string) => Promise<boolean>;
  fetchMe: () => Promise<void>;
  logout: () => Promise<void>;
  logoutAll: () => Promise<void>;
  requestEmailVerify: () => Promise<boolean>;
  requestPasswordReset: (email: string) => Promise<boolean>;
  verifyEmail: (token: string) => Promise<boolean>;
  resetPassword: (token: string, newPassword: string) => Promise<boolean>;
};

export const useAuthStore = create<AuthState>()(
    persist(
        (set, get) => ({
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
                // опционально: явно удалить persisted storage (необязательно, т.к. set({user: null}) перезапишет)
                try {
                    localStorage.removeItem("auth-storage");
                } catch {}
            },

            async logoutAll() {
                try {
                    await api.post("/auth/logout-all");
                } catch {}
                Cookies.remove("access_token");
                Cookies.remove("refresh_token");
                set({ user: null });
                try {
                    localStorage.removeItem("auth-storage");
                } catch {}
            },

            async requestEmailVerify() {
                try {
                    const u = get().user;
                    if (!u) return false;
                    const r = await api.post("/auth/request-email-verify", null, { params: { user_id: u.id } });
                    return r.status >= 200 && r.status < 300;
                } catch {
                    return false;
                }
            },

            async requestPasswordReset(email: string) {
                try {
                    const r = await api.post("/auth/request-password-reset", null, { params: { email } });
                    return r.status >= 200 && r.status < 300;
                } catch {
                    return false;
                }
            },

            async verifyEmail(token: string) {
                try {
                    const r = await api.post("/auth/verify-email", null, { params: { token } });
                    await get().fetchMe();
                    return r.status >= 200 && r.status < 300;
                } catch {
                    return false;
                }
            },

            async resetPassword(token: string, newPassword: string) {
                try {
                    const r = await api.post("/auth/reset-password", null, { params: { token, new_password: newPassword } });
                    return r.status >= 200 && r.status < 300;
                } catch {
                    return false;
                }
            },
        }),

        {
            name: "auth-storage", // ключ в localStorage
            // сохраняем только user — не сохраняем loading, error и т.д.
            partialize: (state) => ({ user: state.user }),
            // version: 1, // можно указать версию и писать миграции, если структура изменится
            // onRehydrateStorage: () => (state) => { /* опционально обработать ре-гидрацию */ },
        }
    )
);

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


