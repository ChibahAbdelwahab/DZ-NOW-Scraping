API_KEY = "be9b53f6ff094d3f8d37c8b63bb1fcd8"
PROJECT_ID = "406520"
client = ScrapinghubClient(API_KEY)
project = client.get_project(PROJECT_ID)


def run_jobs():
    for ii in project.spiders.list():
        try:
            spider = project.spiders.get(ii)
            spider.jobs.run()
        except Exception as e:
            print(e)
