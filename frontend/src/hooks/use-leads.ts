"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { Lead, PaginatedResponse } from "@/types";

interface LeadFilters {
  page?: number;
  per_page?: number;
  q?: string;
  status?: string;
  source?: string;
}

export function useLeads(filters: LeadFilters = {}) {
  return useQuery<PaginatedResponse<Lead>>({
    queryKey: ["leads", filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.page) params.set("page", String(filters.page));
      if (filters.per_page) params.set("per_page", String(filters.per_page));
      if (filters.q) params.set("q", filters.q);
      if (filters.status) params.set("status", filters.status);
      if (filters.source) params.set("source", filters.source);
      const { data } = await apiClient.get(`/api/leads?${params}`);
      return data;
    },
  });
}

export function useLead(id: string) {
  return useQuery<Lead>({
    queryKey: ["lead", id],
    queryFn: async () => {
      const { data } = await apiClient.get(`/api/leads/${id}`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCreateLead() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<Lead>) => {
      const { data: result } = await apiClient.post("/api/leads", data);
      return result;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["leads"] }),
  });
}

export function useUpdateLead() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<Lead> }) => {
      const { data: result } = await apiClient.put(`/api/leads/${id}`, data);
      return result;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["leads"] }),
  });
}

export function useDeleteLead() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/api/leads/${id}`);
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["leads"] }),
  });
}
