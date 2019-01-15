# Google Scholar Scrapy
Scrapping for Google Scholar

## Requirement

### Prerequisites
- Python - Download and Install [Python](https://www.python.org/)
- Pip - Download and Install [Pip](https://pypi.org/project/pip/) 

```
  $ pip install -r requirements.txt

```

## Run Program

Jalankan command berikut untuk menjalankan scrapy

**Start application for firstime on production server**

```
$ cd folder
$ scrapy crawl <spidername>

```

## Note

spider = profil(untuk mendapatkan semua data penelitian dari user)

Start Url (Diganti dengan user yang diinginkan)

```
start_urls = ['https://scholar.google.co.id/citations?user=oRWiRGQAAAAJ/']

```

Webdriver (Diganti dengan path yang sesuai)

```
driver = webdriver.Chrome('/home/arham/chromedriver_linux64/chromedriver')

```

