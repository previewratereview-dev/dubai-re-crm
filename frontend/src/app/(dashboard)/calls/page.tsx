"use client";

import { useState } from "react";
import { useCalls } from "@/hooks/use-calls";
import { DataTable } from "@/components/shared/data-table";
import { Pagination } from "@/components/shared/pagination";
import { Badge } from "@/components/ui/badge";
import { formatDateTime, formatDuration } from "@/lib/utils";
import type { ColumnDef } from "@tanstack/react-table";
import type { Call } from "@/types";

export default function CallsPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useCalls({ page });

  const columns: ColumnDef<Call, unknown>[] = [
    { accessorKey: "phone_number", header: "Phone" },
    { accessorKey: "direction", header: "Direction", cell: ({ row }) => <span className="capitalize">{row.original.direction}</span> },
    { accessorKey: "duration", header: "Duration", cell: ({ row }) => formatDuration(row.original.duration) },
    { accessorKey: "outcome", header: "Outcome", cell: ({ row }) => row.original.outcome || "-" },
    {
      accessorKey: "appointment_created", header: "Appt Created",
      cell: ({ row }) => <Badge variant={row.original.appointment_created ? "default" : "secondary"}>
        {row.original.appointment_created ? "Yes" : "No"}
      </Badge>,
    },
    { accessorKey: "created_at", header: "Date", cell: ({ row }) => formatDateTime(row.original.created_at) },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">Call History</h1>
      {isLoading ? <div className="flex items-center justify-center h-64">Loading...</div> : (
        <>
          <DataTable columns={columns} data={data?.items || []} />
          <Pagination page={data?.page || 1} totalPages={data?.total_pages || 1} onPageChange={setPage} />
        </>
      )}
    </div>
  );
}
