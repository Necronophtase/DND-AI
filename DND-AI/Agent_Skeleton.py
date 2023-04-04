from Agent import *

class Skeleton(Agent):
    def __init__(self, start_pos, AI_class, Team=True):
        Agent.__init__(self, start_pos, AI_class, Team)
        self.DEX=2
        self.CON=2
        self.INT=-2
        self.WIS=-1
        self.CHA=-3
        self.AC=13
        self.HP_max=self.HP_now=13
        self.move=6
        self.prof=2
        #now build the actions:
        self.Actions = [
            Action({"melee":1, "dmg":5, "hitbonus":(lambda:self.DEX+self.prof), "dmgroll":(lambda:d(6)+self.DEX), "dmgtype":dmg.PIERCE_MUND }, self.shortsword,   lambda _: True),
            Action({"range":(16, 64), "dmg":5, "hitbonus":(lambda:self.DEX+self.prof), "dmgroll":(lambda:d(6)+self.DEX), "dmgtype":dmg.PIERCE_MUND}, self.shortbow, lambda _: True)
            ] + self.Actions

    def TakeHit(self, damage, kind):
        if kind==dmg.POISON:
            damage=0
        if kind==dmg.BLUD_MAG or kind==dmg.BLUD_MUND:
            damage*=2
        return super().TakeHit(damage, kind)

    def shortsword(self, target):
        if self.AttackMachinery(target, self.Actions[0]):
            pass

    def shortbow(self, target):
        if self.AttackMachinery(target, self.Actions[1]):
            pass