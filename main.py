from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.remoteOk import extract_remoteOk_jobs

keyword = input("what do you want to search for?")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
remote_ok = extract_remoteOk_jobs(keyword)

jobs = indeed+wwr+remote_ok

file = open(f"{keyword}.csv", "w", encoding="utf-8-sig")
file.write("Position,Company,Location,URL\n")

for job in jobs:
    file.write(
        f"{job['title']},{job['company']},{job['location'],{job['link']}}\n")

file.close()
