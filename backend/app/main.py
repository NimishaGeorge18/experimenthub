from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import user, experiment
from app.db.database import Base, engine
from app.api import users
from app.api import auth          
from app.api import experiments  

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

app.include_router(users.router)
app.include_router(auth.router)   
app.include_router(experiments.router)  

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ExperimentHub API"}