from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# DB setup
from app.db.database import Base, engine

# Import models so SQLAlchemy creates the tables
from app.models import user
from app.models import experiment
from app.models import assignment
from app.models import event
from app.api import analytics

# Import API routers
from app.api import users
from app.api import auth
from app.api import experiments
from app.api import assignments
from app.api import events

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ExperimentHub API",
    description="A/B Testing & Experimentation Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(experiments.router)
app.include_router(assignments.router)
app.include_router(events.router)
app.include_router(analytics.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ExperimentHub API"}