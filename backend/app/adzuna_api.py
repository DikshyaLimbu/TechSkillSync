import requests

APP_ID = '7b9c1c38'
APP_KEY = 'ff185f03d8911f04c567b500bbbaa741'

def search_adzuna_jobs(keyword, location="Sydney", results_per_page=10):
    country = 'au'
    base_url = f'https://api.adzuna.com/v1/api/jobs/{country}/search/1'

    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'results_per_page': results_per_page,
        'what': keyword,
        'where': location,
        'content-type': 'application/json'
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        jobs = response.json().get('results', [])
        return [
            {
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name", ""),
                "location": job.get("location", {}).get("display_name", ""),
                "description": job.get("description", ""),
                "url": job.get("redirect_url")
            }
            for job in jobs
        ]
    else:
        raise Exception(f"Adzuna API error: {response.status_code} - {response.text}")
