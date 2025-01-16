class Character:
    def __init__(self, name, gold, strength, dexterity, constitution, intelligence, wisdom, charisma, health, agility, inventory, other_info):
        self.name = name
        self.gold = gold
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.health = health
        self.agility = agility
        self.level = 0
        self.inventory = inventory
        self.other_info = other_info
    
    def get_stat(self, stat: str) -> int: 
        '''This is a method from the Character class that allows you to get a stat from the following: name, gold, strength, dexterity, constitution, intelligence, wisdom, charisma, health, agility, level, inventory, other_info.'''
        return getattr(self, stat)
    
    def set_stat(self, stat: str, value: int) -> None:
        '''This is a method from the Character class that allows you to modify a stat from the following: name, gold, strength, dexterity, constitution, intelligence, wisdom, charisma, health, agility, level, inventory, other_info.'''
        setattr(self, stat, value)

    def summary(self) -> str:
        return f"Name: {self.name}\nGold: {self.gold}\nStrength: {self.strength}\nDexterity: {self.dexterity}\nConstitution: {self.constitution}\nIntelligence: {self.intelligence}\nWisdom: {self.wisdom}\nCharisma: {self.charisma}\nHealth: {self.health}\nAgility: {self.agility}\nLevel: {self.level}\nInventory: {self.inventory}\nOther Info: {self.other_info}"
    

'''
'''