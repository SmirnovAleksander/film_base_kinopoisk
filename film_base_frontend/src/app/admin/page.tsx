"use client";

import { useState, useEffect } from "react";
import { useAdminStore } from "@/store/admin";
import { useAuthStore } from "@/store/auth";
import { User, UserRole, UserStats, CommentModeration, ModerationStats } from "@/lib/types";

export default function AdminPanel() {
  const { user } = useAuthStore();
  const adminStore = useAdminStore();
  
  const [activeTab, setActiveTab] = useState<"users" | "moderation">("users");
  const [users, setUsers] = useState<User[]>([]);
  const [pendingComments, setPendingComments] = useState<CommentModeration[]>([]);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [moderationStats, setModerationStats] = useState<ModerationStats | null>(null);
  
  const [userPage, setUserPage] = useState(1);
  const [commentPage, setCommentPage] = useState(1);
  const [roleFilter, setRoleFilter] = useState<UserRole | "">("");
  const [searchQuery, setSearchQuery] = useState("");

  // Проверяем права доступа
  if (!user || (user.role !== "admin" && user.role !== "moderator")) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">Доступ запрещен</h1>
          <p className="text-gray-600">У вас нет прав для доступа к админ панели</p>
        </div>
      </div>
    );
  }

  // Загружаем данные
  useEffect(() => {
    loadUserStats();
    if (activeTab === "users") {
      loadUsers();
    } else {
      loadModerationStats();
      loadPendingComments();
    }
  }, [activeTab, userPage, commentPage, roleFilter, searchQuery]);

  const loadUsers = async () => {
    try {
      const result = await adminStore.getUsers(
        userPage, 
        20, 
        roleFilter || undefined, 
        searchQuery || undefined
      );
      setUsers(result.items);
    } catch (error) {
      console.error("Failed to load users:", error);
    }
  };

  const loadUserStats = async () => {
    try {
      const stats = await adminStore.getUserStats();
      setUserStats(stats);
    } catch (error) {
      console.error("Failed to load user stats:", error);
    }
  };

  const loadPendingComments = async () => {
    try {
      const result = await adminStore.getPendingComments(commentPage, 20);
      setPendingComments(result.items);
    } catch (error) {
      console.error("Failed to load pending comments:", error);
    }
  };

  const loadModerationStats = async () => {
    try {
      const stats = await adminStore.getModerationStats();
      setModerationStats(stats);
    } catch (error) {
      console.error("Failed to load moderation stats:", error);
    }
  };

  const handleRoleChange = async (userId: number, newRole: UserRole) => {
    try {
      await adminStore.updateUserRole(userId, newRole);
      loadUsers(); // Перезагружаем список
    } catch (error) {
      console.error("Failed to update user role:", error);
    }
  };

  const handleVerifyEmail = async (userId: number) => {
    try {
      await adminStore.verifyUserEmail(userId);
      loadUsers(); // Перезагружаем список
    } catch (error) {
      console.error("Failed to verify user email:", error);
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (!confirm("Вы уверены, что хотите удалить этого пользователя?")) return;
    
    try {
      await adminStore.deleteUser(userId);
      loadUsers(); // Перезагружаем список
    } catch (error) {
      console.error("Failed to delete user:", error);
    }
  };

  const handleModerateComment = async (commentId: number, action: "approve" | "reject" | "delete") => {
    try {
      await adminStore.moderateComment(commentId, action);
      loadPendingComments(); // Перезагружаем список
    } catch (error) {
      console.error("Failed to moderate comment:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Админ панель</h1>
        
        {/* Статистика */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {userStats && (
            <>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900">Всего пользователей</h3>
                <p className="text-3xl font-bold text-blue-600">{userStats.total_users}</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900">Подтвержденных</h3>
                <p className="text-3xl font-bold text-green-600">{userStats.verified_users}</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900">Новых за 30 дней</h3>
                <p className="text-3xl font-bold text-purple-600">{userStats.new_users_30d}</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900">Админов</h3>
                <p className="text-3xl font-bold text-red-600">{userStats.role_distribution.admin || 0}</p>
              </div>
            </>
          )}
        </div>

        {/* Табы */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6">
              <button
                onClick={() => setActiveTab("users")}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === "users"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                Управление пользователями
              </button>
              {user?.role === "admin" && (
                <button
                  onClick={() => setActiveTab("moderation")}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === "moderation"
                      ? "border-blue-500 text-blue-600"
                      : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  }`}
                >
                  Модерация комментариев
                </button>
              )}
            </nav>
          </div>

          <div className="p-6">
            {activeTab === "users" && (
              <div>
                {/* Фильтры */}
                <div className="flex gap-4 mb-6">
                  <select
                    value={roleFilter}
                    onChange={(e) => setRoleFilter(e.target.value as UserRole | "")}
                    className="px-3 py-2 border border-gray-300 rounded-md"
                  >
                    <option value="">Все роли</option>
                    <option value="user">Пользователь</option>
                    <option value="moderator">Модератор</option>
                    <option value="admin">Администратор</option>
                  </select>
                  
                  <input
                    type="text"
                    placeholder="Поиск по email или username..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                {/* Таблица пользователей */}
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Пользователь
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Роль
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Статус
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Дата регистрации
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Действия
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {users.map((user) => (
                        <tr key={user.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div>
                              <div className="text-sm font-medium text-gray-900">{user.email}</div>
                              <div className="text-sm text-gray-500">{user.username || "Без имени"}</div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <select
                              value={user.role}
                              onChange={(e) => handleRoleChange(user.id, e.target.value as UserRole)}
                              className="text-sm border border-gray-300 rounded px-2 py-1"
                            >
                              <option value="user">Пользователь</option>
                              <option value="moderator">Модератор</option>
                              <option value="admin">Администратор</option>
                            </select>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              user.is_email_verified 
                                ? "bg-green-100 text-green-800" 
                                : "bg-red-100 text-red-800"
                            }`}>
                              {user.is_email_verified ? "Подтвержден" : "Не подтвержден"}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {user.created_at ? new Date(user.created_at).toLocaleDateString() : "Неизвестно"}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                            {!user.is_email_verified && (
                              <button
                                onClick={() => handleVerifyEmail(user.id)}
                                className="text-green-600 hover:text-green-900"
                              >
                                Подтвердить
                              </button>
                            )}
                            <button
                              onClick={() => handleDeleteUser(user.id)}
                              className="text-red-600 hover:text-red-900"
                            >
                              Удалить
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {activeTab === "moderation" && (
              <div>
                {/* Статистика модерации */}
                {moderationStats && (
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-semibold">Всего комментариев</h4>
                      <p className="text-2xl font-bold">{moderationStats.total_comments}</p>
                    </div>
                    <div className="bg-yellow-50 p-4 rounded-lg">
                      <h4 className="font-semibold">На модерации</h4>
                      <p className="text-2xl font-bold text-yellow-600">{moderationStats.pending_comments}</p>
                    </div>
                    <div className="bg-green-50 p-4 rounded-lg">
                      <h4 className="font-semibold">Одобренных</h4>
                      <p className="text-2xl font-bold text-green-600">{moderationStats.status_distribution.approved || 0}</p>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-semibold">За 7 дней</h4>
                      <p className="text-2xl font-bold text-blue-600">{moderationStats.comments_7d}</p>
                    </div>
                  </div>
                )}

                {/* Таблица комментариев */}
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Комментарий
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Фильм
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Автор
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Дата
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Действия
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {pendingComments.map((comment) => (
                        <tr key={comment.id}>
                          <td className="px-6 py-4">
                            <div className="text-sm text-gray-900 max-w-xs truncate">
                              {comment.content}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {comment.film_title}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{comment.user_email}</div>
                            <div className="text-sm text-gray-500">{comment.username || "Без имени"}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {new Date(comment.created_at).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                            <button
                              onClick={() => handleModerateComment(comment.id, "approve")}
                              className="text-green-600 hover:text-green-900"
                            >
                              Одобрить
                            </button>
                            <button
                              onClick={() => handleModerateComment(comment.id, "reject")}
                              className="text-yellow-600 hover:text-yellow-900"
                            >
                              Отклонить
                            </button>
                            <button
                              onClick={() => handleModerateComment(comment.id, "delete")}
                              className="text-red-600 hover:text-red-900"
                            >
                              Удалить
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
