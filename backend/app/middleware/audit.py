import uuid
import json
from datetime import datetime, timezone
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog


TRACKED_MODELS = {"Lead", "Customer", "Campaign", "Appointment", "Ticket", "Integration", "AIAgent"}


def setup_audit_listeners(session_factory):
    @event.listens_for(AsyncSession, "after_flush")
    def after_flush(session, flush_context):
        for obj in session.new:
            if obj.__class__.__name__ in TRACKED_MODELS:
                audit = AuditLog(
                    action="create",
                    entity_type=obj.__class__.__name__,
                    entity_id=obj.id,
                    new_values=_serialize(obj),
                    created_at=datetime.now(timezone.utc),
                )
                session.add(audit)
        for obj in session.dirty:
            if obj.__class__.__name__ in TRACKED_MODELS:
                audit = AuditLog(
                    action="update",
                    entity_type=obj.__class__.__name__,
                    entity_id=obj.id,
                    old_values={},
                    new_values=_serialize(obj),
                    created_at=datetime.now(timezone.utc),
                )
                session.add(audit)


def _serialize(obj) -> dict:
    try:
        data = {}
        for col in obj.__table__.columns:
            val = getattr(obj, col.name, None)
            if isinstance(val, uuid.UUID):
                val = str(val)
            elif isinstance(val, datetime):
                val = val.isoformat()
            elif hasattr(val, "value"):
                val = val.value
            data[col.name] = val
        return data
    except Exception:
        return {}
