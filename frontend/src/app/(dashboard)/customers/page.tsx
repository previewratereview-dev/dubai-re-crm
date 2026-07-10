"use client";

import { useState } from "react";
import { useCustomers } from "@/hooks/use-customers";
import { DataTable } from "@/components/shared/data-table";
import { Pagination } from "@/components/shared/pagination";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import { useRouter } from "next/navigation";
import { formatDate } from "@/lib/utils";
import type { ColumnDef } from "@tanstack/react-table";
import type { Customer } from "@/types";

export default function CustomersPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const { data, isLoading } = useCustomers({ page, q: search || undefined });
  const router = useRouter();

  const columns: ColumnDef<Customer, unknown>[] = [
    { accessorKey: "first_name", header: "Name", cell: ({ row }) => `${row.original.first_name} ${row.original.last_name}` },
    { accessorKey: "company", header: "Company", cell: ({ row }) => row.original.company || "-" },
    { accessorKey: "phone", header: "Phone" },
    { accessorKey: "email", header: "Email" },
    { accessorKey: "city", header: "City", cell: ({ row }) => row.original.city || "-" },
    { accessorKey: "created_at", header: "Joined", cell: ({ row }) => formatDate(row.original.created_at) },
    {
      id: "actions", header: "Actions",
      cell: ({ row }) => (
        <Button variant="ghost" size="sm" onClick={() => router.push(`/customers/${row.original.id}`)}>View</Button>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Customers</h1>
      </div>
      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input placeholder="Search customers..." className="pl-10" value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} />
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
