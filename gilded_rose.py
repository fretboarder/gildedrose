class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class GildedRose(object):
    def __init__(self, items: list[Item]):
        self.items = items

    def update_quality(self):
        for i, item in enumerate(self.items):
            match item.name:
                case "Aged Brie": self.update_brie(i)
                case "Sulfuras, Hand of Ragnaros": self.update_sulfuras(i)
                case "Backstage passes to a TAFKAL80ETC concert": self.update_backstage_pass(i)
                case "Conjured Mana Cake": self.update_conjured_item(i)
                case _: self.update_regular_item(i)

    def _cycle(self, i: int, new_qual, limit_func, limit_val):
        self.items[i].sell_in -= 1
        self.items[i].quality = limit_func(new_qual, limit_val)

    def update_regular_item(self, i: int) -> None:
        reduction = 1 if self.items[i].sell_in > 0 else 2
        self._cycle(i, self.items[i].quality - reduction, max, 0)

    def update_conjured_item(self, i: int) -> None:
        reduction = 2 if self.items[i].sell_in > 0 else 4
        self._cycle(i, self.items[i].quality - reduction, max, 0)

    def update_brie(self, i: int) -> None:
        reduction = -1 if self.items[i].sell_in > 0 else -2
        self._cycle(i, self.items[i].quality - reduction, min, 50)

    def update_backstage_pass(self, i: int) -> None:
        s, q = self.items[i].sell_in, self.items[i].quality
        reduction = q if s <= 0 else -3 if s <= 5 else -2 if s <= 10 else -1
        self._cycle(i, self.items[i].quality - reduction, min, 50)

    def update_sulfuras(self, i: int) -> None:
        self.items[i].quality = 80

