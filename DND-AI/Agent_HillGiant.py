from Agent import *
class HillGiant(Agent):
    def __init__(self, start_pos, AI_class, Team=True):
        Agent.__init__(self, start_pos, AI_class, Team, Size=size.Huge)
        self.STR=5
        self.DEX=-1
        self.CON=4
        self.INT=-3
        self.WIS=-1
        self.CHA=-2
        self.AC=13
        self.HP_max=self.HP_now=105
        self.move=8
        self.prof=3
        #now build the actions:
        self.Actions = [
            Action({"melee":2, "dmg":36, "multi":(1,1)}, self.multiattack, lambda _: True),
            Action({"melee":2, "dmg":18, "hitbonus":(lambda:self.STR+self.prof), "dmgroll":(lambda:d(8, 3)+self.STR), "dmgtype":dmg.BLUD_MUND }, self.greatclub, lambda _: True),
            Action({"range":(12, 48), "dmg":21, "hitbonus":(lambda:self.STR+self.prof), "dmgroll":(lambda:d(10, 3)+self.STR), "dmgtype":dmg.BLUD_MUND}, self.rockthrow, lambda _: True),
            Action({"melee":1, "dmg":26, "hitbonus":(lambda:self.STR+self.prof), "dmgroll":(lambda: d(6, 6)+self.STR), "dmgtype":dmg.BLUD_MUND}, self.squash, lambda _: _.Size<size.Large)
            ] + self.Actions


    def multiattack(self, target):
        self.greatclub(target)
        self.greatclub(target)

    def greatclub(self, target):
        if self.AttackMachinery(target, self.Actions[1]):
            pass

    def rockthrow(self, target):
        if self.AttackMachinery(target, self.Actions[2]):
            pass

    def squash(self, target):
        if self.AttackMachinery(target, self.Actions[3]):
            self.pos=target.pos
            self.HillGiantProneGrapple(self, target)

    class HillGiantProneGrapple(Condition_Base.Prone):
        def __init__(self, carrier, target):
            super().__init__(carrier)
            self.grapple = Condition_Base.Grappled(target)
            
        def remove(self):
            self.grapple.remove()
            super().remove()