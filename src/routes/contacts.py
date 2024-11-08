from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as repositories_contacts
from src.schema.contact import ContactSchema, ContactResponse, ContactUpdateSchema

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    contacts = await repositories_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    contact = await repositories_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def add_contact(
    body: ContactSchema,
    db: AsyncSession = Depends(get_db),
):
    contact = await repositories_contacts.add_contact(body, db)
    return contact


@router.put("/{contact_id}")
async def update_contact(
    body: ContactUpdateSchema,
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    contact = await repositories_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    contact = await repositories_contacts.delete_contact(contact_id, db)
    return contact


@router.get("/contacts/search/", response_model=list[ContactResponse])
async def search_contacts(
    FirstName: Optional[str] = Query(None, description="Contact name to search for"),
    LastName: Optional[str] = Query(None, description="Contact's last name to search for"),
    Email: Optional[str] = Query(None, description="Contact email to search"),
    db: AsyncSession = Depends(get_db),
):
    params = [FirstName, LastName, Email]
    contacts = await repositories_contacts.search_contacts(params, db)
    if contacts is None or not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    print("err5")
    return contacts


@router.get("/contacts/upcoming-birthdays", response_model=list[ContactResponse])
async def get_upcoming_birthdays(days: int = Query(7, gt=0), db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_upcoming_birthdays(days, db)
    return contacts
