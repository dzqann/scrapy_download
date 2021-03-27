# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging


class ScrapyDownloadPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        image_type = request.meta['type']
        return image_type + "/" + url.split('/')[-1]

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Download Failed')
        return item

    def get_media_requests(self, item, info):
        yield Request(url=item['url'], meta={'type': item['type']})
