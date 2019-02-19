import turtle
import time
import random
import mysql.connector
import pandas
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.simpledialog import askstring
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

os.system('cls')

mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               passwd='hardikjain',
                               database='test')

cursors = mydb.cursor()

# FOR SNAKE GAME

sno = count_randomize = count_frenzymode = 0
randomize = True
frenzymode = False
difficulties = ['Easy', 'Medium', 'Hard', 'Insane!']
diff_choice = 1
total_score = 0
scores = []
high_scores = []
high_score = 0
levels = []
Dict_scores = {'Score': scores, 'High Score': high_scores}
scores_df = pandas.DataFrame(Dict_scores)


def options_snake():
    print('NOTE :Max high score will be considerd as high score for the graph and saving puropse\n')

    global diff_choice, difficulties, frenzymode
    root = Tk()
    root.geometry('400x350')
    root.title('Intro Snake Game')

    def play_frenzy():
        global frenzymode, difficulty, diff_choice, difficulties
        access_frenzy = askstring('FRENZY', 'Enter code to access Frenzy at start !', show='*')

        if access_frenzy == 'PLAYFRENZY':

            def play_button_frenzy():
                global frenzymode, diff_choice
                frenzymode = True
                diff_choice = difficulty.get()
                frenzywin.destroy()
                root.destroy()
                snake_game()

            difficulty = IntVar()
            difficulty.set(1)

            frenzywin = Toplevel(root)
            frenzywin.title('Frenzy Config')
            frenzywin.geometry('200x200')

            Label(frenzywin, text='Set Difficulty :', font='Courier 10').pack(anchor=NW)

            Radiobutton(frenzywin, text="Easy", variable=difficulty, command=diff_value, value=1).pack(anchor=W)
            Radiobutton(frenzywin, text="Medium", variable=difficulty, command=diff_value, value=2).pack(anchor=W)
            Radiobutton(frenzywin, text="Hard", variable=difficulty, command=diff_value, value=3).pack(anchor=W)
            Radiobutton(frenzywin, text="Insane", variable=difficulty, command=diff_value, value=4).pack(anchor=W)

            Label(frenzywin).pack(anchor=NW)
            Button(frenzywin, text='PLAY GAME', command=play_button_frenzy).pack()
        else:
            showerror('FRENZY', 'Wrong Password! Access Denied !!')

    def play_antirandomized():
        global randomize, difficulty, diff_choice, difficulties

        access_randomized = askstring('RANDOMIZE', 'Enter code to disable  randomize at start !', show='*')

        if access_randomized == 'PLAYAR':
            def play_button_randomize():
                global randomize, diff_choice
                randomize = False
                diff_choice = difficulty.get()
                randomwin.destroy()
                root.destroy()
                snake_game()

            difficulty = IntVar()
            difficulty.set(1)

            randomwin = Toplevel(root)
            randomwin.title('Disable Frenzy Config')
            randomwin.geometry('200x200')

            Label(randomwin, text='Set Difficulty :', font='Courier 10').pack(anchor=NW)

            Radiobutton(randomwin, text="Easy", variable=difficulty, command=diff_value, value=1).pack(anchor=W)
            Radiobutton(randomwin, text="Medium", variable=difficulty, command=diff_value, value=2).pack(anchor=W)
            Radiobutton(randomwin, text="Hard", variable=difficulty, command=diff_value, value=3).pack(anchor=W)
            Radiobutton(randomwin, text="Insane", variable=difficulty, command=diff_value, value=4).pack(anchor=W)

            Label(randomwin).pack(anchor=NW)
            Button(randomwin, text='PLAY GAME', command=play_button_randomize).pack()
        else:
            showerror('RANDOMIZE', 'Wrong Password! Access denied !!')

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Play in Frenzy mode", command=play_frenzy)
    filemenu.add_command(label="Play in Disabled Randomize mode", command=play_antirandomized)
    menubar.add_cascade(label="Extra", menu=filemenu)

    root.config(menu=menubar)

    difficulty = IntVar()
    difficulty.set(1)

    def diff_value():
        global diff_choice
        diff_choice = difficulty.get()

    def play_button():
        root.destroy()
        snake_game()

    Label(root, text='Snake Game', font='Algerian 30 bold').pack()
    Label(root, text='Welcome to the world of snakes..!\n', font='Courier 15').pack(anchor=NW)
    Label(root, text='OBJECTIVE : Score more and collect food to increase challenges\n\n'
                     'HOW TO PLAY : Press Left Control to see all options while in the game\n\n'
                     'CREATOR : Hardik Jain', font='timesnewroman 9').pack(anchor=NW)
    Label(root).pack(anchor=NW)
    Label(root, text='Set Difficulty :', font='Courier 10').pack(anchor=NW)

    Radiobutton(root, text="Easy", variable=difficulty, command=diff_value, value=1).pack(anchor=W)
    Radiobutton(root, text="Medium", variable=difficulty, command=diff_value, value=2).pack(anchor=W)
    Radiobutton(root, text="Hard", variable=difficulty, command=diff_value, value=3).pack(anchor=W)
    Radiobutton(root, text="Insane", variable=difficulty, command=diff_value, value=4).pack(anchor=W)

    Label(root).pack(anchor=NW)

    Button(root, text='PLAY GAME', command=play_button).pack()

    root.mainloop()


