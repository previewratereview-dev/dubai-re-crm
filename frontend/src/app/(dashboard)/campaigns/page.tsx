"use client";

import { useCampaigns, useStartCampaign, useCancelCampaign } from "@/hooks/use-campaigns";
import { DataTable } from "@/components/shared/data-table";
import { Pagination } from "@/components/shared/pagination";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus, Play, XCircle } from "lucide-react";
import { useRouter } from "next/navigation";
import { formatDate } from "@/lib/utils";
import type { ColumnDef } from "@tanstack/react-table";
import type { Campaign } from "@/types";
import { useState } from "react";

const statusColor: Record<string, string> = {
  draft: "bg-gray-100 text-gray-800",
  scheduled: "bg-blue-100 text-blue-800",
  running: "bg-green-100 text-green-800",
  paused: "bg-yellow-100 text-yellow-800",
  completed: "bg-emerald-100 text-emerald-800",
  cancelled: "bg-red-100 text-red-800",
};

export default function CampaignsPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useCampaigns({ page });
  const startCampaign = useStartCampaign();
  const cancelCampaign = useCancelCampaign();
  const router = useRouter();

  const columns: ColumnDef<Campaign, unknown>[] = [
    { accessorKey: "name", header: "Name" },
    { accessorKey: "type", header: "Type", cell: ({ row }) => <span className="capitalize">{row.original.type.replace("_", " ")}</span> },
    {
      accessorKey: "status", header: "Status",
      cell: ({ row }) => <Badge className={statusColor[row.original.status] || ""}>{row.original.status}</Badge>,
    },
    { accessorKey: "created_at", header: "Created", cell: ({ row }) => formatDate(row.original.created_at) },
    {
      id: "actions", header: "Actions",
      cell: ({ row }) => (
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => router.push(`/campaigns/${row.original.id}`)}>View</Button>
          {row.original.status === "draft" && (
            <Button variant="ghost" size="sm" onClick={() => startCampaign.mutate(row.original.id)}>
              <Play className="h-4 w-4 mr-1" />Start
            </Button>
          )}
          {row.original.status === "running" && (
            <Button variant="ghost" size="sm" onClick={() => cancelCampaign.mutate(row.original.id)}>
              <XCircle className="h-4 w-4 mr-1" />Cancel
            </Button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Campaigns</h1>
        <Button size="sm" onClick={() => router.push("/campaigns/create")}><Plus className="h-4 w-4 mr-2" />New Campaign</Button>
      </div>
      {isLoading ? <div className="flex items-center justify-center h-64">Loading...</div> : (
        <>
          <DataTable columns={columns} data={data?.items || []} />
          <Pagination page={data?.page || 1} totalPages={data?.total_pages || 1} onPageChange={setPage} />
        </>
      )}
    </div>
  );
}
