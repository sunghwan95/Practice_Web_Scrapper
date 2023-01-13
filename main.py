from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.remoteOk import extract_remoteOk_jobs

keyword = input("what do you want to search for?")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
remote_ok = extract_remoteOk_jobs(keyword)

jobs = indeed+wwr+remote_ok