def snake_game():
    global diff_choice, difficulties, randomize, frenzymode, high_score
    delay = 0.1
    bgs = ['lightblue', 'forestgreen', 'cyan', 'magenta', 'orange', 'lightgrey', 'pink',
           'lightpink', 'limegreen', 'wheat', 'palegoldenrod', 'thistle', 'gold']

    score = 0
    high_score = 0
    level = 0

    print("\t\tDIFFICULTY :", difficulties[diff_choice - 1])
    print('Score', '\t', 'High Score', '\t', 'Level')

    wn = turtle.Screen()
    wn.title("Snake Game " + difficulties[diff_choice - 1])
    wn.bgcolor(random.choice(bgs))
    wn.setup(width=700, height=700)
    wn.tracer(1)

    # Snake head
    head = turtle.Turtle()
    head.speed(0)
    head.shape('square')
    head.color("black")
    head.penup()
    head.goto(0, 0)
    head.direction = "stop"
    head.hideturtle()

    # Snake Food
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    food.goto(0, 100)
    food.hideturtle()

    border = turtle.Turtle()
    border.penup()
    border.setposition(-295, -290)
    border.pendown()
    border.pensize(5)
    border.speed(1000)
    for side in range(4):
        border.forward(585)
        border.left(90)
    border.hideturtle()

    segments = []

    # Pen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("black")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 150)

    pen.write("Welcome To The World of Snakes ({})\n".format(difficulties[diff_choice - 1]),
              align="center", font=("Courier", 18))
    pen.write("Do not resize the window !!!", align="center", font=("Courier", 20))

    loading_bar = turtle.Turtle()
    loading_bar.penup()
    loading_bar.goto(-110, 0)
    loading_bar.pendown()
    loading_bar.hideturtle()
    loading_bar.width(5)
    total_forward = 0

    percent = turtle.Turtle()
    percent.penup()
    percent.hideturtle()
    percent.goto(0, 15)

    loading = turtle.Turtle()
    loading.penup()
    loading.hideturtle()
    loading.goto(0, 75)

    errors = ['The snake refused to be controlled !', 'Food was eaten by another snake!',
              'The snake is too tired to play!', 'Food was not grown properly!']

    for i in range(10):
        loading.write('Loading...', align='center', font='Courier 30')
        time.sleep(0.5)
        forward = random.randint(20, 50)
        loading_bar.forward(forward)
        total_forward += forward
        percentage = int((total_forward / 200) * 100)
        load_error = random.randint(1, 100)
        if load_error < 90:
            load_error = False
        else:
            load_error = True

        if percentage > 100:
            if load_error:
                percentage = 99
            else:
                percentage = 100
        percent.clear()
        percent.write('{} %'.format(percentage), align='center', font='timesnewroman 30')
        if total_forward >= 200:
            loading.clear()
            if not load_error:
                loading.write('Load Successful', align='center', font='Courier 30')
                break
            else:
                loading.write('Load Unsuccessful', align='center', font='Courier 30')
                loading.goto(0, -140)
                loading.write(random.choice(errors) + ' Please Retry!!', align='center', font='Courier 14')
                loading.goto(0, -175)
                loading.write('ERROR : SNKGMER' + str(random.randint(10000, 99999)), align='center', font='Courier 15')
                wn.exitonclick()

    time.sleep(2)
    pen.clear()
    loading.clear()
    loading_bar.clear()
    percent.clear()
    head.showturtle()
    food.showturtle()
    wn.tracer(0)
    pen.goto(0, 300)
    pen.write("Score: 0  High Score: 0  Level: 0", align="center", font=("algerian", 20, "normal"))

    # Functions

    def go_up():
        if head.direction != "down":
            head.direction = "up"

    def go_down():
        if head.direction != "up":
            head.direction = "down"

    def go_left():
        if head.direction != "right":
            head.direction = "left"

    def go_right():
        if head.direction != "left":
            head.direction = "right"

    def restart():
        ask_restart = askyesno("RESTART", "Do you want to restart the play ?")
        if ask_restart is True:
            head.direction = "stop"

    def move():
        if head.direction == "up":
            y = head.ycor()
            head.sety(y + 20)

        if head.direction == "down":
            y = head.ycor()
            head.sety(y - 20)

        if head.direction == "left":
            x = head.xcor()
            head.setx(x - 20)

        if head.direction == "right":
            x = head.xcor()
            head.setx(x + 20)

    def stop_randomize():
        global randomize, count_randomize
        count_randomize += 1
        if count_randomize % 2 != 0:
            randomize = False
            showinfo("RANDOMIZE", "Randomization Stopped!!!")
        else:
            randomize = True
            showinfo("RANDOMIZE", "Randomization Enabled!!!")

    def pause_game():
        showinfo('PAUSE', 'Gameplay Paused!\nExit this window to continue')

    def graph():
        global scores, high_scores
        if not scores:
            showerror('GRAPHS', 'Graph cannot be made from empty database!')
        else:
            graph_show = askyesno('GRAPHS', 'Do you want to show the graphs of game?')
            if graph_show:
                head.clear()
                food.clear()
                labels = []
                for i in range(len(scores)):
                    labels.append('Game {}'.format(i + 1))
                index = np.arange(len(labels))
                width = 0.35
                fig, ax = plt.subplots()
                rects1 = ax.bar(index - width / 2, scores, width,
                                color='SkyBlue', label='Score')
                rects2 = ax.bar(index + width / 2, high_scores, width,
                                color='IndianRed', label='High Score')

                ax.legend()

                def autolabel(rects, xpos='center'):
                    xpos = xpos.lower()
                    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
                    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}

                    for rect in rects:
                        height = rect.get_height()
                        ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                                '{}'.format(height), ha=ha[xpos], va='bottom')

                autolabel(rects1, "left")
                autolabel(rects2, "right")

                plt.xlabel('Game Number', fontsize=5)
                plt.ylabel('Score', fontsize=5)
                plt.xticks(index, labels, fontsize=5, rotation=30)
                plt.title('Game Data Analysis')
                plt.suptitle('GRAPH')
                head.hideturtle()
                food.hideturtle()
                pen.goto(0, 100)
                pen.write("Thank you for playing!", align='center', font='algerian 30 underline')
                plt.show()

    def save_data():
        resp_save = askyesno('SAVE', 'Do you wish to save the data and overwrite existing one ?')
        if resp_save:
            pickle.dump(scores, open('scores.dat', 'wb'))
            pickle.dump(high_scores, open('high_scores.dat', 'wb'))
            pickle.dump(levels, open('levels.dat', 'wb'))
            showinfo('SAVE', 'Scores saved')
        else:
            showwarning('SAVE', 'Save Cancelled!')

    def load_data():
        global scores, high_scores, levels, high_score, scores_df
        resp_load = askyesno('LOAD', 'Do you want to discard current game and load data ?')
        if resp_load:
            print('---------- NEW GAME ----------')
            scores = pickle.load(open('scores.dat', 'rb'))
            high_scores = pickle.load(open('high_scores.dat', 'rb'))
            levels = pickle.load(open('levels.dat', 'rb'))
            dict_scores = {'Score': scores, 'High Score': high_scores}
            scores_df = pandas.DataFrame(dict_scores)

            for i in range(len(scores)):
                if 1 < len(str(scores[i])) < 3:
                    print(scores[i], '\t\t', high_scores[i], '\t\t\t', levels[i])
                elif len(str(scores[i])) >= 3:
                    print(scores[i], '\t', high_scores[i], '\t\t\t', levels[i])
                elif len(str(scores[i])) == 1:
                    if len(str(high_scores[i])) > 1:
                        print(scores[i], '\t\t', high_scores[i], '\t\t\t', levels[i])
                    else:
                        print(scores[i], '\t\t', high_scores[i], '\t\t\t\t', levels[i])
            high_score = max(high_scores)
            if not scores:
                showinfo('LOAD', 'Empty Database!')
            else:
                showinfo('LOAD', 'Data Loaded!')
        else:
            showwarning('LOAD', 'Load Cancelled!')

    def frenzy():
        global frenzymode, count_frenzymode
        count_frenzymode += 1
        if count_frenzymode % 2 != 0:
            frenzymode = True
            showinfo('CHEATS', 'Frenzy Mode Enabled!')
        else:
            frenzymode = False
            showinfo('CHEATS', 'Frenzy Mode Disabled!')

    def credits():
        head.direction = 'stop'
        if head.xcor() in range(-300, 300) or head.ycor() in range(-20, 20):
            head.hideturtle()
            for segment in segments:
                segment.hideturtle()
        food.hideturtle()
        wn.tracer(1)

        credit = turtle.Turtle()
        credit.hideturtle()
        credit.penup()
        credit.goto(0, 0)
        credit.write('This Game was created by Hardik Jain', align='center', font='Courier 20')
        credit.goto(0, -75)
        credit.write('EXTRAS : https://www.youtube.com\n\t https://www.python.org', align='center', font='Courier 20')

        time.sleep(2)
        credit.clear()
        head.showturtle()
        food.showturtle()
        wn.tracer(0)

    def show_controls():
        showinfo('CONTROLS', 'Up - Move snake UP\nDown - Move snake DOWN\n'
                             'Left - Move snake LEFT\nRight - Move snake RIGHT\n'
                             'r - Restart Game\nq - Quit Game\ng - Show  graph\n'
                             's - Save data\nl - load data\nc - Credits\n'
                             'Space - Pause Game\nLeft Shift - E/D Randomization\n'
                             'Left Alt - E/D Frenzy Mode\nRight Control - Shift Food')

    def shift_food():
        food.clear()
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

    def quit():
        global scores_df
        quit_resp = askyesno("EXIT", "Do you really want to quit ?")
        if quit_resp:
            print('------------Result-So-Far--------------')
            print(scores_df)
            pen.goto(0, 100)
            pen.write('Click to exit', font='Courier 30 bold', align='center')
            wn.exitonclick()

    # Keyboard bindings
    wn.listen()
    wn.onkeypress(go_up, 'Up')
    wn.onkeypress(go_down, 'Down')
    wn.onkeypress(go_left, 'Left')
    wn.onkeypress(go_right, 'Right')
    wn.onkeypress(restart, 'r')
    wn.onkeypress(quit, 'q')
    wn.onkeypress(stop_randomize, 'Shift_L')
    wn.onkeypress(graph, 'g')
    wn.onkeypress(save_data, 's')
    wn.onkeypress(load_data, 'l')
    wn.onkeypress(frenzy, 'Alt_L')
    wn.onkeypress(credits, 'c')
    wn.onkeypress(pause_game, 'space')
    wn.onkeypress(show_controls, 'Control_L')
    wn.onkeypress(shift_food, 'Control_R')

    # Main Loop
    while True:
        global sno, total_score, scores, scores_df
        wn.update()

        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            if not frenzymode:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"
                if randomize:
                    wn.bgcolor(random.choice(bgs))

                for segment in segments:
                    segment.goto(1000, 1000)

                segments.clear()
                scores.append(score)
                high_scores.append(high_score)
                levels.append(level)
                temp_score = {'Score': scores, 'High Score': high_scores}
                scores_df = pandas.DataFrame(temp_score)

                if 1 < len(str(score)) < 3:
                    print(score, '\t\t', high_score, '\t\t\t', level)
                elif len(str(score)) >= 3:
                    print(score, '\t', high_score, '\t\t\t', level)
                elif len(str(score)) == 1:
                    if len(str(high_score)) > 1:
                        print(score, '\t\t', high_score, '\t\t\t', level)
                    else:
                        print(score, '\t\t', high_score, '\t\t\t\t', level)

                cursors.execute("Insert into scoretest values({}, now(), {}, now())".format(sno, score))

                score = 0
                level = 0

                delay = 0.1
            else:
                if head.xcor() < -290:
                    head.direction = 'right'
                if head.xcor() > 290:
                    head.direction = 'left'
                if head.ycor() > 290:
                    head.direction = 'down'
                if head.ycor() < -290:
                    head.direction = 'up'

            pen.clear()
            pen.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level),
                      align="center", font=("algerian", 20, "normal"))

        if head.distance(food) < 20:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x, y)
            if randomize:
                wn.bgcolor(random.choice(bgs))

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape('square')
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

            lvlscore = 0

            if diff_choice == 1:
                delay -= 0.001
                lvlscore = random.randint(1, 10)
            elif diff_choice == 2:
                delay -= 0.0015
                lvlscore = random.randint(3, 12)
            elif diff_choice == 3:
                delay -= 0.0025
                lvlscore = random.randint(5, 15)
            elif diff_choice == 4:
                delay -= 0.003
                lvlscore = random.randint(8, 17)

            if frenzymode:
                score += random.randint(500, 750)
            else:
                score += lvlscore
            level += 1

            if score > high_score:
                high_score = score

            for i in range(len(high_scores)):
                if high_scores[i] < high_score:
                    high_scores.pop(i)
                    high_scores.insert(i, high_score)

            pen.clear()
            pen.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level),
                      align="center",  font=("algerian", 20, "normal"))

        for index in range(len(segments) - 1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        for segment in segments:
            if segment.distance(head) < 20:
                if not frenzymode:
                    time.sleep(1)
                    head.goto(0, 0)
                    head.direction = "stop"
                    if randomize:
                        wn.bgcolor(random.choice(bgs))

                    for segment2 in segments:
                        segment2.goto(1000, 1000)

                    segments.clear()

                    scores.append(score)
                    high_scores.append(high_score)
                    levels.append(level)
                    temp_score = {'Score': scores, 'High Score': high_scores}
                    scores_df = pandas.DataFrame(temp_score)

                    if 1 < len(str(score)) < 3:
                        print(score, '\t\t', high_score, '\t\t\t', level)
                    elif len(str(score)) >= 3:
                        print(score, '\t', high_score, '\t\t\t', level)
                    elif len(str(score)) == 1:
                        if len(str(high_score)) > 1:
                            print(score, '\t\t', high_score, '\t\t\t', level)
                        else:
                            print(score, '\t\t', high_score, '\t\t\t\t', level)

                    cursors.execute("Insert into scoretest values({}, now(), {}, now())".format(sno, score))

                    score = 0
                    level = 0

                    delay = 0.1

                pen.clear()
                pen.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level),
                          align="center", font=("algerian", 20, "normal"))

        time.sleep(delay)
    wn.update()
    wn.mainloop()


options_snake()
