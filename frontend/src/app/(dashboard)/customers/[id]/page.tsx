"use client";

import { useParams, useRouter } from "next/navigation";
import { useCustomer } from "@/hooks/use-customers";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { formatDate } from "@/lib/utils";
import { ArrowLeft } from "lucide-react";

export default function CustomerDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const { data: customer, isLoading } = useCustomer(id);

  if (isLoading) return <div className="flex items-center justify-center h-64">Loading...</div>;
  if (!customer) return <div className="text-center py-12">Customer not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <h1 className="text-3xl font-bold">{customer.first_name} {customer.last_name}</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle>Contact</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div><span className="text-sm text-muted-foreground">Phone</span><p>{customer.phone}</p></div>
            <div><span className="text-sm text-muted-foreground">Email</span><p>{customer.email}</p></div>
            <div><span className="text-sm text-muted-foreground">Company</span><p>{customer.company || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">City</span><p>{customer.city || "-"}</p></div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Details</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div><span className="text-sm text-muted-foreground">Industry</span><p>{customer.industry || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Joined</span><p>{formatDate(customer.created_at)}</p></div>
          </CardContent>
        </Card>
      </div>

      {customer.notes && (
        <Card>
          <CardHeader><CardTitle>Notes</CardTitle></CardHeader>
          <CardContent><p className="whitespace-pre-wrap">{customer.notes}</p></CardContent>
        </Card>
      )}
    </div>
  );
}
