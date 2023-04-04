from Agent import *
class Bandit(Agent):
    def __init__(self, start_pos, AI_class, Team=True):
        Agent.__init__(self, start_pos, AI_class, Team)
        self.DEX=1
        self.CON=1
        self.AC=12
        self.HP_max=self.HP_now=11
        self.move=6
        self.prof=2
        #now build the actions:
        self.Actions = [
            Action({"melee":1, "dmg":4, "hitbonus":(lambda:self.DEX+self.prof), "dmgroll":(lambda:d(6)+self.DEX), "dmgtype":dmg.SLASH_MUND }, self.scimitar, lambda _: True),
            Action({"range":(16, 64), "dmg":5, "hitbonus":(lambda:self.DEX+self.prof), "dmgroll":(lambda:d(8)+self.DEX), "dmgtype":dmg.PIERCE_MUND}, self.light_xbow, lambda _: True)
            ] + self.Actions

    def scimitar(self, target):
        if self.AttackMachinery(target, self.Actions[0]):
            pass

    def light_xbow(self, target):
        if self.AttackMachinery(target, self.Actions[1]):
            pass