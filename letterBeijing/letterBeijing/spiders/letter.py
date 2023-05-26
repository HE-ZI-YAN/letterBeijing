import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from letterBeijing.items import LetterbeijingItem
import json

i = 1

class LetterSpider(scrapy.Spider):
    name = "letter"
    allowed_domains = ["www.beijing.gov.cn"]
    start_urls = ["https://www.beijing.gov.cn/hudong/hdjl/sindex/bjah-index-hdjl!letterListJson.action?keyword=&startDate=&endDate=&letterType=0&page.pageNo=1&page.pageSize=6&orgtitleLength=26"]

    def parse(self, response):
        input_string = response.text
        # 处理字符串，使用双引号替换键名和字符串值的单引号
        processed_string = input_string.replace("'", "\"")
        processed_string = processed_string.replace("page:", "\"page\":")
        processed_string = processed_string.replace("pageNo:", "\"pageNo\":")
        processed_string = processed_string.replace("totalCount:", "\"totalCount\":")
        processed_string = processed_string.replace("totalPages:", "\"totalPages\":")
        processed_string = processed_string.replace("pageSize:", "\"pageSize\":")
        processed_string = processed_string.replace("result:", "\"result\":")
        processed_string = processed_string.replace("letterType:", "\"letterType\":")
        processed_string = processed_string.replace("letterTypeName:", "\"letterTypeName\":")
        processed_string = processed_string.replace("letterTitle:", "\"letterTitle\":")
        processed_string = processed_string.replace("showLetterTitle:", "\"showLetterTitle\":")
        processed_string = processed_string.replace("writeDate:", "\"writeDate\":")
        processed_string = processed_string.replace("orgNames:", "\"orgNames\":")
        processed_string = processed_string.replace("showOrgNames:", "\"showOrgNames\":")
        processed_string = processed_string.replace("originalId:", "\"originalId\":")

        contents = json.loads(processed_string)["result"]

        for content in contents:
            # 详情内容的url
            url = ["https://www.beijing.gov.cn/hudong/hdjl/com.web.consult.consultDetail.flow?originalId=",
                   "https://www.beijing.gov.cn/hudong/hdjl/com.web.suggest.suggesDetail.flow?originalId=",
                   ]
            # 内容类型
            type = content["letterTypeName"]
            # 内容标题
            title = content["letterTitle"]
            # 处理机构
            institution = content["showOrgNames"]

            if(type=="咨询"):
                yield scrapy.Request(url=url[0]+content["originalId"],callback=self.parse_second,meta={'type':type,'title':title,'institution':institution})
            elif(type=="建议"):
                yield scrapy.Request(url=url[1]+content["originalId"],callback=self.parse_second,meta={'type':type,'title':title,'institution':institution})


    def parse_second(self,response):
        # 信件内容
        content = response.xpath('//div[@class="col-xs-12 col-md-12 column p-2 text-muted mx-2"]/text()').extract_first()
        # 回复内容
        reply = response.xpath('//div[@class="col-xs-12 col-md-12 column p-4 text-muted my-3"]/text()').extract_first()
        type = response.meta['type']
        title = response.meta['title']
        institution = response.meta['institution']

        letter = LetterbeijingItem(type=type,title=title,content=content,institution=institution,reply=reply)

        yield letter
        global i
        i += 1
        url = "https://www.beijing.gov.cn/hudong/hdjl/sindex/bjah-index-hdjl!letterListJson.action?keyword=&startDate=&endDate=&letterType=0&page.pageNo="+str(i)+"&page.pageSize=6&orgtitleLength=26";
        if(i<150):
            yield scrapy.Request(url=url,callback=self.parse,dont_filter = False)