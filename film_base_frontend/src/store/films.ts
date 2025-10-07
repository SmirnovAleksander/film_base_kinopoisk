import { FilmListItem, Paginated, FilmDetails } from "@/lib/types";
import { create } from "zustand";
import api from "@/lib/api/client";

export type FilmsState = {
    items: FilmListItem[];
    page: number;
    pageSize: number;
    totalKnown?: number;
    loading: boolean;
    error: string | null;
    query: string;
    list: (page?: number, pageSize?: number) => Promise<void>;
    search: (query: string, page?: number, pageSize?: number) => Promise<void>;
    filter: (params: Record<string, any>) => Promise<void>;
    getById: (id: number) => Promise<FilmDetails>;
};
// Нормализуем ответ от сервера в удобную camelCase структуру
function normalizePaginated(resp: any, defaultPage = 1, defaultPageSize = 20) {
    const data = resp?.data ?? {};
    const headers = resp?.headers ?? {};

    // items
    const items: FilmListItem[] = Array.isArray(data.items) ? data.items : [];

    // page
    const page: number = Number(data.page ?? defaultPage) || defaultPage;

    // pageSize: поддерживаем и page_size (snake_case) и pageSize (camelCase)
    const pageSize: number = Number(data.page_size ?? data.pageSize ?? defaultPageSize) || defaultPageSize;

    // totalCount: тело или заголовок X-Total-Count
    const totalCountFromBody = data.total_count ?? data.totalCount ?? data.total;
    let totalCount: number | undefined = typeof totalCountFromBody === "number" ? totalCountFromBody : undefined;

    if (totalCount == null && headers["x-total-count"] != null) {
        const v = Number(headers["x-total-count"]);
        if (!Number.isNaN(v)) totalCount = v;
    }

    // fallback: если пришло меньше элементов чем pageSize => это последняя страница
    if (totalCount == null && Array.isArray(items) && items.length < pageSize) {
        totalCount = (page - 1) * pageSize + items.length;




    }return { items, page, pageSize, totalCount } as {
        items: FilmListItem[];
        page: number;
        pageSize: number;
        totalCount?: number;
    };
}

export const useFilmsStore = create<FilmsState>((set, get) => ({
    items: [],
    page: 1,
    pageSize: 12,
    totalKnown: undefined,
    loading: false,
    error: null,
    query: "",

    async list(page = 1, pageSize = 10) {
        set({ loading: true, error: null });
        try {
            const resp = await api.get<Paginated<FilmListItem>>("/films", {
                params: { page, page_size: pageSize },
            });

            const normalized = normalizePaginated(resp, page, pageSize);

            set((state) => ({
                items: normalized.items,
                page: normalized.page,
                pageSize: normalized.pageSize,
                loading: false,
                totalKnown: typeof normalized.totalCount === "number" ? normalized.totalCount : state.totalKnown,
            }));
        } catch (e: any) {
            set({ loading: false, error: e?.response?.data?.detail ?? e?.message ?? "Load error" });
        }
    },

    async search(query, page = 1, pageSize = 20) {
        set({ loading: true, error: null, query });
        try {
            const resp = await api.get<Paginated<FilmListItem>>("/films/search", {
                params: { query, lang: "ru", page, page_size: pageSize },
            });

            const normalized = normalizePaginated(resp, page, pageSize);

            set((state) => ({
                items: normalized.items,
                page: normalized.page,
                pageSize: normalized.pageSize,
                loading: false,
                totalKnown: typeof normalized.totalCount === "number" ? normalized.totalCount : state.totalKnown,
            }));
        } catch (e: any) {
            set({ loading: false, error: e?.response?.data?.detail ?? e?.message ?? "Search error" });
        }
    },

    async filter(params) {
        set({ loading: true, error: null });
        try {
            const resp = await api.get<Paginated<FilmListItem>>("/films/filter", { params });

            // page и page_size могут приходить в ответе — используем нормализацию
            const normalized = normalizePaginated(resp, get().page, get().pageSize);

            set((state) => ({
                items: normalized.items,
                page: normalized.page,
                pageSize: normalized.pageSize,
                loading: false,
                totalKnown: typeof normalized.totalCount === "number" ? normalized.totalCount : state.totalKnown,
            }));
        } catch (e: any) {
            set({ loading: false, error: e?.response?.data?.detail ?? e?.message ?? "Filter error" });
        }
    },

    async getById(id: number) {
        const resp = await api.get<FilmDetails>(`/films/${id}`);
        return resp.data;
    },
}));