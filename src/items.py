class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class QualityExceedsMinException:
    "This error is raised when the quality of an item exceeds its minimum value"
    pass


class QualityExceedsMaxException:
    "This error is raised when the quality of an item exceeds its maximum value"
    pass


class TradeableItem(Item):
    def __init__(self, name, sell_in, quality, min_quality=0, max_quality=50):
        super().__init__(name, sell_in, quality)
        self.min_quality = 0
        self.max_quality = 50

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
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality, min_quality=80, max_quality=80)

    def update_quality(self):
        pass

    def update_sell_in(self):
        pass


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
