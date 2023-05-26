# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter

class LetterbeijingPipeline:
    def __init__(self):
        self.file = open('letter.json', 'wb')  # 必须写入二进制
        self.exporter = JsonLinesItemExporter(self.file, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        print(item)

    def close_item(self, spider):
        self.file.close()

