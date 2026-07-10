"use client";

import { useQuery } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { AIAgent, PaginatedResponse } from "@/types";

export default function AIAgentsPage() {
  const { data, isLoading } = useQuery<PaginatedResponse<AIAgent>>({
    queryKey: ["ai-agents"],
    queryFn: async () => {
      const { data } = await apiClient.get("/api/ai-agents");
      return data;
    },
  });

  if (isLoading) return <div className="flex items-center justify-center h-64">Loading...</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">AI Agents</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {data?.items?.map((agent) => (
          <Card key={agent.id}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{agent.name}</CardTitle>
                <Badge variant={agent.status === "active" ? "default" : "secondary"}>{agent.status}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-2">
              <p className="text-sm text-muted-foreground">{agent.description || "No description"}</p>
              <div className="text-sm"><span className="text-muted-foreground">Agent ID:</span> {agent.agent_id}</div>
              <div className="text-sm"><span className="text-muted-foreground">Language:</span> {agent.language}</div>
              <div className="text-sm"><span className="text-muted-foreground">Phone:</span> {agent.phone_number || "-"}</div>
            </CardContent>
          </Card>
        ))}
        {data?.items?.length === 0 && (
          <div className="col-span-full text-center py-12 text-muted-foreground">No AI agents configured yet</div>
        )}
      </div>
    </div>
  );
}
