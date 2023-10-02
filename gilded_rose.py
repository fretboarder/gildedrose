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
                case "Aged Brie":
                    self.items[i] = self.update_brie(item)
                case "Sulfuras, Hand of Ragnaros":
                    self.items[i] = self.update_sulfuras(item)
                case "Backstage passes to a TAFKAL80ETC concert":
                    self.items[i] = self.update_backstage_pass(item)
                case "Conjured Mana Cake":
                    self.items[i] = self.update_conjured_item(item)
                case _:
                    self.items[i] = self.update_regular_item(item)

    @staticmethod
    def _update(item: Item, reduction: int, limit_func, limit_val) -> Item:
        name, sell_in, quality = item.__dict__.values()
        return Item(name, sell_in - 1, limit_func(quality-reduction, limit_val))

    def update_regular_item(self, item: Item) -> Item:
        reduction = 1 if item.sell_in > 0 else 2
        return self._update(item, reduction, max, 0)

    def update_conjured_item(self, item: Item) -> Item:
        reduction = 2 if item.sell_in > 0 else 4
        return self._update(item, reduction, max, 0)

    def update_brie(self, item: Item) -> Item:
        reduction = -1 if item.sell_in > 0 else -2
        return self._update(item, reduction, min, 50)

    def update_backstage_pass(self, item: Item) -> Item:
        reduction = (
            item.quality if item.sell_in <= 0
            else -3 if item.sell_in <= 5
            else -2 if item.sell_in <= 10
            else-1
        )
        return self._update(item, reduction, min, 50)

    def update_sulfuras(self, item: Item) -> Item:
        return Item(item.name, item.sell_in, 80)
