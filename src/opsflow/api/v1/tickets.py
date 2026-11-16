from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from opsflow.api.dependencies import get_current_user
from opsflow.database.session import get_db
from opsflow.models.ticket import Ticket
from opsflow.models.user import User
from opsflow.schemas.ticket import (
    TicketCreate,
    TicketRead,
    TicketStatus,
    TicketUpdateStatus,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_in: TicketCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Ticket:
    new_ticket = Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        priority=ticket_in.priority.value,
        status=TicketStatus.OPEN.value,
        author_id=current_user.id,
    )
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    return new_ticket


@router.get("", response_model=list[TicketRead])
async def get_tickets(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Ticket]:
    query = select(Ticket).order_by(Ticket.created_at.desc())

    # all tickets for ADMIN!!!
    if current_user.role != "ADMIN":
        query = query.where(Ticket.author_id == current_user.id)

    result = await db.scalars(query)
    return list(result.all())


@router.patch("/{ticket_id}/status", response_model=TicketRead)
async def update_ticket_status(
    ticket_id: int,
    status_in: TicketUpdateStatus,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Ticket:
    ticket = await db.scalar(select(Ticket).where(Ticket.id == ticket_id))
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    is_admin = current_user.role == "ADMIN"
    is_author = ticket.author_id == current_user.id

    if not is_admin and not is_author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify this ticket",
        )

    if not is_admin and status_in.status != TicketStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change status to anything other than CLOSED",
        )

    ticket.status = status_in.status.value
    await db.commit()
    await db.refresh(ticket)
    return ticket