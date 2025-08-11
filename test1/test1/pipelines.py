# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# pipelines.py
import json
from itemadapter import ItemAdapter

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('products.json', 'w', encoding='utf-8')
        self.file.write('[\n')  # 开始JSON数组
        self.first_item = True

    def process_item(self, item, spider):
        line = json.dumps(
            ItemAdapter(item).asdict(),
            ensure_ascii=False,
            indent=2
        )
        if not self.first_item:
            self.file.write(',\n' + line)
        else:
            self.file.write(line)
            self.first_item = False
        return item

    def close_spider(self, spider):
        self.file.write('\n]')  # 结束JSON数组
        self.file.close()
        
class Test1Pipeline:
    def process_item(self, item, spider):
        return item
