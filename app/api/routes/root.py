"""
Root API routes
"""

# Import from third party
from fastapi import APIRouter, Depends


# Define router
router = APIRouter(
    prefix="/root",
    tags=["root"],
)
