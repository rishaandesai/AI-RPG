class Player:
    def __init__(self):
        self.stats = {
            'Health': 100.0,
            'Hunger': 50.0,
            'Thirst': 75.0,
            'Strength': 10.0,
            'Dexterity': 10.0,
            'Constitution': 10.0,
            'Intelligence': 10.0,
            'Wisdom': 10.0,
            'Charisma': 10.0,
            'Passive Perception': 10.0,
            'Hit Points': 50.0,
            'Death': 100.0
        }
        self.inventory = [
            'Short sword',
            'Leather tunic',
            'Wooden shield',
            "Backpack with 2 days' worth of rations",
            'Empty waterskin',
        ]
        self.gold = 10

    def update_stats(self, changes):
        for key, value in changes.items():
            if key in self.stats:
                try:
                    self.stats[key] += float(value)
                except ValueError:
                    pass

    def update_inventory(self, changes):
        for item in changes.get('add', []):
            if item not in self.inventory:
                self.inventory.append(item)
        for item in changes.get('remove', []):
            if item in self.inventory:
                self.inventory.remove(item)

    def update_gold(self, amount):
        self.gold += amount