from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from datetime import date

from app.backend.services import users
from app.backend.utils.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


class UserProfileUpdate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    birth_date: str = Field(..., description="Birth date in format YYYY-MM-DD, e.g. 1990-05-20")

    def validate_birth_date(self) -> None:
        try:
            bd = date.fromisoformat(self.birth_date)
            today = date.today()
            if bd > today:
                raise ValueError("Birth date cannot be in the future")
            if (today.year - bd.year) > 120:
                raise ValueError("Age cannot exceed 120 years")
        except ValueError as e:
            raise ValueError(f"Invalid birth date: {str(e)}")


@router.get("/me", summary="Get current user profile")
def read_users_me(current_user: dict = Depends(get_current_active_user)):
    """Get the profile of the currently logged-in user."""
    return current_user


@router.put("/me", summary="Update current user profile")
def update_user_me(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_active_user),
):
    """
    Update the profile of the currently logged-in user.

    - **full_name**: new full name
    - **birth_date**: new birth date in format YYYY-MM-DD
    """
    try:
        profile_data.validate_birth_date()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    success = users.update_user_profile(
        user_id=current_user["id"],
        full_name=profile_data.full_name,
        birth_date=profile_data.birth_date,
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Profile updated successfully"}


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user account")
def delete_user_me(current_user: dict = Depends(get_current_active_user)):
    """Delete the account of the currently logged-in user."""
    success = users.delete_user(user_id=current_user["id"])
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return
