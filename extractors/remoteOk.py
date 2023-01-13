from bs4 import BeautifulSoup
import requests


def extract_remoteOk_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    results = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all("div", class_="page")
        for job_section in jobs:
            job_post = job_section.find_all("div", class_="container")
            for post in job_post:
                jobsboard = post.find_all("table")
                for main_post_box in jobsboard:
                    job = main_post_box.find_all("tr", class_="job")
                    for main_described in job:
                        main = main_described.find_all(
                            "td", class_="company_and_position")
                        for job_described in main:
                            anchors = job_described.find_all("a")
                            anchor = anchors[0]
                            link = anchor["href"]
                            position = anchor.find("h2")
                            company = job_described.find("h3")
                            location_pay = job_described.find_all("div")
                            location = location_pay[0]
                            pay = location_pay[1]
                            job_data = {
                                "link": f"https://remoteok.com/{link}",
                                "position": position.string,
                                "company": company.string,
                                "location": location.string,
                                "pay": pay.string
                            }
                            results.append(job_data)
    return results
