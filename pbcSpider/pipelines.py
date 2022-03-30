# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.exporters import XmlItemExporter
from pbcSpider import settings


class PbcspiderPipeline:

    def __init__(self):
        self.exporters = {}

    def open_spider(self, spider):
        self.exporters = {}
        outFilePathL = [settings.PBCCOIN_EXPORT_DEFAULT,
                        settings.PBCCOIN_EXPORT_IMPORTANT]
        exporterNameL = ["default", "important"]
        for exporterName, outFilePath in zip(exporterNameL, outFilePathL):
            exporter = XmlItemExporter(open(outFilePath, 'w+b'))
            exporter.start_exporting()
            self.exporters[exporterName] = exporter

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()

    def process_item(self, item, spider):
        if item['isImportant'] == "True":
            item.pop('isImportant')
            self.exporters["important"].export_item(item)
        else:
            item.pop('isImportant')
            self.exporters["default"].export_item(item)
        return item
