from fastapi import FastAPI

from api.v1.router import router as notes_router


app = FastAPI(title='Simple Notes')

app.include_router(notes_router)
