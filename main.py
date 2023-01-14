from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.remoteOk import extract_remoteOk_jobs
from file import save_to_file

app = Flask("JobScrapper")

database = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in database:
        jobs = database[keyword]
    else:
        indeed = extract_indeed_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        remote_ok = extract_remoteOk_jobs(keyword)
        jobs = indeed+wwr+remote_ok
        database[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in database:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, database[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")
