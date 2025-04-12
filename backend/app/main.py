from fastapi import FastAPI, Query
from typing import List
from adzuna_api import search_adzuna_jobs
from job_ad_api import match_jobs_by_skills

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to TechSkillSync API"}

@app.get("/adzuna_jobs")
def get_jobs(
    keyword: str = Query(...),
    location: str = Query("Sydney"),
    skills: List[str] = Query([])
):
    jobs = search_adzuna_jobs(keyword, location)
    matched = match_jobs_by_skills(jobs, skills)
    return {"results": matched}
