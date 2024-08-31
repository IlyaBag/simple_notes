from fastapi import APIRouter

from .auth import router as auth_router
from .notes_api import router as notes_router


router = APIRouter(prefix='/api/v1')

router.include_router(notes_router)
router.include_router(auth_router)
