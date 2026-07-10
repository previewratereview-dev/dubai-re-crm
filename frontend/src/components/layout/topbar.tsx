"use client";

import { useAuth } from "@/providers/auth-provider";
import { useTheme } from "@/providers/theme-provider";
import { Moon, Sun, Bell, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export function Topbar() {
  const { user, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const router = useRouter();

  return (
    <header className="h-16 border-b bg-card flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
          {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </Button>
      </div>
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.push("/notifications")}>
          <Bell className="h-5 w-5" />
        </Button>
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-medium">
            {user?.first_name?.[0]}{user?.last_name?.[0]}
          </div>
          <div className="hidden md:block">
            <p className="text-sm font-medium">{user?.first_name} {user?.last_name}</p>
            <p className="text-xs text-muted-foreground capitalize">{user?.role?.replace("_", " ")}</p>
          </div>
        </div>
        <Button variant="outline" size="sm" onClick={logout}>Logout</Button>
      </div>
    </header>
  );
}
