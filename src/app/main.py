from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import WaitlistIn
from .models import Base, Waitlist
from .database import engine, get_db
from .emailer import send_thank_you_email

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request
from slowapi.errors import RateLimitExceeded

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/waitlist", status_code=201)
@limiter.limit("5/minute") 
async def join_waitlist(
    request: Request,
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

@app.get("/waitlist/stats")
async def waitlist_stats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Waitlist))
    users = result.scalars().all()
    return {
        "count": len(users),
        "users": [{"id": u.id, "name": u.name, "email": u.email, "created_at": u.created_at} for u in users]
    }
