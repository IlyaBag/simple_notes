from fastapi import APIRouter

from .notes_api import router as notes_router


router = APIRouter(prefix='/api/v1')

router.include_router(notes_router)
