"use client";

import { useState } from "react";
import { useAppointments, useCancelAppointment } from "@/hooks/use-appointments";
import { DataTable } from "@/components/shared/data-table";
import { Pagination } from "@/components/shared/pagination";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDateTime } from "@/lib/utils";
import type { ColumnDef } from "@tanstack/react-table";
import type { Appointment } from "@/types";

const statusColor: Record<string, string> = {
  scheduled: "bg-blue-100 text-blue-800",
  confirmed: "bg-green-100 text-green-800",
  completed: "bg-emerald-100 text-emerald-800",
  cancelled: "bg-red-100 text-red-800",
  no_show: "bg-gray-100 text-gray-800",
};

export default function AppointmentsPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useAppointments({ page });
  const cancelAppointment = useCancelAppointment();

  const columns: ColumnDef<Appointment, unknown>[] = [
    { accessorKey: "title", header: "Title" },
    { accessorKey: "start_time", header: "Start", cell: ({ row }) => formatDateTime(row.original.start_time) },
    { accessorKey: "end_time", header: "End", cell: ({ row }) => formatDateTime(row.original.end_time) },
    { accessorKey: "location", header: "Location", cell: ({ row }) => row.original.location || "-" },
    {
      accessorKey: "status", header: "Status",
      cell: ({ row }) => <Badge className={statusColor[row.original.status] || ""}>{row.original.status}</Badge>,
    },
    {
      id: "actions", header: "Actions",
      cell: ({ row }) => (
        row.original.status !== "cancelled" && row.original.status !== "completed" ? (
          <Button variant="ghost" size="sm" onClick={() => cancelAppointment.mutate(row.original.id)}>Cancel</Button>
        ) : null
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">Appointments</h1>
      {isLoading ? <div className="flex items-center justify-center h-64">Loading...</div> : (
        <>
          <DataTable columns={columns} data={data?.items || []} />
          <Pagination page={data?.page || 1} totalPages={data?.total_pages || 1} onPageChange={setPage} />
        </>
      )}
    </div>
  );
}
