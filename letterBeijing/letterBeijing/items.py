# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LetterbeijingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 信件类型
    type = scrapy.Field()
    # 信件标题
    title = scrapy.Field()
    # 信件内容
    content = scrapy.Field()
    # 处理部门
    institution = scrapy.Field()
    # 答复内容
    reply = scrapy.Field()

