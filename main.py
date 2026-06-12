from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import hmac
import os
from bson import ObjectId

from index import startPoint
from mongodbConnect import MongoDBManager
from config_manager import get_config, update_config
from dataLib import deleteAllData, deleteOneData, max_post_count
from job_scrapper import jobScrapper
from jobberman_scrapper import jobbermanScrapper
from logs import logProcesses

scheduler = AsyncIOScheduler(timezone="Africa/Accra")

POST_CYCLE_JOB_ID = "post_cycle"


def _schedule_hours_str():
    return ",".join(str(h) for h in get_config()["schedule_hours"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(
        startPoint,
        "cron",
        hour=_schedule_hours_str(),
        misfire_grace_time=300,
        id=POST_CYCLE_JOB_ID,
    )
    scheduler.start()
    logProcesses("Jobotron started via FastAPI + APScheduler")
    yield
    scheduler.shutdown()


app = FastAPI(title="Jobotron Admin API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_auth(x_admin_key: str = Header(default="")):
    expected = os.getenv("ADMIN_PASSWORD", "")
    if not expected or not hmac.compare_digest(x_admin_key, expected):
        raise HTTPException(status_code=401, detail="Unauthorized")


class LoginRequest(BaseModel):
    password: str


class ConfigUpdate(BaseModel):
    schedule_hours: Optional[List[int]] = None
    keywords: Optional[List[str]] = None
    sources: Optional[Dict[str, bool]] = None
    max_post_count: Optional[int] = None
    min_queue_size: Optional[int] = None
    jobberman_fallback_query: Optional[str] = None


@app.post("/auth/login")
def login(body: LoginRequest):
    expected = os.getenv("ADMIN_PASSWORD", "")
    if not expected:
        raise HTTPException(status_code=503, detail="ADMIN_PASSWORD is not set on the server")
    if not hmac.compare_digest(body.password, expected):
        raise HTTPException(status_code=401, detail="Wrong password")
    return {"ok": True}


@app.get("/health")
def health():
    client = MongoDBManager.get_client()
    db_ok = client is not None
    jobs = scheduler.get_jobs()
    return {
        "status": "ok" if db_ok else "degraded",
        "db_connected": db_ok,
        "scheduler_running": scheduler.running,
        "next_run": str(jobs[0].next_run_time) if jobs else None,
    }


@app.get("/config", dependencies=[Depends(require_auth)])
def read_config():
    return get_config(force_refresh=True)


@app.put("/config", dependencies=[Depends(require_auth)])
def write_config(body: ConfigUpdate):
    changes = body.model_dump(exclude_none=True)
    try:
        config = update_config(changes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    if "schedule_hours" in changes:
        scheduler.reschedule_job(
            POST_CYCLE_JOB_ID, trigger="cron", hour=_schedule_hours_str()
        )
        logProcesses(f"Schedule updated via portal: hours {config['schedule_hours']}")

    return config


@app.get("/jobs", dependencies=[Depends(require_auth)])
def list_jobs():
    try:
        collection = MongoDBManager.get_collection()
        if collection is None:
            raise HTTPException(status_code=503, detail="Database unavailable")
        jobs = list(collection.find({"numberTimesPosted": {"$lte": max_post_count()}}))
        for job in jobs:
            job["_id"] = str(job["_id"])
        return {"jobs": jobs, "count": len(jobs), "max_post_count": max_post_count()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")


@app.delete("/jobs/{job_id}", dependencies=[Depends(require_auth)])
def delete_job(job_id: str):
    try:
        oid = ObjectId(job_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid job ID")
    result = deleteOneData(oid)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found or DB unavailable")
    return {"deleted": job_id}


@app.delete("/jobs", dependencies=[Depends(require_auth)])
def clear_jobs():
    result = deleteAllData()
    if not result:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"message": "All jobs cleared"}


@app.post("/scrape", dependencies=[Depends(require_auth)])
async def trigger_scrape():
    result = await asyncio.to_thread(_run_scrape)
    return result


def _run_scrape():
    sources = get_config()["sources"]
    scrap_result = None
    if sources.get("jobwebghana", True):
        scrap_result = jobScrapper()
        logProcesses(f"Manual scrape - Jobweb: {scrap_result}")
    jobweb_no_results = (
        scrap_result is None
        or (isinstance(scrap_result, str) and scrap_result in ("No New Job", "Database Unavailable"))
        or (isinstance(scrap_result, dict) and not scrap_result.get("status", True))
    )
    if jobweb_no_results and sources.get("jobberman", True):
        scrap_result_jb = jobbermanScrapper()
        logProcesses(f"Manual scrape - Jobberman: {scrap_result_jb}")
        return {"jobwebghana": str(scrap_result), "jobberman": str(scrap_result_jb)}
    return {"jobwebghana": str(scrap_result), "jobberman": "not_run"}


@app.post("/post", dependencies=[Depends(require_auth)])
async def trigger_post():
    await asyncio.to_thread(startPoint)
    return {"message": "Post cycle triggered"}


@app.get("/logs", dependencies=[Depends(require_auth)])
def get_logs(lines: int = 100):
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logfile.txt")
    if not os.path.exists(log_path):
        return {"logs": [], "total_lines": 0}
    with open(log_path, "r") as f:
        all_lines = f.readlines()
    return {"logs": all_lines[-lines:], "total_lines": len(all_lines)}


@app.get("/schedule", dependencies=[Depends(require_auth)])
def get_schedule():
    jobs = scheduler.get_jobs()
    return {
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run": str(job.next_run_time),
                "trigger": str(job.trigger),
            }
            for job in jobs
        ]
    }


# Serve the built admin portal (admin/dist) at the root. Mounted last so the
# API routes above take precedence.
ADMIN_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "admin", "dist")
if os.path.isdir(ADMIN_DIST):
    app.mount("/", StaticFiles(directory=ADMIN_DIST, html=True), name="admin")
