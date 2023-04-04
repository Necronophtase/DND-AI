import AI_Base
from lib import *
# if enemy within normal range of longest attack, back up
# if enemy at edge of longest range, shoot, then back up one more
# else if enemy in long range of any attacks, approach while possible
# when cannot approach, shoot anyway
class Kite(AI_Base.AI):
    def __call__(self, pawn):
        global redTeam, blueTeam
        enemyList = redTeam if pawn.team else blueTeam
        chosenRange = max([atk.tags["range"][0] for atk in pawn.Actions if ("range" in atk.tags.keys())])
        while True:
            if len(enemyList)==0:
                return

            closeBoi = AI_Base.Closest_Foe(pawn, enemyList)
            currentRange = dist(pawn, closeBoi)

            if currentRange < chosenRange and (ch:=AI_Base.Flee(pawn, closeBoi)) is not None:
                yield ch
                continue
                
            if currentRange ==chosenRange and (ch:=AI_Base.ShortRangeShot(pawn, enemyList)) is not None:
                yield ch
                return
            
            if currentRange > chosenRange and (ch:=AI_Base.Approach(pawn, closeBoi)) is not None:
                yield ch
                continue

            if (ch:=AI_Base.LongRangeShot(pawn, enemyList)) is not None:
                yield ch
                return
            return

