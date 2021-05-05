import requests
from bs4 import BeautifulSoup




def get_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')
  pages = soup.find('div', {'class':'s-pagination'}).find_all('a')
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)

def extract_job(soup):
  title = soup.find("h2", {"class":"fc-black-800"}).find('a').string
  company,location = soup.find("h3", {"class":"fc-black-700"}).find_all('span', recursive=False)
  #recursive=False를 붙여주면 같은 단계의 span만 검색해내줌
  #그 하위 단계들의 span에 대해서는 검색하지 않음.
  #company,location으로 표현한 것은 검색결과가 딱 2개가 나올 것임을 알고 있어서
  #값을 2개 받도록 선언해둔 것임!
  company = company.get_text(strip=True).strip("\n")
  location = location.get_text(strip=True)
  job_id = soup["data-jobid"]
  return {'title':title, 'company':company, 'location':location, "link":f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page, URL):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: Page {page+1}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find_all("div", {"class":"-job"})
    for page in pages:
      job = extract_job(page)
      jobs.append(job)
  return jobs


def get_jobs(word):
  URL = f"https://stackoverflow.com/jobs?q={word}"
  last_page = get_last_page(URL)
  jobs = extract_jobs(last_page, URL)
  return jobs