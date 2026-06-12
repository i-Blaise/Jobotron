from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
from bson import ObjectId

from index import startPoint
from mongodbConnect import MongoDBManager
from dataLib import deleteAllData, deleteOneData
from job_scrapper import jobScrapper
from jobberman_scrapper import jobbermanScrapper
from logs import logProcesses

scheduler = AsyncIOScheduler(timezone="Africa/Accra")


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(startPoint, "cron", hour="9,12,15,18", misfire_grace_time=300)
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


@app.get("/jobs")
def list_jobs():
    try:
        collection = MongoDBManager.get_collection()
        if collection is None:
            raise HTTPException(status_code=503, detail="Database unavailable")
        jobs = list(collection.find({"numberTimesPosted": {"$lte": 2}}))
        for job in jobs:
            job["_id"] = str(job["_id"])
        return {"jobs": jobs, "count": len(jobs)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")


@app.delete("/jobs/{job_id}")
def delete_job(job_id: str):
    try:
        oid = ObjectId(job_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid job ID")
    result = deleteOneData(oid)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found or DB unavailable")
    return {"deleted": job_id}


@app.delete("/jobs")
def clear_jobs():
    result = deleteAllData()
    if not result:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"message": "All jobs cleared"}


@app.post("/scrape")
async def trigger_scrape():
    result = await asyncio.to_thread(_run_scrape)
    return result


def _run_scrape():
    scrap_result = jobScrapper()
    logProcesses(f"Manual scrape - Jobweb: {scrap_result}")
    jobweb_no_results = (
        (isinstance(scrap_result, str) and scrap_result in ("No New Job", "Database Unavailable"))
        or (isinstance(scrap_result, dict) and not scrap_result.get("status", True))
    )
    if jobweb_no_results:
        scrap_result_jb = jobbermanScrapper()
        logProcesses(f"Manual scrape - Jobberman: {scrap_result_jb}")
        return {"jobwebghana": scrap_result, "jobberman": str(scrap_result_jb)}
    return {"jobwebghana": str(scrap_result), "jobberman": "not_run"}


@app.post("/post")
async def trigger_post():
    await asyncio.to_thread(startPoint)
    return {"message": "Post cycle triggered"}


@app.get("/logs")
def get_logs(lines: int = 100):
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logfile.txt")
    if not os.path.exists(log_path):
        return {"logs": [], "total_lines": 0}
    with open(log_path, "r") as f:
        all_lines = f.readlines()
    return {"logs": all_lines[-lines:], "total_lines": len(all_lines)}


@app.get("/schedule")
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
