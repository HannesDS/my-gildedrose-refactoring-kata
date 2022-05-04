# -*- coding: utf-8 -*-
import unittest

from src.gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEquals("foo", items[0].name)

    def test_update_quality_basic_item_negative_sell_in(self):
        quality = 10
        items = [Item("basic", -1, quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEquals(quality - 2, items[0].quality)

    def test_update_quality_basic_item_positive_sell_in(self):
        pass

    def test_update_quality_basic_item_quality_min(self):
        pass

    def update_quality_basic_item_quality_max(self):
        pass

    def update_quality_aged_brie(self):
        pass

    def update_quality_sulfuras(self):
        pass

    def update_quality_backstage_pass_negative_sell_in(self):
        pass

    def update_quality_backstage_pass_positive_sell_in(self):
        pass


if __name__ == "__main__":
    unittest.main()
