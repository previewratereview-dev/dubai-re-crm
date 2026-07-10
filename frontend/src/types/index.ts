export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  is_active: boolean;
  avatar_url: string | null;
  last_login_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Lead {
  id: string;
  first_name: string;
  last_name: string;
  company: string | null;
  phone: string;
  email: string | null;
  website: string | null;
  address: string | null;
  city: string | null;
  state: string | null;
  country: string | null;
  zip_code: string | null;
  industry: string | null;
  source: string | null;
  status: string;
  assigned_user_id: string | null;
  priority: string;
  budget: number | null;
  notes: string | null;
  last_contacted_at: string | null;
  next_follow_up_at: string | null;
  call_outcome: string | null;
  property_type: string | null;
  property_purpose: string | null;
  preferred_location: string | null;
  preferred_bedrooms: number | null;
  preferred_bathrooms: number | null;
  min_budget: number | null;
  max_budget: number | null;
  currency: string;
  investment_timeline: string | null;
  nationality: string | null;
  tags: Tag[];
  created_at: string;
  updated_at: string;
}

export interface Customer {
  id: string;
  lead_id: string | null;
  first_name: string;
  last_name: string;
  company: string | null;
  phone: string;
  email: string;
  address: string | null;
  city: string | null;
  state: string | null;
  country: string | null;
  zip_code: string | null;
  industry: string | null;
  notes: string | null;
  purchase_history: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface Appointment {
  id: string;
  title: string;
  description: string | null;
  lead_id: string | null;
  customer_id: string | null;
  assigned_user_id: string;
  start_time: string;
  end_time: string;
  timezone: string;
  status: string;
  google_event_id: string | null;
  location: string | null;
  meeting_link: string | null;
  created_at: string;
  updated_at: string;
}

export interface Campaign {
  id: string;
  name: string;
  description: string | null;
  type: string;
  status: string;
  agent_id: string | null;
  scheduled_start: string | null;
  retry_rules: Record<string, unknown> | null;
  stats: Record<string, unknown> | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Call {
  id: string;
  call_id: string;
  direction: string;
  duration: number;
  phone_number: string;
  lead_id: string | null;
  customer_id: string | null;
  campaign_id: string | null;
  agent_id: string | null;
  twilio_sid: string | null;
  transcript_url: string | null;
  recording_url: string | null;
  outcome: string | null;
  appointment_created: boolean;
  lead_status_changed: boolean;
  metadata: Record<string, unknown> | null;
  created_at: string;
}

export interface Tag {
  id: string;
  name: string;
  color: string;
}

export interface AIAgent {
  id: string;
  name: string;
  agent_id: string;
  description: string | null;
  purpose: string | null;
  language: string;
  phone_number: string | null;
  status: string;
  knowledge_sources: unknown[] | null;
  prompt_version: string | null;
  last_updated: string | null;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  type: string;
  read: boolean;
  link: string | null;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface DashboardStats {
  today_calls: number;
  today_appointments: number;
  open_leads: number;
  follow_ups_due: number;
  pipeline_value: number;
  calls_answered: number;
  calls_missed: number;
  appointments_booked: number;
  conversion_rate: number;
  lead_sources: { source: string; count: number }[];
  recent_activity: Record<string, unknown>[];
  campaign_status: { status: string; count: number }[];
  upcoming_meetings: { id: string; title: string; time: string }[];
}
