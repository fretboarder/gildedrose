from typing import NamedTuple
import pytest as pt
from gilded_rose import Item, GildedRose

class ItemAttr(NamedTuple):
    sell_in: int
    quality: int

@pt.fixture
def updater(request):
    def _update(item: Item, cycles=1) -> GildedRose:
        g = GildedRose([item])
        for c in range(cycles):
            g.update_quality()
        return g
    return _update


@pt.mark.parametrize("attr,result", [
    (ItemAttr(10, 10), ItemAttr(9, 9)), # regulare degrading
    (ItemAttr(10, 0), ItemAttr(9, 0)),  # limit 0
    (ItemAttr(0, 10), ItemAttr(-1, 8)), # double degrading
    (ItemAttr(0, 1), ItemAttr(-1, 0))   # double degrading with limit
])
def test_regular(updater, attr: ItemAttr, result):
    g = updater(Item("Regular", *attr))
    assert g.items[0].sell_in == result.sell_in
    assert g.items[0].quality == result.quality


@pt.mark.parametrize("attr,result", [
    (ItemAttr(10, 10), ItemAttr(9, 11)), # regulare degrading
    (ItemAttr(10, 50), ItemAttr(9, 50)), # limit 50
    (ItemAttr(0, 10), ItemAttr(-1, 12)), # double degrading
    (ItemAttr(0, 49), ItemAttr(-1, 50))  # double degrading with limit
])
def test_brie(updater, attr: ItemAttr, result):
    g = updater(Item("Aged Brie", *attr))
    assert g.items[0].sell_in == result.sell_in
    assert g.items[0].quality == result.quality


@pt.mark.parametrize("attr,result", [
    (ItemAttr(20, 10), ItemAttr(19, 11)), # regular degrading
    (ItemAttr(11, 10), ItemAttr(10, 11)), # regular degrading
    (ItemAttr(10, 11), ItemAttr(9, 13)),  # regular degrading
    (ItemAttr(6, 10), ItemAttr(5, 12)),   # regular degrading
    (ItemAttr(5, 12), ItemAttr(4, 15)),   # regular degrading
    (ItemAttr(1, 15), ItemAttr(0, 18)),   # regular degrading
    (ItemAttr(0, 18), ItemAttr(-1, 0)),   # regular degrading
    (ItemAttr(6, 49), ItemAttr(5, 50)),   # degrading with limit
    (ItemAttr(1, 48), ItemAttr(0, 50)),   # degrading with limit
])
def test_backstage(updater, attr: ItemAttr, result):
    g = updater(Item("Backstage passes to a TAFKAL80ETC concert", *attr))
    assert g.items[0].sell_in == result.sell_in
    assert g.items[0].quality == result.quality

@pt.mark.parametrize("attr,result", [
    (ItemAttr(0, 80), ItemAttr(0, 80)), # regulare degrading
    (ItemAttr(-1, 80), ItemAttr(-1, 80)), # regulare degrading
])
def test_sulfuras(updater, attr: ItemAttr, result: ItemAttr) -> None:
    g = updater(Item("Sulfuras, Hand of Ragnaros", *attr))
    assert g.items[0].sell_in == result.sell_in
    assert g.items[0].quality == result.quality

# @pt.mark.parametrize("attr,result", [
#     (ItemAttr(10, 10), ItemAttr(9, 8)), # regulare degrading
#     (ItemAttr(10, 0), ItemAttr(9, 0)),  # limit 0
#     (ItemAttr(0, 10), ItemAttr(-1, 6)), # double degrading
#     (ItemAttr(0, 1), ItemAttr(-1, 0))   # double degrading with limit
# ])
# def test_conjured(updater, attr: ItemAttr, result):
#     g = updater(Item("Conjured Mana Cake", *attr))
#     assert g.items[0].sell_in == result.sell_in
#     assert g.items[0].quality == result.quality

if __name__ == '__main__':
    pt.main(["-v", "--cov=."])
