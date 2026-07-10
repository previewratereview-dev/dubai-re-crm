"use client";

import { useQuery } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import { DataTable } from "@/components/shared/data-table";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import type { ColumnDef } from "@tanstack/react-table";
import type { User, PaginatedResponse } from "@/types";

export default function UsersPage() {
  const { data, isLoading } = useQuery<PaginatedResponse<User>>({
    queryKey: ["users"],
    queryFn: async () => {
      const { data } = await apiClient.get("/api/users");
      return data;
    },
  });

  const columns: ColumnDef<User, unknown>[] = [
    {
      accessorKey: "first_name", header: "Name",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm">
            {row.original.first_name[0]}{row.original.last_name[0]}
          </div>
          <span>{row.original.first_name} {row.original.last_name}</span>
        </div>
      ),
    },
    { accessorKey: "email", header: "Email" },
    { accessorKey: "role", header: "Role", cell: ({ row }) => <Badge className="capitalize">{row.original.role.replace("_", " ")}</Badge> },
    { accessorKey: "is_active", header: "Status", cell: ({ row }) => <Badge variant={row.original.is_active ? "default" : "secondary"}>{row.original.is_active ? "Active" : "Inactive"}</Badge> },
    { accessorKey: "last_login_at", header: "Last Login", cell: ({ row }) => row.original.last_login_at ? formatDate(row.original.last_login_at) : "Never" },
  ];

  if (isLoading) return <div className="flex items-center justify-center h-64">Loading...</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">Users</h1>
      <DataTable columns={columns} data={data?.items || []} />
    </div>
  );
}
