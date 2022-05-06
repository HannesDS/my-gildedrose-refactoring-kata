class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class QualityExceedsMinException(Exception):
    "This error is raised when the quality of an item exceeds its minimum value"


class QualityExceedsMaxException(Exception):
    "This error is raised when the quality of an item exceeds its maximum value"


class TradeableItem(Item):
    """
    A Tradeable Item is a wrapper around an Item, that is tradeable and can be distributed
    by a company (eg. Gilded Rose).
    """

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


class Legendary(TradeableItem):
    """
    Decorator for a tradable item.
    Legendary items:
    - Don't expire
    - Keep their quality
    - Have a quality of 80
    """

    def __init__(self, tradeable_item: TradeableItem):
        super().__init__(
            tradeable_item.name,
            tradeable_item.sell_in,
            tradeable_item.quality,
            min_quality=80,
            max_quality=80,
        )
        self.tradable_item = tradeable_item

    def update_quality(self):
        return

    def update_sell_in(self):
        return


class AgedBrie(TradeableItem):
    def update_quality(self):
        if self.quality == self.max_quality:
            return
        elif self.sell_in < 0:
            self.quality += 2
        else:
            self.quality += 1


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


SPECIAL_ITEMS = {
    "aged brie": AgedBrie,
    "backstage passes": BackstagePasses,
}

ITEM_INHERENT_TYPES = {"sulfuras": Legendary}

TYPES = {"legendary": Legendary}


def factory_tradable_item(item: Item) -> TradeableItem:
    """
    Static factory method that creates the correct tradeable item based on the name.
    """
    tradeable_item = _create_tradeable_item(item)
    decorated_tradeable_item = _add_decorators(tradeable_item)
    decorated_tradeable_item.check_quality()
    return decorated_tradeable_item


def _create_tradeable_item(item: Item) -> TradeableItem:
    for item_name, const in SPECIAL_ITEMS.items():
        if item_name in item.name.lower():
            return const(name=item.name, quality=item.quality, sell_in=item.sell_in)
    return TradeableItem(name=item.name, quality=item.quality, sell_in=item.sell_in)


def _add_decorators(tradeable_item: TradeableItem) -> TradeableItem:
    for prefix, const in ITEM_INHERENT_TYPES.items():
        if prefix in tradeable_item.name.lower():
            return const(tradeable_item)

    for type, const in TYPES.items():
        if type in tradeable_item.name.lower():
            return const(tradeable_item)

    return tradeable_item
