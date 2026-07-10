"use client";

import { useQuery } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { DashboardStats } from "@/types";

export function useDashboard() {
  return useQuery<DashboardStats>({
    queryKey: ["dashboard"],
    queryFn: async () => {
      const { data } = await apiClient.get("/api/dashboard");
      return data;
    },
  });
}
