export const LEAD_STATUSES = [
  { value: "new", label: "New", color: "bg-blue-100 text-blue-800" },
  { value: "attempting_contact", label: "Attempting Contact", color: "bg-yellow-100 text-yellow-800" },
  { value: "connected", label: "Connected", color: "bg-green-100 text-green-800" },
  { value: "interested", label: "Interested", color: "bg-emerald-100 text-emerald-800" },
  { value: "appointment_scheduled", label: "Appointment Scheduled", color: "bg-purple-100 text-purple-800" },
  { value: "proposal_sent", label: "Proposal Sent", color: "bg-indigo-100 text-indigo-800" },
  { value: "negotiation", label: "Negotiation", color: "bg-orange-100 text-orange-800" },
  { value: "won", label: "Won", color: "bg-green-100 text-green-800" },
  { value: "lost", label: "Lost", color: "bg-red-100 text-red-800" },
  { value: "busy", label: "Busy", color: "bg-gray-100 text-gray-800" },
  { value: "voicemail", label: "Voicemail", color: "bg-gray-100 text-gray-800" },
  { value: "wrong_number", label: "Wrong Number", color: "bg-red-100 text-red-800" },
  { value: "no_answer", label: "No Answer", color: "bg-gray-100 text-gray-800" },
  { value: "follow_up", label: "Follow Up", color: "bg-amber-100 text-amber-800" },
  { value: "do_not_contact", label: "Do Not Contact", color: "bg-red-100 text-red-800" },
] as const;

export const LEAD_PRIORITIES = [
  { value: "low", label: "Low", color: "bg-gray-100 text-gray-800" },
  { value: "medium", label: "Medium", color: "bg-blue-100 text-blue-800" },
  { value: "high", label: "High", color: "bg-orange-100 text-orange-800" },
  { value: "urgent", label: "Urgent", color: "bg-red-100 text-red-800" },
] as const;

export const CAMPAIGN_TYPES = [
  { value: "sales", label: "Sales" },
  { value: "follow_up", label: "Follow Up" },
  { value: "reminder", label: "Reminder" },
  { value: "survey", label: "Survey" },
  { value: "support", label: "Support" },
] as const;

export const CAMPAIGN_STATUSES = [
  { value: "draft", label: "Draft", color: "bg-gray-100 text-gray-800" },
  { value: "scheduled", label: "Scheduled", color: "bg-blue-100 text-blue-800" },
  { value: "running", label: "Running", color: "bg-green-100 text-green-800" },
  { value: "paused", label: "Paused", color: "bg-yellow-100 text-yellow-800" },
  { value: "completed", label: "Completed", color: "bg-emerald-100 text-emerald-800" },
  { value: "cancelled", label: "Cancelled", color: "bg-red-100 text-red-800" },
] as const;

export const ROLES = [
  { value: "super_admin", label: "Super Admin" },
  { value: "admin", label: "Admin" },
  { value: "sales", label: "Sales" },
  { value: "support", label: "Support" },
  { value: "developer", label: "Developer" },
  { value: "viewer", label: "Viewer" },
] as const;

export const PROPERTY_TYPES = [
  "apartment", "villa", "townhouse", "penthouse", "office", "land", "warehouse", "retail", "other"
] as const;

export const PROPERTY_PURPOSES = [
  { value: "buy", label: "Buy" },
  { value: "rent", label: "Rent" },
  { value: "invest", label: "Invest" },
] as const;

export const NAV_ITEMS = [
  { label: "Dashboard", href: "/dashboard", icon: "LayoutDashboard" },
  { label: "Leads", href: "/leads", icon: "Users" },
  { label: "Customers", href: "/customers", icon: "UserCheck" },
  { label: "Appointments", href: "/appointments", icon: "Calendar" },
  { label: "Campaigns", href: "/campaigns", icon: "Megaphone" },
  { label: "Call History", href: "/calls", icon: "Phone" },
  { label: "AI Agents", href: "/ai-agents", icon: "Bot" },
  { label: "Integrations", href: "/integrations", icon: "Plug" },
  { label: "Users", href: "/users", icon: "UsersRound" },
  { label: "Analytics", href: "/analytics", icon: "BarChart3" },
  { label: "Settings", href: "/settings", icon: "Settings" },
] as const;
