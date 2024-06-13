from math import ceil, log
from random import randint
from time import sleep
from numpy import Infinity
import pygame
from keyboard import is_pressed
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
w,h = screen.get_size()
pygame.init()
clock = pygame.time.Clock()
tier1 = [(screen, (255,0,0), (40+200,40), 35), 200, 0, False, 10, 0, 10, 0, False, 1]
tier2 = [(screen, (255,127,0), (40+200,40*3), 35), 200, 0, False, 10, 0, 10, 0, False, 1]
tier3 = [(screen, (255,255,0), (40+200,40*5), 35), 200, 0, False, 10, 0, 10, 0, False, 1]
tier4 = [(screen, (127,255,0), (40+200,40*7), 35), 200, 0, False, 10, 0, 10, 2, False, 1]
tier5 = [(screen, (0,255,0), (40+200,40*9), 35), 200, 0, False, 10, 0, 10, 10, False, 1]
tier6 = [(screen, (0,255,255), (40+200,40*11), 35), 200, 0, False, 10, 0, 10, 51, False, 1]
tier7 = [(screen, (0,127,255), (40+200,40*13), 35), 200, 0, False, 10, 0, 10, 255, False, 1]
tier8 = [(screen, (0,0,255), (40+200,40*15), 35), 200, 0, False, 10, 0, 10, 1011, False, 1]
tier9 = [(screen, (127,0,255), (40+200,40*17), 35), 200, 0, False, 10, 0, 10, 6005, False, 1]
tiers = [tier1, tier2, tier3, tier4, tier5, tier6, tier7, tier8, tier9]
machineunlocks = [False, False, False, False, False, False, False, False]
prestigemods = [None, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
machinecosts = [0, 0, 0, 0, 0, 0, 0]
machinepoints = [6005,6005,6005,6005,6005,6005,Infinity]
money = 0
buymode = "All"
font = pygame.font.Font("PixeloidSans.ttf", 30)
upgradetimer = 0
buynexttimer = 0
sfxtimer = 0
buynexttier = 1
prestigepoints = 0
checkbox = pygame.image.load("checkbox.png")
checkbox = pygame.transform.scale(checkbox, (25,25))
prestigearrow = pygame.image.load("prestige_arrow.png").convert_alpha()
prestigearrow = pygame.transform.scale(prestigearrow, (200,200))
prestigearrowrect = prestigearrow.get_rect()
prestigearrowrect.bottomright = (w,h)
prestiging = False
ascending = False
insettings = False
sfx = True
pygame.mixer.set_num_channels(99)
def logprot(num, base):
    try:
        return log(num, base)
    except ValueError:
        return 0
def zerodivprot(numerator, denominator):
    try:
        return numerator/denominator
    except ZeroDivisionError:
        return 0
def converttosci(num: int, threshold: float = 10000, decimals: int = 2):
    if num >= threshold or num <= -threshold:
        return f"{num:.{decimals}e}"
    else:
        return round(num)
def is_clicked(rect: pygame.Rect, timer: float, time: float = 0.2):
    return rect.collidepoint(pygame.mouse.get_pos()) and timer >= time and pygame.mouse.get_pressed()[0]
def play(filename : str, channel: int):
    pygame.mixer.Channel(channel).play(pygame.mixer.Sound(f'{filename}'))
    return None
def colorchange(rect: pygame.Rect, colorbefore: tuple[int, int, int], colorafter: tuple[int, int, int], moneyforbuy: int, width: int = 0, cornerradius: int = 10):
    if money >= moneyforbuy:
        return pygame.draw.rect(screen, colorafter, rect, width, cornerradius)
    else:
        return pygame.draw.rect(screen, colorbefore, rect, width, cornerradius)
while True:
    dt = clock.tick(60)
    screen.fill((0,0,0))
    if not prestiging and not ascending and not insettings:
        prestigepoints = 0
        if not machineunlocks[6]:
            try:
                buynextrect = colorchange(pygame.Rect(w-150, (h-100)/2, 150, 100), (100,100,100), (170,170,170), tiers[buynexttier-1][5])
                buynextcosttext = font.render("$"+str(tiers[buynexttier-1][5]), 1, (0,255,0))
            except IndexError:
                buynextrect = colorchange(pygame.Rect(w-150, (h-100)/2, 150, 100), (100,100,100), (170,170,170), machinecosts[buynexttier-10])
                buynextcosttext = font.render("$"+str(machinecosts[buynexttier-10]), 1, (0,255,0))
            buynextcosttextrect = buynextcosttext.get_rect()
            buynextcosttextrect.midtop = buynextrect.center
            buynexttext = font.render("Buy Next", 1, (255,255,255))
            buynexttextrect = buynexttext.get_rect()
            buynexttextrect.midbottom = buynextrect.center
            screen.blit(buynexttext, buynexttextrect)
            screen.blit(buynextcosttext, buynextcosttextrect)
        else:
            buynextrect = pygame.draw.rect(screen, (0,0,0), pygame.Rect(w-150, (h-100)/2, 150, 100), border_radius=10)
            # buynextcosttext = font.render("Ascend", 1, (0,255,0))
            # buynextcosttextrect = buynextcosttext.get_rect()
            # buynextcosttextrect.center = buynextrect.center
            # screen.blit(buynextcosttext, buynextcosttextrect)
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        if is_pressed("escape"):
            exit()
        varstochange = 0
        for n in range(len(tiers)):
            if tiers[n][3]:
                varstochange += 3
                tiers[n][2] += tiers[n][1]*(dt/1000)
                tiercirc = pygame.draw.circle(*tiers[n][0])
                tieroutrect = pygame.draw.rect(screen, tiers[n][0][1], pygame.Rect(100+200, tiers[n][0][2][1]-30, 500, 60), 8, 10)
                pygame.draw.rect(screen, tiers[n][0][1], pygame.Rect(100+200, tiers[n][0][2][1]-30, tiers[n][2], 60), border_radius=10)
                tieruprect = colorchange(pygame.Rect(630+200, tiers[n][0][2][1]-35, 150, 70), (100,100,100), (170,170,170), tiers[n][4])
                upcostsci = converttosci(tiers[n][4])
                upcosttext = font.render("$"+str(upcostsci), 1, (0,255,0))
                upcosttextrect = upcosttext.get_rect()
                upcosttextrect.center = tieruprect.center
                screen.blit(upcosttext, upcosttextrect)
                earnsci = converttosci(tiers[n][6])
                font = pygame.font.Font("PixeloidSans.ttf", 20)
                earntext = font.render("Earn: $"+str(earnsci), 1, (100,100,100))
                font = pygame.font.Font("PixeloidSans.ttf", 30)
                earntextrect = earntext.get_rect()
                earntextrect.midleft = (tieruprect.midright[0]+30, tieruprect.midright[1])
                screen.blit(earntext, earntextrect)
                if tiers[n][2] >= 500:
                    money += tiers[n][6]
                    tiers[n][2] = 0
                    if sfx:
                        play("beep.mp3", n)
                if is_clicked(tieruprect, upgradetimer) and money >= tiers[n][4]:
                    if buymode == "1":
                        tiers[n][6] *= (1.05+((n)/200))
                        tiers[n][4] *= (1.1+((n)/100))
                        tiers[n][9] += 1
                        money -= tiers[n][4]
                        upgradetimer = 0
                        if not tiers[n][8]:
                            if tiers[n][9] == 10:
                                tiers[n][6] *= 3
                                tiers[n][8] = True
                    else:
                        while tiers[n][9] < 400 and money >= tiers[n][4]:
                            tiers[n][6] *= (1.05+((n)/200))
                            tiers[n][4] *= (1.1+((n)/100))
                            tiers[n][9] += 1
                            money -= tiers[n][4]
                            upgradetimer = 0
                            if not tiers[n][8]:
                                if tiers[n][9] == 10:
                                    tiers[n][6] *= 3
                                    tiers[n][8] = True
                prestigepoints += tiers[n][7]
            if is_clicked(buynextrect, buynexttimer) and buynexttier == (n+1) and money >= tiers[n][5]:
                buynexttier += 1
                money -= tiers[n][5]
                tiers[n][3] = not tiers[n][3]
                buynexttimer = 0
        for n in range(len(machineunlocks)):
            if machineunlocks[n]:
                prestigepoints += machinepoints[n]
            try:
                if is_clicked(buynextrect, buynexttimer) and buynexttier == (n+10) and money >= machinecosts[n]:
                    buynexttier += 1
                    money-=machinecosts[n]
                    machineunlocks[n] = not machineunlocks[n]
                    buynexttimer = 0
            except IndexError:
                pass # ascending = True
        if prestigepoints > 0:
            screen.blit(prestigearrow, prestigearrowrect)
            prestigepointssci = converttosci(prestigepoints, decimals = 0)
            prestigepointtext = font.render(str(prestigepointssci), 1, (200,200,0))
            prestigepointtextrect = prestigepointtext.get_rect()
            prestigepointtextrect.center = prestigearrowrect.center
            screen.blit(prestigepointtext, prestigepointtextrect)
            if is_clicked(prestigearrowrect, 99, 0):
                prestiging = True
        settingsicon = pygame.image.load("settings.png")
        settingsicon = pygame.transform.scale(settingsicon, (75,75))
        settingsiconrect = settingsicon.get_rect()
        settingsiconrect.topleft = (0,0)
        screen.blit(settingsicon, settingsiconrect)
        if is_clicked(settingsiconrect, 99, 0):
            insettings = True
        moneysci = converttosci(money)
        moneytext = font.render("Money: $"+str(moneysci), 1, (0,255,0))
        moneytextrect = moneytext.get_rect()
        moneytextrect.topright = (w,0)
        font = pygame.font.Font("PixeloidSans.ttf", 20)
        consttext3 = font.render("To prestige:", 1, (100,100,100))
        consttext3rect = consttext3.get_rect()
        consttext3rect.midtop = (100,round(h/2))
        if tier4[3]:
            consttext2 = checkbox
        else:
            consttext2 = font.render("Unlock tier 4", 1, ((100,100,100)))
        consttext2rect = consttext2.get_rect()
        consttext2rect.midbottom = consttext3rect.midtop
        consttext1 = font.render("To ascend:", 1, (100,100,100))
        consttext1rect = consttext1.get_rect()
        consttext1rect.midbottom = consttext2rect.midtop
        if machineunlocks[6]:
            consttext4 = checkbox
        else:
            consttext4 = font.render("Finish the machine", 1, ((100,100,100)))
        consttext4rect = consttext4.get_rect()
        consttext4rect.midtop = consttext3rect.midbottom
        screen.blit(consttext1, consttext1rect)
        screen.blit(consttext2, consttext2rect)
        screen.blit(consttext3, consttext3rect)
        screen.blit(consttext4, consttext4rect)
        screen.blit(moneytext, moneytextrect)
        font = pygame.font.Font("PixeloidSans.ttf", 30)
        if sfx:
            if not pygame.mixer.Channel(10).get_busy():
                play("bgm.mp3", 10)
    elif insettings:
        sfxbutton = pygame.draw.rect(screen, (100, 100, 100), pygame.Rect((w / 2 - 50, h / 2 - 50), (100, 100)), 10, 10)
        if sfx:
            sfxicon = pygame.image.load("volumeon.png")
        else:
            sfxicon = pygame.image.load("volumeoff.png")
        sfxicon = pygame.transform.scale(sfxicon, (75,75))
        sfxiconrect = sfxicon.get_rect()
        sfxiconrect.center = sfxbutton.center
        screen.blit(sfxicon, sfxiconrect)
        settingsiconrect.topright = (w, 0)
        screen.blit(settingsicon, settingsiconrect)
        if is_clicked(settingsiconrect, 99, 0):
            insettings = False
        if is_clicked(sfxbutton, sfxtimer):
            sfx = not sfx
            if sfx:
                play("bgm.mp3", 10)
            else:
                pygame.mixer.Channel(10).stop()
            sfxtimer = 0
        for event in pygame.event.get():
            if event.typeofupgrade == pygame.QUIT:
                exit()
        if is_pressed("escape"):
            exit()
    elif prestiging:
        vartochange = randint(1,varstochange)
        if vartochange%3 == 1:
            typeofupgrade = "Earn"
        elif vartochange%3 == 2:
            typeofupgrade = "Speed"
        else:
            typeofupgrade = "Cost"
        tier = f"Tier {ceil(vartochange/3)}"
        prestigemods[vartochange] += prestigepoints
        tier1 = [(screen, (255,0,0), (40+200,40), 35), 200+logprot((prestigemods[2]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[3])*0.25), 0*zerodivprot(1, (3+prestigemods[3])*0.25), logprot(prestigemods[1]**2, 10)*10+10, 0, False, 1]
        tier2 = [(screen, (255,127,0), (40+200,40*3), 35), 200+logprot((prestigemods[5]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[6])*0.25), 0*zerodivprot(1, (3+prestigemods[6])*0.25), logprot(prestigemods[4]**2, 10)*10+10, 0, False, 1]
        tier3 = [(screen, (255,255,0), (40+200,40*5), 35), 200+logprot((prestigemods[8]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[9])*0.25), 0*zerodivprot(1, (3+prestigemods[9])*0.25), logprot(prestigemods[7]**2, 10)*10+10, 0, False, 1]
        tier4 = [(screen, (127,255,0), (40+200,40*7), 35), 200+logprot((prestigemods[11]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[12])*0.25), 0*zerodivprot(1, (3+prestigemods[12])*0.25), logprot(prestigemods[10]**2, 10)*10+10, 2, False, 1]
        tier5 = [(screen, (0,255,0), (40+200,40*9), 35), 200+logprot((prestigemods[14]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[15])*0.25), 0*zerodivprot(1, (3+prestigemods[15])*0.25), logprot(prestigemods[13]**2, 10)*10+10, 10, False, 1]
        tier6 = [(screen, (0,255,255), (40+200,40*11), 35), 200+logprot((prestigemods[17]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[18])*0.25), 0*zerodivprot(1, (3+prestigemods[18])*0.25), logprot(prestigemods[16]**2, 10)*10+10, 51, False, 1]
        tier7 = [(screen, (0,127,255), (40+200,40*13), 35), 200+logprot((prestigemods[20]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[21])*0.25), 0*zerodivprot(1, (3+prestigemods[21])*0.25), logprot(prestigemods[19]**2, 10)*10+10, 255, False, 1]
        tier8 = [(screen, (0,0,255), (40+200,40*15), 35), 200+logprot((prestigemods[23]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[24])*0.25), 0*zerodivprot(1, (3+prestigemods[24])*0.25), logprot(prestigemods[22]**2, 10)*10+10, 1011, False, 1]
        tier9 = [(screen, (127,0,255), (40+200,40*17), 35), 200+logprot((prestigemods[26]**50), 10), 0, False, 10*zerodivprot(1, (3+prestigemods[27])*0.25), 0*zerodivprot(1, (3+prestigemods[27])*0.25), logprot(prestigemods[25]**2, 10)*10+10, 6005, False, 1]
        tiers = [tier1, tier2, tier3, tier4, tier5, tier6, tier7, tier8, tier9]
        machineunlocks = [False, False, False, False, False, False, False, False]
        machinecosts = [0, 0, 0, 0, 0, 0, 0]
        machinepoints = [6005,6005,6005,6005,6005,6005,Infinity]
        money = 0
        font = pygame.font.Font("PixeloidSans.ttf", 30)
        upgradetimer = 0
        buynexttimer = 0
        sfxtimer = 0
        buynexttier = 1
        checkbox = pygame.image.load("checkbox.png")
        checkbox = pygame.transform.scale(checkbox, (25,25))
        prestigearrow = pygame.image.load("prestige_arrow.png").convert_alpha()
        prestigearrow = pygame.transform.scale(prestigearrow, (200,200))
        prestigearrowrect = prestigearrow.get_rect()
        prestigearrowrect.bottomright = (w,h)
        prestiging = False
        ascending = False
        insettings = False
        typeofupgradetext = font.render(str(typeofupgrade), 1, (170,170,170))
        typeofupgradetextrect = typeofupgradetext.get_rect()
        typeofupgradetextrect.midright = (round(w/2)-10, round(h/2))
        screen.blit(typeofupgradetext, typeofupgradetextrect)
        pygame.display.update()
        sleep(1)
        tiertext = font.render(tier, 1, tiers[ceil(vartochange/3)-1][0][1])
        tiertextrect = tiertext.get_rect()
        tiertextrect.midleft = (round(w/2)+10, round(h/2))
        screen.blit(tiertext, tiertextrect)
        pygame.display.update()
        sleep(1)
    upgradetimer += dt/1000
    buynexttimer += dt/1000
    sfxtimer += dt/1000
    pygame.display.update()