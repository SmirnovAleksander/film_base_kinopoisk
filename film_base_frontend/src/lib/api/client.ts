import axios from "axios";
import Cookies from "js-cookie";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: false,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = Cookies.get("access_token");
  if (token) {
    config.headers = config.headers || {};
    (config.headers as any).Authorization = `Bearer ${token}`;
  }
  return config;
});

let isRefreshing = false;
let pendingQueue: Array<() => void> = [];

async function refreshToken(): Promise<string | null> {
  const refresh = Cookies.get("refresh_token");
  if (!refresh) return null;
  try {
    const resp = await api.post("/auth/refresh", { refresh_token: refresh });
    const { access_token, refresh_token } = resp.data || {};
    if (access_token) Cookies.set("access_token", access_token);
    if (refresh_token) Cookies.set("refresh_token", refresh_token);
    return access_token || null;
  } catch {
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    return null;
  }
}

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config || {};
    if (error?.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        await new Promise<void>((resolve) => pendingQueue.push(resolve));
      } else {
        isRefreshing = true;
        const newToken = await refreshToken();
        isRefreshing = false;
        pendingQueue.forEach((fn) => fn());
        pendingQueue = [];
        if (!newToken) return Promise.reject(error);
      }
      (original as any)._retry = true;
      const token = Cookies.get("access_token");
      if (token) {
        original.headers = original.headers || {};
        (original.headers as any).Authorization = `Bearer ${token}`;
      }
      return api(original);
    }
    return Promise.reject(error);
  }
);

export default api;


