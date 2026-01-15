"use client"

import * as React from "react"
import {
  Film,
  Users,
  Tag,
  Globe,
  Newspaper,
  UserCog,
  Home,
} from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import Link from "next/link"
import { ROUTES } from "@/lib/config"
import { NavMain } from "./NavMain"

interface AdminSidebarProps extends React.ComponentProps<typeof Sidebar> {
  activeTab?: string
  counts?: {
    films?: number
    stuff?: number
    genres?: number
    countries?: number
    users?: number
  }
}

export function AdminSidebar({ activeTab, counts, ...props }: AdminSidebarProps) {

  const navMain = [
    {
      title: "Фильмы",
      url: "#films",
      icon: Film,
      count: counts?.films,
    },
    {
      title: "Участники",
      url: "#stuff",
      icon: Users,
      count: counts?.stuff,
    },
    {
      title: "Жанры",
      url: "#genres",
      icon: Tag,
      count: counts?.genres,
    },
    {
      title: "Страны",
      url: "#countries",
      icon: Globe,
      count: counts?.countries,
    },
    {
      title: "Пользователи",
      url: "#users",
      icon: UserCog,
      count: counts?.users,
    },
  ]

  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild className="data-[slot=sidebar-menu-button]:p-1.5!">
              <Link href={ROUTES.HOME} className="flex items-center gap-2">
                <Film className="size-5!" />
                <span className="text-base font-semibold">Film Base</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navMain} activeTab={activeTab} />
      </SidebarContent>
    </Sidebar>
  )
}

