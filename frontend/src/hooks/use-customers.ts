"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { Customer, PaginatedResponse } from "@/types";

export function useCustomers(filters: { page?: number; q?: string } = {}) {
  return useQuery<PaginatedResponse<Customer>>({
    queryKey: ["customers", filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.page) params.set("page", String(filters.page));
      if (filters.q) params.set("q", filters.q);
      const { data } = await apiClient.get(`/api/customers?${params}`);
      return data;
    },
  });
}

export function useCustomer(id: string) {
  return useQuery<Customer>({
    queryKey: ["customer", id],
    queryFn: async () => {
      const { data } = await apiClient.get(`/api/customers/${id}`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCreateCustomer() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<Customer>) => {
      const { data: result } = await apiClient.post("/api/customers", data);
      return result;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["customers"] }),
  });
}

export function useUpdateCustomer() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<Customer> }) => {
      const { data: result } = await apiClient.put(`/api/customers/${id}`, data);
      return result;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["customers"] }),
  });
}
