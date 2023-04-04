from Agent import *

class Ogre(Agent):
    def __init__(self, start_pos, AI_class, Team=True):
        Agent.__init__(self, start_pos, AI_class, Team, Size=size.Large)
        self.STR=4
        self.DEX=-1
        self.CON=3
        self.INT=-3
        self.WIS=-2
        self.CHA=-2
        self.AC=11
        self.HP_max=self.HP_now=59
        self.move=8
        self.prof=2
        #now build the actions:
        self.Actions = [
            Action({"melee":1, "dmg":13, "hitbonus":(lambda:self.STR+self.prof), "dmgroll":(lambda:d(8, 2)+self.STR), "dmgtype":dmg.BLUD_MUND }, self.greatclub,   lambda _: True),
            Action({"range":(6, 24), "dmg":11, "hitbonus":(lambda:self.STR+self.prof), "dmgroll":(lambda:d(6, 2)+self.STR), "dmgtype":dmg.PIERCE_MUND}, self.javelin, lambda _: True)
            ] + self.Actions
            
    def greatclub(self, target):
        if self.AttackMachinery(target, self.Actions[0]):
            pass

    def javelin(self, target):
        if self.AttackMachinery(target, self.Actions[1]):
            pass