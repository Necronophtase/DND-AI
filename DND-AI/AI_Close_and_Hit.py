import AI_Base
from lib import *
#while enemy not in melee, approach nearest enemy
#if enemy in melee, use highest-damage stab (melee is 1 square here)
#when cannot move any longer, Dash
class Close_and_Hit(AI_Base.AI):
    def __call__(self, pawn):
        global redTeam, blueTeam
        enemyList = redTeam if pawn.team else blueTeam
        MaxMeleeRange =0
        for attack in pawn.Actions:
            if ("melee" in attack.tags.keys()) and (attack.tags["melee"]>=MaxMeleeRange):
                MaxMeleeRange=attack.tags["melee"]
        while True:
            if len(enemyList)==0: #if there are no enemies, leave
                return

            if (ch:=AI_Base.BasicMelee(pawn, enemyList)) is not None:
                yield ch
                continue

            if AI_Base.Enemy_Within(pawn, enemyList, MaxMeleeRange): #if we didn't attack, but we did have an enemy within melee, our action is expended already and our turn is over
                return
            
            if (ch:=AI_Base.Approach(pawn, AI_Base.Closest_Foe(pawn, enemyList))) is not None:
                yield ch
                continue
            
            if pawn.MovementSpent>=pawn.move and pawn.ActionOpen: #if we finished moving without attacking, Dash
                for i in range(len(pawn.Actions)):
                    if "dash" in pawn.Actions[i].tags.keys():
                        yield (1, i, None)
                        break
                continue

            if (ch:=AI_Base.ShortRangeShot(pawn, enemyList)) is not None: #we shouldn't ever get here unless it's somehow blocked from moving 
                yield ch
                return

            if (ch:=AI_Base.LongRangeShot(pawn, enemyList)) is not None:
                yield ch
                return
            return
            