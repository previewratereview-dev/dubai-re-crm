"use client";

import { useState } from "react";
import { useLeads, useDeleteLead } from "@/hooks/use-leads";
import { DataTable } from "@/components/shared/data-table";
import { Pagination } from "@/components/shared/pagination";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { LEAD_STATUSES, LEAD_PRIORITIES } from "@/lib/constants";
import { formatDate } from "@/lib/utils";
import { Plus, Search, Upload, Download } from "lucide-react";
import { useRouter } from "next/navigation";
import type { ColumnDef } from "@tanstack/react-table";
import type { Lead } from "@/types";

const statusColor: Record<string, string> = {
  new: "bg-blue-100 text-blue-800",
  attempting_contact: "bg-yellow-100 text-yellow-800",
  connected: "bg-green-100 text-green-800",
  interested: "bg-emerald-100 text-emerald-800",
  appointment_scheduled: "bg-purple-100 text-purple-800",
  proposal_sent: "bg-indigo-100 text-indigo-800",
  negotiation: "bg-orange-100 text-orange-800",
  won: "bg-green-100 text-green-800",
  lost: "bg-red-100 text-red-800",
  follow_up: "bg-amber-100 text-amber-800",
};

const priorityColor: Record<string, string> = {
  low: "bg-gray-100 text-gray-800",
  medium: "bg-blue-100 text-blue-800",
  high: "bg-orange-100 text-orange-800",
  urgent: "bg-red-100 text-red-800",
};

export default function LeadsPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const { data, isLoading } = useLeads({ page, q: search || undefined, status: statusFilter || undefined });
  const deleteLead = useDeleteLead();
  const router = useRouter();

  const columns: ColumnDef<Lead, unknown>[] = [
    { accessorKey: "first_name", header: "Name", cell: ({ row }) => `${row.original.first_name} ${row.original.last_name}` },
    { accessorKey: "company", header: "Company", cell: ({ row }) => row.original.company || "-" },
    { accessorKey: "phone", header: "Phone" },
    { accessorKey: "email", header: "Email", cell: ({ row }) => row.original.email || "-" },
    {
      accessorKey: "status", header: "Status",
      cell: ({ row }) => (
        <Badge className={statusColor[row.original.status] || ""}>
          {row.original.status.replace(/_/g, " ")}
        </Badge>
      ),
    },
    {
      accessorKey: "priority", header: "Priority",
      cell: ({ row }) => (
        <Badge className={priorityColor[row.original.priority] || ""}>
          {row.original.priority}
        </Badge>
      ),
    },
    { accessorKey: "source", header: "Source", cell: ({ row }) => row.original.source || "-" },
    { accessorKey: "created_at", header: "Created", cell: ({ row }) => formatDate(row.original.created_at) },
    {
      id: "actions", header: "Actions",
      cell: ({ row }) => (
        <Button variant="ghost" size="sm" onClick={() => router.push(`/leads/${row.original.id}`)}>
          View
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Leads</h1>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm"><Upload className="h-4 w-4 mr-2" />Import</Button>
          <Button variant="outline" size="sm"><Download className="h-4 w-4 mr-2" />Export</Button>
          <Button size="sm" onClick={() => router.push("/leads/new")}><Plus className="h-4 w-4 mr-2" />Add Lead</Button>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input placeholder="Search leads..." className="pl-10" value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} />
        </div>
        <select
          className="h-10 rounded-md border border-input bg-background px-3 text-sm"
          value={statusFilter}
          onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
        >
          <option value="">All Statuses</option>
          {LEAD_STATUSES.map((s) => (
            <option key={s.value} value={s.value}>{s.label}</option>
          ))}
        </select>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">Loading...</div>
      ) : (
        <>
          <DataTable columns={columns} data={data?.items || []} />
          <Pagination page={data?.page || 1} totalPages={data?.total_pages || 1} onPageChange={setPage} />
        </>
      )}
    </div>
  );
}
