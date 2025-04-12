import re
from typing import List, Dict

def extract_skills_from_description(description: str, skill_list: List[str]) -> List[str]:
    found_skills = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, description, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills

def match_jobs_by_skills(jobs: List[Dict], user_skills: List[str]) -> List[Dict]:
    matched_jobs = []
    for job in jobs:
        matched = extract_skills_from_description(job.get("description", ""), user_skills)
        score = len(matched)
        job_with_match = {
            **job,
            "matched_skills": matched,
            "match_score": score
        }
        matched_jobs.append(job_with_match)

    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    return matched_jobs
