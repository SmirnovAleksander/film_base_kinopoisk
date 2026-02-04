"use client"

import * as React from "react"
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

interface NavMainProps {
  items: {
    title: string
    url: string
    icon: React.ElementType
    count?: number
  }[]
  activeTab?: string
}

export function NavMain({ items, activeTab }: NavMainProps) {
  const handleClick = (url: string) => {
    window.history.pushState(null, '', url)
    window.dispatchEvent(new HashChangeEvent('hashchange'))
  }

  return (
    <SidebarMenu className="p-2">
      {items.map((item) => {
        const Icon = item.icon
        const isActive = activeTab === item.url
        return (
          <SidebarMenuItem key={item.title}>
            <SidebarMenuButton
              onClick={() => handleClick(item.url)}
              isActive={isActive}
              tooltip={item.title}
            >
              <Icon />
              <span>{item.title}</span>
              {item.count !== undefined && (
                <span className="ml-auto text-xs text-muted-foreground">
                  {item.count}
                </span>
              )}
            </SidebarMenuButton>
          </SidebarMenuItem>
        )
      })}
    </SidebarMenu>
  )
}

