"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { Campaign, PaginatedResponse } from "@/types";

export function useCampaigns(filters: { page?: number } = {}) {
  return useQuery<PaginatedResponse<Campaign>>({
    queryKey: ["campaigns", filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.page) params.set("page", String(filters.page));
      const { data } = await apiClient.get(`/api/campaigns?${params}`);
      return data;
    },
  });
}

export function useCampaign(id: string) {
  return useQuery<Campaign>({
    queryKey: ["campaign", id],
    queryFn: async () => {
      const { data } = await apiClient.get(`/api/campaigns/${id}`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCreateCampaign() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (data: Record<string, unknown>) => {
      const { data: result } = await apiClient.post("/api/campaigns", data);
      return result;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["campaigns"] }),
  });
}

export function useStartCampaign() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data } = await apiClient.post(`/api/campaigns/${id}/start`);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["campaigns"] }),
  });
}

export function usePauseCampaign() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data } = await apiClient.post(`/api/campaigns/${id}/pause`);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["campaigns"] }),
  });
}

export function useCancelCampaign() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data } = await apiClient.post(`/api/campaigns/${id}/cancel`);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["campaigns"] }),
  });
}
