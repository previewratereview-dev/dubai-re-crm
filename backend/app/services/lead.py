import uuid
import csv
import io
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lead import Lead, LeadStatus
from app.models.tag import Tag
from app.repositories.lead import LeadRepository
from app.schemas.lead import LeadCreate, LeadUpdate, LeadBulkUpdate


class LeadService:
    def __init__(self, db: AsyncSession):
        self.repo = LeadRepository(db)
        self.db = db

    async def search(
        self, query: str | None = None, status_filter: LeadStatus | None = None,
        assigned_user_id: uuid.UUID | None = None, source: str | None = None,
        page: int = 1, per_page: int = 20
    ) -> tuple[list[Lead], int]:
        return await self.repo.search(query, status_filter, assigned_user_id, source, page, per_page)

    async def get_by_id(self, id: uuid.UUID) -> Lead:
        lead = await self.repo.get_by_id(id)
        if not lead:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
        return lead

    async def create(self, data: LeadCreate, user_id: uuid.UUID | None = None) -> Lead:
        tag_ids = data.tag_ids
        lead_data = data.model_dump(exclude={"tag_ids"})
        lead = await self.repo.create(**lead_data, created_by=user_id)
        if tag_ids:
            tags = (await self.db.execute(select(Tag).where(Tag.id.in_(tag_ids)))).scalars().all()
            lead.tags = list(tags)
            await self.db.flush()
        return lead

    async def update(self, id: uuid.UUID, data: LeadUpdate) -> Lead:
        update_data = data.model_dump(exclude_unset=True)
        tag_ids = update_data.pop("tag_ids", None)
        lead = await self.repo.update(id, **update_data)
        if not lead:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
        if tag_ids is not None:
            tags = (await self.db.execute(select(Tag).where(Tag.id.in_(tag_ids)))).scalars().all()
            lead.tags = list(tags)
            await self.db.flush()
        return lead

    async def delete(self, id: uuid.UUID) -> bool:
        return await self.repo.soft_delete(id)

    async def bulk_update(self, data: LeadBulkUpdate) -> int:
        count = 0
        for lead_id in data.lead_ids:
            update_fields = {}
            if data.status:
                update_fields["status"] = data.status
            if data.assigned_user_id:
                update_fields["assigned_user_id"] = data.assigned_user_id
            if data.priority:
                update_fields["priority"] = data.priority
            if update_fields:
                await self.repo.update(lead_id, **update_fields)
                count += 1
        return count

    async def import_csv(self, csv_content: str, user_id: uuid.UUID | None = None) -> dict:
        reader = csv.DictReader(io.StringIO(csv_content))
        imported = 0
        errors = []
        for i, row in enumerate(reader):
            try:
                phone = row.get("phone") or row.get("Phone") or row.get("PHONE")
                if not phone:
                    errors.append(f"Row {i+1}: missing phone")
                    continue
                data = LeadCreate(
                    first_name=row.get("first_name") or row.get("First Name", ""),
                    last_name=row.get("last_name") or row.get("Last Name", ""),
                    phone=phone,
                    email=row.get("email") or row.get("Email"),
                    company=row.get("company") or row.get("Company"),
                    city=row.get("city") or row.get("City"),
                    country=row.get("country") or row.get("Country"),
                    source=row.get("source") or row.get("Source"),
                )
                await self.create(data, user_id)
                imported += 1
            except Exception as e:
                errors.append(f"Row {i+1}: {str(e)}")
        return {"imported": imported, "errors": errors}

    async def export_csv(self, lead_ids: list[uuid.UUID] | None = None) -> str:
        if lead_ids:
            leads = []
            for lid in lead_ids:
                lead = await self.repo.get_by_id(lid)
                if lead:
                    leads.append(lead)
        else:
            leads, _ = await self.repo.get_all(page=1, per_page=10000)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["first_name", "last_name", "phone", "email", "company", "city", "country", "status", "source"])
        for lead in leads:
            writer.writerow([
                lead.first_name, lead.last_name, lead.phone, lead.email,
                lead.company, lead.city, lead.country, lead.status.value, lead.source,
            ])
        return output.getvalue()

    async def merge(self, primary_id: uuid.UUID, duplicate_ids: list[uuid.UUID]) -> Lead:
        primary = await self.get_by_id(primary_id)
        for dup_id in duplicate_ids:
            dup = await self.repo.get_by_id(dup_id)
            if dup:
                if not primary.email and dup.email:
                    primary.email = dup.email
                if not primary.company and dup.company:
                    primary.company = dup.company
                if not primary.notes and dup.notes:
                    primary.notes = dup.notes
                await self.repo.soft_delete(dup_id)
        await self.db.flush()
        return primary

    async def assign_user(self, lead_id: uuid.UUID, user_id: uuid.UUID) -> Lead:
        lead = await self.repo.update(lead_id, assigned_user_id=user_id)
        if not lead:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
        return lead

    async def get_follow_ups_due(self) -> list[Lead]:
        return await self.repo.get_follow_ups_due()

    async def get_pipeline_value(self) -> float:
        return await self.repo.get_pipeline_value()

    async def count_by_status(self) -> list[dict]:
        return await self.repo.count_by_status()

    async def count_by_source(self) -> list[dict]:
        return await self.repo.count_by_source()
