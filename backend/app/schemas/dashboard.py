from pydantic import BaseModel


class DashboardStats(BaseModel):
    today_calls: int = 0
    today_appointments: int = 0
    open_leads: int = 0
    follow_ups_due: int = 0
    pipeline_value: float = 0
    calls_answered: int = 0
    calls_missed: int = 0
    appointments_booked: int = 0
    conversion_rate: float = 0
    lead_sources: list[dict] = []
    recent_activity: list[dict] = []
    campaign_status: list[dict] = []
    upcoming_meetings: list[dict] = []
