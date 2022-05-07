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
        name: str = "",
        sell_in: int = 0,
        quality: int = 0,
        min_quality: int = 0,
        max_quality: int = 50,
    ):
        super().__init__(name, sell_in, quality)
        self._min_quality = min_quality
        self._max_quality = max_quality

    def set_min_quality(self, min_quality):
        self._min_quality = min_quality

    def set_max_quality(self, max_quality):
        self._max_quality = max_quality

    def get_quality(self):
        return self.quality

    def get_sell_in(self):
        return self.sell_in

    def daily_update(self):
        self.update_quality()
        self.update_sell_in()

    def update_quality(self):
        if self.quality == self._min_quality:
            return
        elif self.sell_in < 0:
            self.quality -= 2
        else:
            self.quality -= 1

    def update_sell_in(self):
        self.sell_in -= 1

    def check_quality(self):
        if self._max_quality < self.quality:
            raise QualityExceedsMaxException
        if self.quality < self._min_quality:
            raise QualityExceedsMinException


class DecoratorTradeableItem(TradeableItem):
    def __init__(self, tradeable_item: TradeableItem):
        super().__init__()
        self._tradeable_item = tradeable_item

    def get_quality(self):
        return self._tradeable_item.get_quality()

    def get_sell_in(self):
        return self._tradeable_item.get_sell_in()

    def check_quality(self):
        self._tradeable_item.check_quality()


class Legendary(DecoratorTradeableItem):
    """
    Decorator for a tradable item.
    Legendary items:
    - Don't expire
    - Keep their quality
    - Have a quality of 80
    """

    def __init__(self, tradeable_item: TradeableItem):
        super().__init__(tradeable_item=tradeable_item)
        self._tradeable_item.set_min_quality(80)
        self._tradeable_item.set_max_quality(80)

    def daily_update(self):
        return


class Conjured(DecoratorTradeableItem):
    """
    Decorator for a tradable item.
    Conjured items:
    - have their quality updates happen twice
    """

    def __init__(self, tradeable_item: TradeableItem):
        super().__init__(tradeable_item)

    def daily_update(self):
        self._tradeable_item.update_quality()
        self._tradeable_item.update_quality()
        self._tradeable_item.update_sell_in()


class AgedBrie(TradeableItem):
    """
    Aged Brie is an tradable item where
    - it increases in Quality the older it gets
    """

    def update_quality(self):
        if self.quality == self._max_quality:
            return
        elif self.sell_in < 0:
            self.quality += 2
        else:
            self.quality += 1


class BackstagePasses(TradeableItem):
    """
    Backstage passes for ... is a tradeable item where
    - it increases in Quality as its SellIn value approaches;
        Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but
        Quality drops to 0 after the concert
    """

    def update_quality(self):
        if self.sell_in < 0:
            self.quality = 0
        elif self.quality == self._max_quality:
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

TYPES = {"legendary": Legendary, "conjured": Conjured}


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


def _add_decorators(
    tradeable_item: TradeableItem,
) -> TradeableItem:
    for prefix, const in ITEM_INHERENT_TYPES.items():
        if prefix in tradeable_item.name.lower():
            return const(tradeable_item)

    for type_name, constructor in TYPES.items():
        if type_name in tradeable_item.name.lower():
            return constructor(tradeable_item)

    return tradeable_item
