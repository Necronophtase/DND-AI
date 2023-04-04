import AI_Base
from lib import *
#if enemy in melee, use highest-damage stab (melee is 5 feet here)
#else if enemy in normal range of any ranged attacks, shoot
#else if enemy in long range of any attacks, approach while possible
#when cannot approach, shoot anyway
class Shoot_and_Close(AI_Base.AI):
    def __call__(self, pawn):
        global redTeam
        global blueTeam
        enemyList = redTeam if pawn.team else blueTeam
        while True:
            if len(enemyList)==0:
                return

            if (ch:=AI_Base.BasicMelee(pawn, enemyList)) is not None:#first, try to do a melee
                yield ch
                return
            
            if (ch:=AI_Base.ShortRangeShot(pawn, enemyList)) is not None:#then try to shoot in short range
                yield ch
                return 

            if (ch:=AI_Base.Approach(pawn, AI_Base.Closest_Foe(pawn, enemyList))) is not None: #then step closer to whatever enemy is closest and start over from the top
                yield ch 
                continue

            if (ch:=AI_Base.LongRangeShot(pawn, enemyList)) is not None: #if there's no more moving to be done, take the best long-range shot possible
                yield ch
                return
            return

