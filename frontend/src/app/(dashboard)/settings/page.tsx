"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>

      <Card>
        <CardHeader><CardTitle>SMTP Configuration</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">SMTP Host</label>
              <Input placeholder="smtp.gmail.com" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">SMTP Port</label>
              <Input placeholder="587" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Username</label>
              <Input placeholder="your-email@gmail.com" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Password</label>
              <Input type="password" placeholder="••••••••" />
            </div>
          </div>
          <Button>Save SMTP Settings</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle>Google Calendar</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Client ID</label>
            <Input placeholder="Google Calendar Client ID" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Client Secret</label>
            <Input type="password" placeholder="Google Calendar Client Secret" />
          </div>
          <Button>Connect Google Calendar</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle>ElevenLabs Configuration</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">
            ElevenLabs agents and voice settings are managed directly in the ElevenLabs dashboard.
            This platform stores agent metadata for campaign management.
          </p>
          <div className="space-y-2">
            <label className="text-sm font-medium">Tools API Key</label>
            <Input placeholder="Shared secret for ElevenLabs tool calls" />
          </div>
          <Button>Save Configuration</Button>
        </CardContent>
      </Card>
    </div>
  );
}
