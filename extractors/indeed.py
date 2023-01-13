import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import get
from bs4 import BeautifulSoup


def get_page_count(keyword):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)
    browser.get(f"https://kr.indeed.com/jobs?q={keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})
    if pagination == None:
        return 1
    pages = pagination.select("div a")
    count = len(pages)+1
    for page in pages:
        if page['aria-label'] == "Previous Page":
            count -= 1
        elif page['aria-label'] == "Next Page":
            count -= 1
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print(f"Found {pages} pages")
    results = []
    for page in range(pages):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(options=options)
        browser.get(f"https://kr.indeed.com/jobs?q={keyword}&{page*10}")
        print("Requesting...",
              f"https://kr.indeed.com/jobs?q={keyword}&{page*10}")

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor["aria-label"]
                link = anchor["href"]
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    "link": f"https://kr.indeed.com{link}",
                    "company": company.string,
                    "location": location.string,
                    "title": title,
                }
                results.append(job_data)
    return results
