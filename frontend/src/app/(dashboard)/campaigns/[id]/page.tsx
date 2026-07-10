"use client";

import { useParams, useRouter } from "next/navigation";
import { useCampaign, useStartCampaign, useCancelCampaign } from "@/hooks/use-campaigns";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { ArrowLeft, Play, Pause, XCircle } from "lucide-react";

export default function CampaignDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const { data: campaign, isLoading } = useCampaign(id);
  const startCampaign = useStartCampaign();
  const cancelCampaign = useCancelCampaign();

  if (isLoading) return <div className="flex items-center justify-center h-64">Loading...</div>;
  if (!campaign) return <div className="text-center py-12">Campaign not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => router.back()}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <h1 className="text-3xl font-bold">{campaign.name}</h1>
          <Badge>{campaign.status}</Badge>
        </div>
        <div className="flex gap-2">
          {campaign.status === "draft" && (
            <Button size="sm" onClick={() => startCampaign.mutate(campaign.id)}>
              <Play className="h-4 w-4 mr-2" />Start
            </Button>
          )}
          {campaign.status === "running" && (
            <Button variant="destructive" size="sm" onClick={() => cancelCampaign.mutate(campaign.id)}>
              <XCircle className="h-4 w-4 mr-2" />Cancel
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader><CardTitle>Details</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div><span className="text-sm text-muted-foreground">Type</span><p className="capitalize">{campaign.type.replace("_", " ")}</p></div>
            <div><span className="text-sm text-muted-foreground">Status</span><p className="capitalize">{campaign.status}</p></div>
            <div><span className="text-sm text-muted-foreground">Created</span><p>{formatDate(campaign.created_at)}</p></div>
          </CardContent>
        </Card>
        <Card className="lg:col-span-2">
          <CardHeader><CardTitle>Description</CardTitle></CardHeader>
          <CardContent><p>{campaign.description || "No description"}</p></CardContent>
        </Card>
      </div>

      {campaign.stats && Object.keys(campaign.stats).length > 0 && (
        <Card>
          <CardHeader><CardTitle>Statistics</CardTitle></CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(campaign.stats).map(([key, value]) => (
                <div key={key}>
                  <span className="text-sm text-muted-foreground capitalize">{key.replace(/_/g, " ")}</span>
                  <p className="text-2xl font-bold">{String(value)}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
