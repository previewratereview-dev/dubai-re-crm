"use client";

import { useQuery } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Phone, Users, Megaphone } from "lucide-react";

export default function AnalyticsPage() {
  const { data: calls } = useQuery({
    queryKey: ["analytics", "calls"],
    queryFn: async () => (await apiClient.get("/api/analytics/calls")).data,
  });
  const { data: leads } = useQuery({
    queryKey: ["analytics", "leads"],
    queryFn: async () => (await apiClient.get("/api/analytics/leads")).data,
  });
  const { data: campaigns } = useQuery({
    queryKey: ["analytics", "campaigns"],
    queryFn: async () => (await apiClient.get("/api/analytics/campaigns")).data,
  });

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Analytics</h1>

      {/* Call Analytics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Calls</CardTitle>
            <Phone className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent><p className="text-2xl font-bold">{calls?.total_calls || 0}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Answered</CardTitle>
            <Phone className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent><p className="text-2xl font-bold">{calls?.answered || 0}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Missed</CardTitle>
            <Phone className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent><p className="text-2xl font-bold">{calls?.missed || 0}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Avg Duration</CardTitle>
          </CardHeader>
          <CardContent><p className="text-2xl font-bold">{calls?.avg_duration || 0}s</p></CardContent>
        </Card>
      </div>

      {/* Lead Analytics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Leads</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent><p className="text-2xl font-bold">{leads?.total_leads || 0}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Converted</CardTitle>
            <Users className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent><p className="text-2xl font-bold">{leads?.converted || 0}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Conversion Rate</CardTitle>
          </CardHeader>
          <CardContent><p className="text-2xl font-bold">{leads?.conversion_rate || 0}%</p></CardContent>
        </Card>
      </div>

      {/* Lead by Status */}
      {leads?.by_status?.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Leads by Status</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-2">
              {leads.by_status.map((s: { status: string; count: number }) => (
                <div key={s.status} className="flex items-center justify-between">
                  <span className="text-sm capitalize">{s.status.replace(/_/g, " ")}</span>
                  <span className="font-medium">{s.count}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
