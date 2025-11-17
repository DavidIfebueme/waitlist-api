from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .schemas import WaitlistIn
from .models import Base, Waitlist
from .database import engine, get_db
from .emailer import send_thank_you_email

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/waitlist", status_code=201)
async def join_waitlist(
    data: WaitlistIn,
    background: BackgroundTasks,
    db=Depends(get_db)
):
    new_entry = Waitlist(name=data.name, email=data.email)

    db.add(new_entry)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already on waitlist")

    background.add_task(send_thank_you_email, data.email, data.name)
    return {"status": "ok"}
