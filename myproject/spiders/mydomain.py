import scrapy
from scrapy_splash import SplashRequest 

# https://jiwonkim@redwit.io:redwit0801!@beginmate.com/team

def parseWord( word):
    if (word==None):
        return ''
    return word.replace("\xa0","").replace("\n","").replace("\t","").replace("\r","").strip()


class BrickSetSpider(scrapy.Spider):
    name = "splash_spider"
    allowed_domains = ['beginmate.com']
    start_urls = ["https://beginmate.com/team"]
    

    def start_requests(self):
        for url in self.start_urls: 
            yield SplashRequest(url, self.login, 
                endpoint='render.html', 
                args={'wait': 0.5}, 
           ) 

    def start_request(self,response):
        yield SplashRequest(response.url, self.after_login, 
            endpoint='render.html', 
            args={'wait': 0.5}, 
        ) 

    # Login and then go to after_login to parse the necessary pages.
    def login(self, response):
        # scrapy.Request(url="https://beginmate.com/Token",
        #                        cookies=[{'username': 'jiwonkim@redwit.io', 'password': 'redwit0801!',
        #                        'grant_type':'password'}],
        #                         callback=self.after_login)
        return scrapy.FormRequest(
            url="https://beginmate.com/Token",
            formdata={'username': 'jiwonkim@redwit.io', 'password': 'redwit0801!','grant_type':'password'},
            # formcss="sign_login_section",
            callback=self.goto_team
        )
    def goto_team(self, response):

        yield scrapy.Request(
                    response.urljoin("https://beginmate.com/team"),
                    callback=self.start_request
                )
    def after_login(self, response):
        
        PAGES_SELECTOR = '.recruit_card a::attr(href)'
        pages = response.css(PAGES_SELECTOR).extract()
        pages = list(dict.fromkeys(pages))
        for next_page in pages:
            if len(next_page) < 200:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.start_request
                )
        SET_SELECTOR = '.contact_info'
        for brickset in response.css(SET_SELECTOR):
            
            name = brickset.css(".info_content::text").extract()
            
            if name!=None:

                yield({
                    "contact_info":name,
                })



