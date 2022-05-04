# -*- coding: utf-8 -*-
from .items import *


class GildedRose(object):
    CATALOG = {
        "aged brie": AgedBrie,
        "sulfuras": Sulfuras,
        "backstage passes": BackstagePasses,
    }

    def __init__(self, items):
        self.items = items
        tradeable_items = []
        for item in items:
            try:
                tradeable_items.append(
                    create_tradable_item(item=item, catalog=self.CATALOG)
                )
            except (QualityExceedsMinException, QualityExceedsMaxException):
                print(
                    "Please provide a legitimate quality for this specific item."
                    f"item:{item.name} , quality: {item.quality}"
                )
                continue

        self.tradaeble_items = [
            create_tradable_item(item=item, catalog=self.CATALOG) for item in items
        ]

    def update_quality(self):
        for tradeable_item in self.tradaeble_items:
            tradeable_item.daily_update()
