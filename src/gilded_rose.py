# -*- coding: utf-8 -*-
from .items import *


class GildedRose(object):
    def __init__(self, items):
        self.items = items
        tradeable_items = []
        for item in items:
            try:
                tradeable_items.append(factory_tradable_item(item=item))
            except (QualityExceedsMinException, QualityExceedsMaxException):
                print(
                    "Please provide a legitimate quality for this specific item."
                    f"item:{item.name} , quality: {item.quality}"
                )
                continue
        self.tradaeble_items = tradeable_items

    def update_quality(self):
        for tradeable_item in self.tradaeble_items:
            tradeable_item.daily_update()
