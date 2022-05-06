# -*- coding: utf-8 -*-
import pytest as pytest

from src.gilded_rose import GildedRose
from src.items import (
    Item,
    QualityExceedsMaxException,
    factory_tradable_item,
    QualityExceedsMinException,
)


def test_foo():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert "foo" == items[0].name


@pytest.mark.parametrize(
    "item_type,quality,sell_in,expected_sell_in",
    [
        ("basic", 10, 1, 0),
        ("Sulfuras, Hand of Ragnaros", 80, 1, 1),
    ],
)
def test_update_quality_sell_in(item_type, quality, sell_in, expected_sell_in):
    items = [Item(item_type, sell_in, quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert expected_sell_in == gilded_rose.tradaeble_items[0].sell_in


@pytest.mark.parametrize(
    "item_type,quality,sell_in,expected_quality",
    [
        ("basic", 10, 1, 9),
        ("basic", 10, -1, 8),
        ("basic", 0, -1, 0),
        ("basic", 0, 1, 0),
        ("Aged Brie", 10, 1, 11),
        ("Aged Brie", 10, -1, 12),
        ("Aged Brie", 0, -1, 2),
        ("Aged Brie", 0, 1, 1),
        ("Aged Brie", 50, -1, 50),
        ("Aged Brie", 50, 1, 50),
        ("Sulfuras, Hand of Ragnaros", 80, 1, 80),
        ("Sulfuras, Hand of Ragnaros", 80, -1, 80),
        ("Backstage passes to a TAFKAL80ETC concert", 10, 1, 13),
        ("Backstage passes to a TAFKAL80ETC concert", 10, 10, 12),
        ("Backstage passes to a TAFKAL80ETC concert", 10, 11, 11),
        ("Backstage passes to a TAFKAL80ETC concert", 10, -1, 0),
        ("Backstage passes to a TAFKAL80ETC concert", 0, -1, 0),
        ("Backstage passes to a TAFKAL80ETC concert", 50, 5, 50),
        ("Backstage passes to a TAFKAL80ETC concert", 50, 10, 50),
        ("Backstage passes to a TAFKAL80ETC concert", 50, 11, 50),
    ],
)
def test_update_quality_quality(item_type, quality, sell_in, expected_quality):
    items = [Item(item_type, sell_in, quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert expected_quality == gilded_rose.tradaeble_items[0].quality


@pytest.mark.parametrize(
    "item",
    [
        Item("basic", 0, 51),
        Item("Aged Brie", 0, 51),
        Item("Sulfuras, Hand of Ragnaros", 0, 81),
        Item("Backstage passes to a TAFKAL80ETC concert", 0, 51),
    ],
)
def test_create_tradable_item_quality_upperlimit(item: Item):
    with pytest.raises(QualityExceedsMaxException):
        factory_tradable_item(item)


@pytest.mark.parametrize(
    "item",
    [
        Item("basic", 0, -1),
        Item("Aged Brie", 0, -1),
        Item("Sulfuras, Hand of Ragnaros", 0, 79),
        Item("Backstage passes to a TAFKAL80ETC concert", 0, -1),
    ],
)
def test_create_tradable_item_quality_lowerlimit(item: Item):
    with pytest.raises(QualityExceedsMinException):
        factory_tradable_item(item)
