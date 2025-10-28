import { create } from "zustand";
import { api } from "../lib/api/client";
import { User, UserStats, CommentModeration, ModerationStats, Paginated, UserRole } from "@/lib/types";

type AdminState = {
  // Состояние
  loading: boolean;
  error: string | null;
  
  // Методы для управления пользователями
  getUsers: (page?: number, pageSize?: number, role?: UserRole, search?: string) => Promise<Paginated<User>>;
  updateUserRole: (userId: number, newRole: UserRole) => Promise<void>;
  verifyUserEmail: (userId: number) => Promise<void>;
  deleteUser: (userId: number) => Promise<void>;
  getUserStats: () => Promise<UserStats>;
  
  // Методы для модерации комментариев
  getPendingComments: (page?: number, pageSize?: number) => Promise<Paginated<CommentModeration>>;
  moderateComment: (commentId: number, action: "approve" | "reject" | "delete") => Promise<void>;
  getModerationStats: () => Promise<ModerationStats>;
};

export const useAdminStore = create<AdminState>((set) => ({
  loading: false,
  error: null,

  // Управление пользователями
  async getUsers(page = 1, pageSize = 20, role, search) {
    set({ loading: true, error: null });
    try {
      const params: any = { page, page_size: pageSize };
      if (role) params.role = role;
      if (search) params.search = search;
      
      const resp = await api.get<Paginated<User>>("/users", { params });
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get users" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async updateUserRole(userId: number, newRole: UserRole) {
    set({ loading: true, error: null });
    try {
      await api.put(`/users/${userId}/role`, null, {
        params: { new_role: newRole }
      });
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to update user role" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async verifyUserEmail(userId: number) {
    set({ loading: true, error: null });
    try {
      await api.put(`/users/${userId}/verify`);
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to verify user email" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async deleteUser(userId: number) {
    set({ loading: true, error: null });
    try {
      await api.delete(`/users/${userId}`);
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to delete user" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async getUserStats() {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<UserStats>("/users/stats");
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get user stats" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  // Модерация комментариев
  async getPendingComments(page = 1, pageSize = 20) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<Paginated<CommentModeration>>("/comments/moderation/pending", {
        params: { page, page_size: pageSize }
      });
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get pending comments" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async moderateComment(commentId: number, action: "approve" | "reject" | "delete") {
    set({ loading: true, error: null });
    try {
      await api.put(`/comments/${commentId}/moderate`, null, {
        params: { action }
      });
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to moderate comment" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async getModerationStats() {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<ModerationStats>("/comments/moderation/stats");
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get moderation stats" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },
}));
