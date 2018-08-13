from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt

HEIGHT = 500
WIDTH = 800
window = Tk()
window.title('Bubble Blaster')
c = Canvas(window, width = WIDTH, height = HEIGHT, bg = 'darkblue')
c.pack()


#SHIP
ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill = 'red')
ship_id2 = c.create_oval(0, 0, 30, 30, outline = 'red') 
SHIP_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)

SHIP_SPD = 10
def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SHIP_SPD)
        c.move(ship_id2, 0, -SHIP_SPD)
    elif event.keysym == 'Down':
        c.move(ship_id, 0, SHIP_SPD)
        c.move(ship_id2, 0, SHIP_SPD)
    elif event.keysym == 'Left':
        c.move(ship_id, -SHIP_SPD, 0)
        c.move(ship_id2, -SHIP_SPD, 0)
    elif event.keysym == 'Right':
        c.move(ship_id, SHIP_SPD, 0)
        c.move(ship_id2, SHIP_SPD, 0)    
c.bind_all('<Key>', move_ship)


#BUBS
bub_id = list()
bub_r = list()
bub_speed = list()
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPD = 10
GAP = 100
def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline = 'white')
    bub_id.append(id1)
    bub_r.append(randint(1, MAX_BUB_SPD))
    bub_speed.append(randint(1, MAX_BUB_SPD))
        
def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)

def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y

def del_bubble(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]
    
def clean_up_bubs():
    for i in range(len(bub_id) - 1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def collision_bubs():
    points = 0
    for bub in range(len(bub_id) - 1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):
            points += (bub_r[bub] + bub_speed[bub])
            del_bubble(bub)
    return points


#BOMBS
bomb_id = list()
bomb_r = list()
bomb_speed = list()
MIN_BOMB_R = 10
MAX_BOMB_R = 30
MAX_BOMB_SPD = 10
GAP = 100

def create_bomb():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BOMB_R, MAX_BOMB_R)
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline = 'red', fill = 'black')
    bomb_id.append(id1)
    bomb_r.append(randint(1, MAX_BOMB_SPD))
    bomb_speed.append(randint(1, MAX_BOMB_SPD))
     
def move_bombs():
    for i in range(len(bomb_id)):
        c.move(bomb_id[i], -bomb_speed[i], 0)

def del_bombs(i):
    del bomb_r[i]
    del bomb_speed[i]
    c.delete(bomb_id[i])
    del bomb_id[i]
    
def clean_up_bombs():
    for i in range(len(bomb_id) - 1, -1, -1):
        x, y = get_coords(bomb_id[i])
        if x < -GAP:
            del_bombs(i)

def collision_bombs():
    points = 0
    for bomb in range(len(bomb_id) - 1, -1, -1):
        if distance(ship_id2, bomb_id[bomb]) < (SHIP_R + bomb_r[bomb]):
            return "GAME OVER"
        else:
            return 0


#TIME AND SCORE
c.create_text(50, 30, text = 'TIME', fill = 'white')
c.create_text(150, 30, text = 'SCORE', fill = 'white')
time_text = c.create_text(50, 50, fill = 'white')
score_text = c.create_text(150, 50, fill = 'white')
def show_score(score):
    c.itemconfig(score_text, text = str(score))
def show_time(time_left):
    c.itemconfig(time_text, text = str(time_left))
    
BUB_CHANCE = 10
BOMB_CHANCE = 500
TIME_LIMIT = 30
BONUS_SCORE = 350
score = 0
bonus = 0
end = time() + TIME_LIMIT    
def main(event):
    global BUB_CHANCE
    global BOMB_CHANCE
    global TIME_LIMIT
    global BONUS_SCORE
    global score
    global bonus
    global end    
    #MAIN GAME LOOP
    
    while time() < end:
        if randint(1, BUB_CHANCE) == 1:
            create_bubble()
        if randint(1, BOMB_CHANCE) == 1:
            create_bomb()
        move_bubbles()
        move_bombs()
        clean_up_bombs()
        clean_up_bubs()
        GAME_OVER = collision_bombs()
        if GAME_OVER == "GAME OVER":
            break
        score += collision_bubs()
        if (int(score / BONUS_SCORE)) > bonus:
            bonus += 1
            end += TIME_LIMIT
        show_score(score)
        show_time(int(end - time()))
        window.update()
        sleep(0.01)
        
main(1)
BUB_CHANCE = 10
BOMB_CHANCE = 500
TIME_LIMIT = 30
BONUS_SCORE = 350
score = 0
bonus = 0
end = time() + TIME_LIMIT 

#GAME OVER
c.create_text(int(MID_X), int(MID_Y), text = 'GAME OVER', fill = 'white', font = ('Arial', 30))
c.create_text(int(MID_X), int(MID_Y + 30), text = 'Score: ' +  str(score), fill = 'white')
c.create_text(int(MID_X), int(MID_Y + 45), text = 'Bonus time: ' + str(bonus * TIME_LIMIT), fill = 'white')


btn_again = Button(text = 'Again')
btn_again.place(x = MID_X - 20, y = MID_Y + 60)
btn_again.bind('<Button-1>', main)
window.mainloop()