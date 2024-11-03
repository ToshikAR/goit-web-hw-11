from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import func, select, or_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact
from src.schema.contact import ContactSchema, ContactUpdateSchema, ContactResponse


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def add_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    # contact = Contact(
    #     first_name=body.first_name,
    #     last_name=body.last_name,
    #     email=body.email,
    #     phone=body.phone,
    #     description=body.description,
    # )
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.description = body.description
        contact.date_birth = body.date_birth
        contact.last_visit = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(params: List[Optional[str]], db: AsyncSession):
    first_name, last_name, email = params

    filters = []
    if first_name:
        filters.append(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        filters.append(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        filters.append(Contact.email.ilike(f"%{email}%"))

    if filters:
        stmt = select(Contact).where(or_(*filters))

    result = await db.execute(stmt)
    contacts = result.scalars().all()
    return contacts


async def get_upcoming_birthdays(days: int, db: AsyncSession):
    today = datetime.now().date()
    months_days = [(today.month, today.day)]
    for i in range(1, days + 1):
        next_day = today + timedelta(days=i)
        months_days.append((next_day.month, next_day.day))

    conditions = [
        (extract("month", Contact.date_birth) == month)
        & (extract("day", Contact.date_birth) == day)
        for month, day in months_days
    ]

    stmt = select(Contact).where(or_(*conditions))

    result = await db.execute(stmt)
    contacts = result.scalars().all()
    return contacts
