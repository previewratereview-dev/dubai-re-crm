"use client";

import { useParams, useRouter } from "next/navigation";
import { useLead, useUpdateLead, useDeleteLead } from "@/hooks/use-leads";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatDate, formatCurrency } from "@/lib/utils";
import { ArrowLeft, Edit, Trash2 } from "lucide-react";

export default function LeadDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const { data: lead, isLoading } = useLead(id);
  const deleteLead = useDeleteLead();

  if (isLoading) return <div className="flex items-center justify-center h-64">Loading...</div>;
  if (!lead) return <div className="text-center py-12">Lead not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => router.back()}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <h1 className="text-3xl font-bold">{lead.first_name} {lead.last_name}</h1>
          <Badge className={`bg-${lead.status === "won" ? "green" : "blue"}-100 text-${lead.status === "won" ? "green" : "blue"}-800`}>
            {lead.status.replace(/_/g, " ")}
          </Badge>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm"><Edit className="h-4 w-4 mr-2" />Edit</Button>
          <Button variant="destructive" size="sm" onClick={() => { deleteLead.mutate(id); router.push("/leads"); }}>
            <Trash2 className="h-4 w-4 mr-2" />Delete
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Contact Info */}
        <Card>
          <CardHeader><CardTitle>Contact Information</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div><span className="text-sm text-muted-foreground">Phone</span><p>{lead.phone}</p></div>
            <div><span className="text-sm text-muted-foreground">Email</span><p>{lead.email || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Company</span><p>{lead.company || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Website</span><p>{lead.website || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Source</span><p>{lead.source || "-"}</p></div>
          </CardContent>
        </Card>

        {/* Property Preferences */}
        <Card>
          <CardHeader><CardTitle>Property Preferences</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div><span className="text-sm text-muted-foreground">Property Type</span><p>{lead.property_type || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Purpose</span><p>{lead.property_purpose || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Preferred Location</span><p>{lead.preferred_location || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Bedrooms</span><p>{lead.preferred_bedrooms || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Budget</span><p>{lead.min_budget ? `${formatCurrency(lead.min_budget)} - ${formatCurrency(lead.max_budget || 0)}` : "-"}</p></div>
          </CardContent>
        </Card>

        {/* Activity */}
        <Card>
          <CardHeader><CardTitle>Activity</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div><span className="text-sm text-muted-foreground">Priority</span><p className="capitalize">{lead.priority}</p></div>
            <div><span className="text-sm text-muted-foreground">Last Contacted</span><p>{lead.last_contacted_at ? formatDate(lead.last_contacted_at) : "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Next Follow Up</span><p>{lead.next_follow_up_at ? formatDate(lead.next_follow_up_at) : "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Call Outcome</span><p>{lead.call_outcome || "-"}</p></div>
            <div><span className="text-sm text-muted-foreground">Created</span><p>{formatDate(lead.created_at)}</p></div>
          </CardContent>
        </Card>
      </div>

      {/* Notes */}
      {lead.notes && (
        <Card>
          <CardHeader><CardTitle>Notes</CardTitle></CardHeader>
          <CardContent><p className="whitespace-pre-wrap">{lead.notes}</p></CardContent>
        </Card>
      )}

      {/* Tags */}
      {lead.tags?.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Tags</CardTitle></CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {lead.tags.map((tag) => (
                <Badge key={tag.id} style={{ backgroundColor: tag.color, color: "white" }}>{tag.name}</Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
