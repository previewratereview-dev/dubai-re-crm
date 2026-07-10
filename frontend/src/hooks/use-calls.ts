"use client";

import { useQuery } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { Call, PaginatedResponse } from "@/types";

export function useCalls(filters: { page?: number } = {}) {
  return useQuery<PaginatedResponse<Call>>({
    queryKey: ["calls", filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.page) params.set("page", String(filters.page));
      const { data } = await apiClient.get(`/api/calls?${params}`);
      return data;
    },
  });
}
