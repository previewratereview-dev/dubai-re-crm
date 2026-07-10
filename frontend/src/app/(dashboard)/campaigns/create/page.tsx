"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useCreateCampaign } from "@/hooks/use-campaigns";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { CAMPAIGN_TYPES } from "@/lib/constants";
import { ArrowLeft } from "lucide-react";

export default function CreateCampaignPage() {
  const router = useRouter();
  const createCampaign = useCreateCampaign();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [type, setType] = useState("sales");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createCampaign.mutateAsync({ name, description, type });
    router.push("/campaigns");
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <h1 className="text-3xl font-bold">New Campaign</h1>
      </div>

      <Card>
        <CardHeader><CardTitle>Campaign Details</CardTitle></CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Name</label>
              <Input value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Description</label>
              <Input value={description} onChange={(e) => setDescription(e.target.value)} />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Type</label>
              <Select value={type} onValueChange={setType}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  {CAMPAIGN_TYPES.map((t) => (
                    <SelectItem key={t.value} value={t.value}>{t.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button type="submit" disabled={createCampaign.isPending}>
              {createCampaign.isPending ? "Creating..." : "Create Campaign"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
