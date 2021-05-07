# scraper_login

# Environment
* Python 3.7 >
# Installation
* pip install scrapy
* https://github.com/scrapy-plugins/scrapy-splash[https://github.com/scrapy-plugins/scrapy-splash]
# Run
* cd myprojet/spiders
* scrapy runspider mydomain.py
# Export to a csv file
* scrapy runspider mydomain.py  -t csv -o FileName.csv --loglevel=INFO
