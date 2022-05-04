from typing import Dict


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class QualityExceedsMinException(Exception):
    "This error is raised when the quality of an item exceeds its minimum value"
    pass


class QualityExceedsMaxException(Exception):
    "This error is raised when the quality of an item exceeds its maximum value"
    pass


class TradeableItem(Item):
    def __init__(
        self,
        name: str,
        sell_in: int,
        quality: int,
        min_quality: int = 0,
        max_quality: int = 50,
    ):
        super().__init__(name, sell_in, quality)
        self.min_quality = min_quality
        self.max_quality = max_quality

    def daily_update(self):
        self.check_quality()
        self.update_quality()
        self.update_sell_in()

    def update_quality(self):
        if self.quality == self.min_quality:
            return
        elif self.sell_in < 0:
            self.quality -= 2
        else:
            self.quality -= 1

    def update_sell_in(self):
        self.sell_in -= 1

    def check_quality(self):
        if self.max_quality < self.quality:
            raise QualityExceedsMaxException
        if self.quality < self.min_quality:
            raise QualityExceedsMinException


class AgedBrie(TradeableItem):
    def update_quality(self):
        if self.quality == self.max_quality:
            return
        elif self.sell_in < 0:
            self.quality += 2
        else:
            self.quality += 1


class Sulfuras(TradeableItem):
    def __init__(self, name: str, sell_in: int, quality: int):
        super().__init__(name, sell_in, quality, min_quality=80, max_quality=80)

    def update_quality(self):
        return

    def update_sell_in(self):
        return


class BackstagePasses(TradeableItem):
    def update_quality(self):
        if self.sell_in < 0:
            self.quality = 0
        elif self.quality == self.max_quality:
            return
        elif self.sell_in <= 5:
            self.quality += 3
        elif self.sell_in <= 10:
            self.quality += 2
        else:
            self.quality += 1


def create_tradable_item(item: Item, catalog: Dict) -> TradeableItem:
    for prefix, object in catalog.items():
        if item.name.lower().startswith(prefix):
            return object(name=item.name, quality=item.quality, sell_in=item.sell_in)
    return TradeableItem(name=item.name, quality=item.quality, sell_in=item.sell_in)
