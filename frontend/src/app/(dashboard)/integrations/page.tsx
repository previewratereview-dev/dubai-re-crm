"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Calendar, Mail, Phone, Bot } from "lucide-react";

const integrations = [
  { name: "Google Calendar", icon: Calendar, status: "Configure in Settings", description: "Book appointments and sync with Google Calendar" },
  { name: "SMTP Email", icon: Mail, status: "Configure in Settings", description: "Send emails via SMTP server" },
  { name: "Twilio (Voice)", icon: Phone, status: "Managed by ElevenLabs", description: "Phone calls handled through ElevenLabs" },
  { name: "ElevenLabs AI", icon: Bot, status: "Connected", description: "AI voice agents for calling campaigns" },
];

export default function IntegrationsPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">Integrations</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {integrations.map((integration) => {
          const Icon = integration.icon;
          return (
            <Card key={integration.name}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                      <Icon className="h-5 w-5 text-primary" />
                    </div>
                    <CardTitle className="text-lg">{integration.name}</CardTitle>
                  </div>
                  <Badge variant={integration.status === "Connected" ? "default" : "secondary"}>
                    {integration.status}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{integration.description}</p>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
