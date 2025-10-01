const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function resolveMediaUrl(src: string | null | undefined): string | null {
  if (!src) return null;
  if (/^https?:\/\//i.test(src)) return src;
  if (src.startsWith("/")) return API_BASE_URL.replace(/\/$/, "") + src;
  return API_BASE_URL.replace(/\/$/, "") + "/" + src.replace(/^\//, "");
}


