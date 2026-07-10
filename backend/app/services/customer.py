import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: AsyncSession):
        self.repo = CustomerRepository(db)
        self.db = db

    async def search(self, query: str | None = None, page: int = 1, per_page: int = 20):
        return await self.repo.search(query, page, per_page)

    async def get_by_id(self, id: uuid.UUID) -> Customer:
        customer = await self.repo.get_by_id(id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer

    async def create(self, data: CustomerCreate, user_id: uuid.UUID | None = None) -> Customer:
        return await self.repo.create(**data.model_dump(exclude={"tag_ids"}), created_by=user_id)

    async def update(self, id: uuid.UUID, data: CustomerUpdate) -> Customer:
        customer = await self.repo.update(id, **data.model_dump(exclude_unset=True))
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer

    async def delete(self, id: uuid.UUID) -> bool:
        return await self.repo.soft_delete(id)

    async def from_lead(self, lead_id: uuid.UUID, user_id: uuid.UUID | None = None) -> Customer:
        from app.repositories.lead import LeadRepository
        lead_repo = LeadRepository(self.db)
        lead = await lead_repo.get_by_id(lead_id)
        if not lead:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
        customer = Customer(
            lead_id=lead.id,
            first_name=lead.first_name,
            last_name=lead.last_name,
            company=lead.company,
            phone=lead.phone,
            email=lead.email or f"placeholder_{lead.id}@noemail.com",
            address=lead.address,
            city=lead.city,
            state=lead.state,
            country=lead.country,
            zip_code=lead.zip_code,
            industry=lead.industry,
            created_by=user_id,
        )
        self.db.add(customer)
        lead.status = "won"
        await self.db.flush()
        await self.db.refresh(customer)
        return customer

    async def search_for_tools(self, query: str) -> list[Customer]:
        customers, _ = await self.repo.search(query, page=1, per_page=10)
        return customers
