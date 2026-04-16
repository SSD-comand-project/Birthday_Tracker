from fastapi import APIRouter, Depends, Query

from app.backend.services import birthdays, users
from app.backend.utils.auth import get_current_active_user

router = APIRouter(prefix="/birthdays", tags=["Birthdays"])


@router.get("/today", summary="Get birthdays today")
def get_today(current_user: dict = Depends(get_current_active_user)):
    """Returns list of users with birthdays today."""
    return birthdays.get_birthdays_today()


@router.get("/upcoming", summary="Get birthdays for next 7 days")
def get_upcoming(current_user: dict = Depends(get_current_active_user)):
    """Returns list of users with birthdays in the next 7 days."""
    return birthdays.get_birthdays_next_7_days()


@router.get("/search", summary="Search users by name")
def search(
    name: str = Query(..., min_length=1, description="Search query for user's full name"),
    current_user: dict = Depends(get_current_active_user),
):
    """Search users by full name."""
    return users.search_users_by_name(name)
