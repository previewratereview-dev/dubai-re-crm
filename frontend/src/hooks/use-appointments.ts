"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { Appointment, PaginatedResponse } from "@/types";

export function useAppointments(filters: { page?: number } = {}) {
  return useQuery<PaginatedResponse<Appointment>>({
    queryKey: ["appointments", filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.page) params.set("page", String(filters.page));
      const { data } = await apiClient.get(`/api/appointments?${params}`);
      return data;
    },
  });
}

export function useUpcomingAppointments() {
  return useQuery<Appointment[]>({
    queryKey: ["appointments", "upcoming"],
    queryFn: async () => {
      const { data } = await apiClient.get("/api/appointments/upcoming");
      return data;
    },
  });
}

export function useBookAppointment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (data: Record<string, unknown>) => {
      const { data: result } = await apiClient.post("/api/appointments", data);
      return result;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["appointments"] }),
  });
}

export function useCancelAppointment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/api/appointments/${id}`);
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["appointments"] }),
  });
}
