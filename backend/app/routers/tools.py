import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import verify_tools_api_key
from app.schemas.lead import LeadCreate, LeadUpdate
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.schemas.note import NoteCreate
from app.schemas.appointment import AppointmentCreate
from app.schemas.ticket import TicketCreate
from app.services.lead import LeadService
from app.services.customer import CustomerService
from app.services.note import NoteService
from app.services.appointment import AppointmentService
from app.services.ticket import TicketService
from app.services.call import CallService
from app.services.email import send_email
from app.models.lead import LeadStatus

router = APIRouter(prefix="/api/tools", tags=["ElevenLabs Tools"])


@router.post("/create-lead")
async def create_lead(
    data: LeadCreate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = LeadService(db)
    lead = await service.create(data)
    return {"success": True, "lead_id": str(lead.id), "message": f"Lead {lead.first_name} {lead.last_name} created"}


@router.post("/update-lead")
async def update_lead(
    lead_id: uuid.UUID,
    data: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = LeadService(db)
    lead = await service.update(lead_id, data)
    return {"success": True, "lead_id": str(lead.id), "message": "Lead updated"}


@router.post("/get-lead")
async def get_lead(
    lead_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = LeadService(db)
    lead = await service.get_by_id(lead_id)
    return {
        "success": True,
        "lead": {
            "id": str(lead.id),
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "phone": lead.phone,
            "email": lead.email,
            "company": lead.company,
            "status": lead.status.value if lead.status else None,
            "property_type": lead.property_type,
            "property_purpose": lead.property_purpose,
            "preferred_location": lead.preferred_location,
            "budget": float(lead.budget) if lead.budget else None,
        }
    }


@router.post("/search-leads")
async def search_leads(
    query: str = "",
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = LeadService(db)
    status_filter = LeadStatus(status) if status else None
    leads, total = await service.search(query=query, status_filter=status_filter, per_page=10)
    return {
        "success": True,
        "total": total,
        "leads": [
            {
                "id": str(l.id),
                "first_name": l.first_name,
                "last_name": l.last_name,
                "phone": l.phone,
                "email": l.email,
                "status": l.status.value if l.status else None,
            }
            for l in leads
        ]
    }


@router.post("/create-customer")
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = CustomerService(db)
    customer = await service.create(data)
    return {"success": True, "customer_id": str(customer.id), "message": f"Customer {customer.first_name} created"}


@router.post("/update-customer")
async def update_customer(
    customer_id: uuid.UUID,
    data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = CustomerService(db)
    customer = await service.update(customer_id, data)
    return {"success": True, "customer_id": str(customer.id), "message": "Customer updated"}


@router.post("/search-customer")
async def search_customer(
    query: str = "",
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = CustomerService(db)
    customers, total = await service.search(query=query, per_page=10)
    return {
        "success": True,
        "total": total,
        "customers": [
            {
                "id": str(c.id),
                "first_name": c.first_name,
                "last_name": c.last_name,
                "phone": c.phone,
                "email": c.email,
            }
            for c in customers
        ]
    }


@router.post("/create-note")
async def create_note(
    data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = NoteService(db)
    note = await service.create(data)
    return {"success": True, "note_id": str(note.id), "message": "Note created"}


@router.post("/book-appointment")
async def book_appointment(
    data: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = AppointmentService(db)
    appt = await service.book(data)
    return {
        "success": True,
        "appointment_id": str(appt.id),
        "message": f"Appointment booked for {appt.start_time.isoformat()}"
    }


@router.post("/check-availability")
async def check_availability(
    user_id: uuid.UUID,
    date: str,
    duration_minutes: int = 30,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = AppointmentService(db)
    slots = await service.check_availability(user_id, date, duration_minutes)
    return {"success": True, "available_slots": slots}


@router.post("/reschedule")
async def reschedule_appointment(
    appointment_id: uuid.UUID,
    new_start_time: str,
    new_end_time: str,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    from datetime import datetime
    service = AppointmentService(db)
    from app.schemas.appointment import AppointmentUpdate
    appt = await service.reschedule(appointment_id, AppointmentUpdate(
        start_time=datetime.fromisoformat(new_start_time),
        end_time=datetime.fromisoformat(new_end_time),
    ))
    return {"success": True, "appointment_id": str(appt.id), "message": "Appointment rescheduled"}


@router.post("/cancel-appointment")
async def cancel_appointment(
    appointment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = AppointmentService(db)
    await service.cancel(appointment_id)
    return {"success": True, "message": "Appointment cancelled"}


@router.post("/get-upcoming-appointments")
async def get_upcoming_appointments(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = AppointmentService(db)
    appts = await service.get_upcoming(limit=limit)
    return {
        "success": True,
        "appointments": [
            {
                "id": str(a.id),
                "title": a.title,
                "start_time": a.start_time.isoformat(),
                "end_time": a.end_time.isoformat(),
                "status": a.status.value,
            }
            for a in appts
        ]
    }


@router.post("/send-email")
async def send_email_tool(
    to_email: str,
    subject: str,
    body: str,
    _: str = Depends(verify_tools_api_key),
):
    success = send_email(to_email, subject, body)
    return {"success": success, "message": "Email sent" if success else "Failed to send email"}


@router.post("/send-sms")
async def send_sms_tool(
    to_phone: str,
    message: str,
    _: str = Depends(verify_tools_api_key),
):
    return {"success": True, "message": "SMS sending configured via Twilio in ElevenLabs"}


@router.post("/create-ticket")
async def create_ticket(
    data: TicketCreate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = TicketService(db)
    ticket = await service.create(data)
    return {"success": True, "ticket_id": str(ticket.id), "message": "Support ticket created"}


@router.post("/create-followup")
async def create_followup(
    lead_id: uuid.UUID,
    follow_up_date: str,
    notes: str | None = None,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    from datetime import datetime
    service = LeadService(db)
    update = LeadUpdate(next_follow_up_at=datetime.fromisoformat(follow_up_date), notes=notes)
    await service.update(lead_id, update)
    return {"success": True, "message": "Follow-up scheduled"}


@router.post("/update-call-outcome")
async def update_call_outcome(
    lead_id: uuid.UUID,
    outcome: str,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_tools_api_key),
):
    service = LeadService(db)
    status_map = {
        "interested": LeadStatus.INTERESTED,
        "not_interested": LeadStatus.LOST,
        "busy": LeadStatus.BUSY,
        "voicemail": LeadStatus.VOICEMAIL,
        "wrong_number": LeadStatus.WRONG_NUMBER,
        "no_answer": LeadStatus.NO_ANSWER,
        "follow_up": LeadStatus.FOLLOW_UP,
        "do_not_contact": LeadStatus.DO_NOT_CONTACT,
        "connected": LeadStatus.CONNECTED,
        "appointment_booked": LeadStatus.APPOINTMENT_SCHEDULED,
    }
    update = LeadUpdate(
        call_outcome=outcome,
        status=status_map.get(outcome, LeadStatus.CONNECTED),
    )
    await service.update(lead_id, update)
    return {"success": True, "message": f"Call outcome '{outcome}' recorded"}


@router.post("/get-company-information")
async def get_company_information(
    _: str = Depends(verify_tools_api_key),
):
    return {
        "success": True,
        "company": {
            "name": "Dubai Real Estate",
            "industry": "Real Estate",
            "services": ["Property Sales", "Property Rentals", "Investment Consulting"],
            "location": "Dubai, UAE",
        }
    }
