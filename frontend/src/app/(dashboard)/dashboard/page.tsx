"use client";

import { useDashboard } from "@/hooks/use-dashboard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Phone, Calendar, Users, TrendingUp, Clock, PhoneOff, CalendarCheck, Target } from "lucide-react";
import { formatCurrency } from "@/lib/utils";

const statCards = [
  { key: "today_calls", label: "Today's Calls", icon: Phone },
  { key: "today_appointments", label: "Today's Appointments", icon: Calendar },
  { key: "open_leads", label: "Open Leads", icon: Users },
  { key: "follow_ups_due", label: "Follow Ups Due", icon: Clock },
  { key: "calls_answered", label: "Calls Answered", icon: Phone },
  { key: "calls_missed", label: "Calls Missed", icon: PhoneOff },
  { key: "appointments_booked", label: "Appointments Booked", icon: CalendarCheck },
  { key: "conversion_rate", label: "Conversion Rate", icon: Target, suffix: "%" },
];

export default function DashboardPage() {
  const { data: stats, isLoading } = useDashboard();

  if (isLoading) return <div className="flex items-center justify-center h-64">Loading dashboard...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map(({ key, label, icon: Icon, suffix }) => (
          <Card key={key}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
              <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {key === "pipeline_value"
                  ? formatCurrency(stats?.pipeline_value || 0)
                  : `${stats?.[key as keyof typeof stats] || 0}${suffix || ""}`}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Pipeline Value Highlight */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            Pipeline Value
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-4xl font-bold text-primary">{formatCurrency(stats?.pipeline_value || 0)}</p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Lead Sources */}
        <Card>
          <CardHeader><CardTitle>Lead Sources</CardTitle></CardHeader>
          <CardContent>
            {stats?.lead_sources?.length ? (
              <div className="space-y-3">
                {stats.lead_sources.map((source) => (
                  <div key={source.source} className="flex items-center justify-between">
                    <span className="text-sm">{source.source}</span>
                    <span className="text-sm font-medium">{source.count}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No lead sources data yet</p>
            )}
          </CardContent>
        </Card>

        {/* Campaign Status */}
        <Card>
          <CardHeader><CardTitle>Campaign Status</CardTitle></CardHeader>
          <CardContent>
            {stats?.campaign_status?.length ? (
              <div className="space-y-3">
                {stats.campaign_status.map((cs) => (
                  <div key={cs.status} className="flex items-center justify-between">
                    <span className="text-sm capitalize">{cs.status.replace("_", " ")}</span>
                    <span className="text-sm font-medium">{cs.count}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No campaigns yet</p>
            )}
          </CardContent>
        </Card>

        {/* Upcoming Meetings */}
        <Card className="lg:col-span-2">
          <CardHeader><CardTitle>Upcoming Meetings</CardTitle></CardHeader>
          <CardContent>
            {stats?.upcoming_meetings?.length ? (
              <div className="space-y-3">
                {stats.upcoming_meetings.map((m) => (
                  <div key={m.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                    <span className="font-medium">{m.title}</span>
                    <span className="text-sm text-muted-foreground">{new Date(m.time).toLocaleString()}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No upcoming meetings</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
