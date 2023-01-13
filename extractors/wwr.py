from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    response = get(url, headers={"User-Agent": "Kimchi"})
    results = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        for job_section in jobs:
            job_post = job_section.find_all("li")
            job_post.pop(-1)
            for post in job_post:
                anchors = post.find_all("a")
                anchor = anchors[1]
                link = anchor["href"]
                company, kind, region = anchor.find_all(
                    "span", class_="company")
                title = anchor.find("span", class_="title")
                job_data = {
                    "link": f"https://weworkremotely.com/{link}",
                    "company": company.string,
                    "location": region.string,
                    "position": title.string
                }
                results.append(job_data)
    return results
