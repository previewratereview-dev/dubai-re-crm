import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.customer import CustomerService
from math import ceil

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("", response_model=PaginatedResponse)
async def list_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    q: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)
    customers, total = await service.search(q, page, per_page)
    return PaginatedResponse(
        items=[CustomerResponse.model_validate(c) for c in customers],
        total=total, page=page, per_page=per_page, total_pages=ceil(total / per_page),
    )


@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)
    customer = await service.create(data, current_user.id)
    return CustomerResponse.model_validate(customer)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)
    customer = await service.get_by_id(customer_id)
    return CustomerResponse.model_validate(customer)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: uuid.UUID,
    data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)
    customer = await service.update(customer_id, data)
    return CustomerResponse.model_validate(customer)


@router.delete("/{customer_id}", response_model=MessageResponse)
async def delete_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)
    await service.delete(customer_id)
    return MessageResponse(message="Customer deleted")


@router.post("/from-lead/{lead_id}", response_model=CustomerResponse)
async def convert_lead_to_customer(
    lead_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)
    customer = await service.from_lead(lead_id, current_user.id)
    return CustomerResponse.model_validate(customer)
