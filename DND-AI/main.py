import pygame
import random
from lib import *
import AgentTypes
import AI_Types
from pygame.locals import (
    K_RETURN,
    KEYDOWN,
    K_ESCAPE,
    QUIT,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_SPACE
)
from Player import *
import easygui as gui

"""
To Do List:
~~~~~~~~~~~
- Differentiate between creature type and ai type in render
- Add mid-battle stats for each side
- scroll correctly
"""


def setup():
    msg = "Who them bitches?"
    title = "Setup Widget"
    creatures = ["[[Start Simulation]]"] + list(agentTypeDict.keys())
    creaturetype = gui.choicebox(msg, title, creatures)
    if creaturetype == "[[Start Simulation]]":
        return [creaturetype]
    archetypes = list(aiTypeDict.keys())
    archetypetype = gui.choicebox(msg, title, archetypes)
    fieldNames = ["Which Side?", "How many?", "Place them yourself? (y/n)"]
    fieldValues = [creaturetype, archetypetype]  # we start with blanks for the values
    fieldValues += gui.multenterbox(msg, title, fieldNames)
    return fieldValues

def place_randomly(side_data):
    global agentTypeDict, aiTypeDict, redTeam, blueTeam
    for _ in range(int(side_data[3])):
        condition = False
        # Probably a cleaner way to write this. 1 goes to the bottom of the screen and 2 goes to the top
        ystart = int(((int(side_data[2])) % 2) * SCREEN_HEIGHT / 2) + 2
        yend = int(ystart + SCREEN_HEIGHT / 2 + 2) - gridsize
        print(f"{side_data[2]} yields ystart:{ystart}, yend:{yend}")
        while not condition:
            coords = (random.randrange(2, SCREEN_WIDTH + 2, gridsize), random.randrange(ystart, yend, gridsize))
            condition = True
            for dude in dudes:
                if dude.rect.topleft == coords:
                    condition = False
        dudes.append(Player())
        dudes[-1].rect.topleft = coords

        #  moved this to its own function for editability's sake
        assignTeam()

        dudes[-1].info += side_data[0:2]

def make_sprites():
    global still_placing, done_placing, side_data, bogies, blueTeam, redTeam, initList, agentTypeDict, aiTypeDict

    if pygame.time.get_ticks() > 1500 and not (still_placing or done_placing):
        bogies = 0
        side_data = setup()
        if side_data[0] == "[[Start Simulation]]":
            done_placing = True
            beginInit()
        elif side_data[4] != "y":
            place_randomly(side_data)
        else:
            still_placing = True

    if pygame.mouse.get_pressed()[0] == 1 and still_placing:

        # this would have all been inside the constructor if it would have worked that way
        dudes.append(Player())
        pos = pygame.mouse.get_pos()
        dudes[-1].rect.center = (gridsize * int(pos[0] / gridsize) + 0.5 * gridsize + 1,
                                 gridsize * int(pos[1] / gridsize) + 0.5 * gridsize + 1)
        assignTeam()    # moved to its own function for editability

        dudes[-1].info = side_data[0:2]  # Give the Object its tags
        bogies += 1
        if bogies == int(side_data[3]):
            still_placing = False
        pygame.time.delay(150)  # delay to not create more than one player object

def assignTeam():
    print(f"assigning pos. \nsprite={dudes[-1].rect.topleft}\nagent={px_to_tile((dudes[-1].rect.left, dudes[-1].rect.top, 0))}")
    print(f"does {dudes[-1].rect.topleft} == {tile_to_px(px_to_tile((dudes[-1].rect.left, dudes[-1].rect.top, 0)))}")
    if int(side_data[2]) == 1:
        blueTeam.append(agentTypeDict[side_data[0]](px_to_tile((dudes[-1].rect.left, dudes[-1].rect.top, 0)),
                                                    aiTypeDict[side_data[1]](), Team=True))
        dudes[-1].assign_Agent(blueTeam[-1])
    else:
        redTeam.append(agentTypeDict[side_data[0]](px_to_tile((dudes[-1].rect.left, dudes[-1].rect.top, 0)),
                                                   aiTypeDict[side_data[1]](), Team=False))
        dudes[-1].assign_Agent(redTeam[-1])

    # add creature type name and AI type name to sprite object for prints and display
    dudes[-1].creature_type = side_data[0]
    dudes[-1].archetype_type = side_data[1]
    dudes[-1].name = side_data[0] + " " + side_data[1] # to more easily print "Ogre Brute", for example

def nameSprites():
    sprites = [agent.sprite for agent in initList]
    for dude_index in range(len(sprites)):
        dude = sprites[dude_index]
        team = "\u001b[34mBlue " if dude.agent.team else "\u001b[32mGreen " # ANSI color codes to make it look pretty
        count = 1   # how many creatures of the same types on the same team, including this one
        for creature in sprites[0:dude_index]:
            if creature.creature_type == dude.creature_type and creature.archetype_type == dude.archetype_type and \
                    creature.agent.team == dude.agent.team:
                count += 1
        dude.name = team + dude.creature_type + " " + dude.archetype_type + " #" + str(count) + "\u001b[0m"
        print(f"{dude_index+1}: {dude.name}")

def beginInit():
    global initList, redTeam, blueTeam
    LLL = []
    for person in redTeam + blueTeam:
        LLL.append((person, person.Initiative()))
    LLL.sort(key=lambda x: x[1], reverse=True)
    [initList.append(x[0]) for x in LLL]
    print(initList)
    nameSprites()

pygame.init()
# Run until the user asks to quit
running = True
game_paused = False
still_placing = False
done_placing = False
side_data = []
bogies = 0
agentTypeDict = {
    "Bandit":       AgentTypes.Bandit,
    "Skeleton":     AgentTypes.Skeleton,
    "Ogre":         AgentTypes.Ogre,
    "Hill Giant":   AgentTypes.HillGiant,
    "Salamander":   AgentTypes.Salamander
}
aiTypeDict = {
    "Defunct":       AI_Types.Shoot_and_Close,
    "Brute":        AI_Types.Close_and_Hit,
    "Archer":       AI_Types.Kite
}

while running:
    # Allow for pausing, exiting, etc.
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE or event.key == K_RETURN:
                running = False
            elif event.key == K_SPACE:
                game_paused = not game_paused
        elif event.type == QUIT:
            running = False
    
    make_sprites()
    if done_placing:
        try:
            for dude in initList:
                if not dude.isDead:
                    print(f"\n\tStarting next turn")
                    if not game_paused:
                        dude.take_turn()
                        refresh()
                        clock.tick(200*lib.SimSpeed)
        except customStopIteration:
            running = False

    refresh()
    clock.tick(200*lib.SimSpeed)

# Done! Time to quit.
pygame.quit()