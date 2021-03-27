import scrapy
from urllib.parse import urlencode
import json
from scrapy_download.items import ScrapyDownloadItem
from scrapy.http import Request


class ImageSpiderSpider(scrapy.Spider):
    name = 'image_spider'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def start_requests(self):
        types = self.settings.get('TYPE')
        page_num = self.settings.get('PAGE')
        base_url = 'https://image.so.com/zjl?'
        for each_type in types:
            data = {
                'ch': each_type,
                'listtype': 'new'
            }
            for each_page in range(1, page_num + 1):
                data['sn'] = each_page * 30
                yield Request(base_url + urlencode(data), meta={'type': each_type})

    def parse(self, response):
        json_content = json.loads(response.text)
        for each_image in json_content.get('list'):
            item = ScrapyDownloadItem()
            item['type'] = response.meta['type']
            item['url'] = each_image.get('qhimg_url')
            yield item
