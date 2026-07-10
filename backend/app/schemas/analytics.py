from pydantic import BaseModel


class AnalyticsPeriod(BaseModel):
    period: str  # daily, weekly, monthly, yearly
    start_date: str | None = None
    end_date: str | None = None


class CallAnalytics(BaseModel):
    total_calls: int = 0
    answered: int = 0
    missed: int = 0
    avg_duration: float = 0
    by_date: list[dict] = []
    by_agent: list[dict] = []
    outcomes: list[dict] = []


class LeadAnalytics(BaseModel):
    total_leads: int = 0
    converted: int = 0
    conversion_rate: float = 0
    by_status: list[dict] = []
    by_source: list[dict] = []
    avg_time_to_contact: float = 0
    avg_time_to_appointment: float = 0


class CampaignAnalytics(BaseModel):
    total_campaigns: int = 0
    active: int = 0
    completed: int = 0
    total_calls: int = 0
    appointments_booked: int = 0
    by_type: list[dict] = []


class EmployeePerformance(BaseModel):
    user_id: str
    name: str
    leads_assigned: int = 0
    leads_converted: int = 0
    calls_made: int = 0
    appointments_booked: int = 0
