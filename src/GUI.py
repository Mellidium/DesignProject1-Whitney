from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
import pandas as pd
import TrainedModelTesting
from threading import Thread
from threading import Timer
from multiprocessing import Queue
import queue
import random


def hide_all():
    global gameRunning
    gameRunning = False
    global scoreValue
    scoreValue = 0
    scoreValueLabel.configure(text=("Score: %s" % scoreValue))

    btnGP.pack_forget()
    btnB.pack_forget()
    btnL.pack_forget()
    btnTT.pack_forget()
    btnCL.pack_forget()
    photoLabel.pack_forget()
    usernameEntry.pack_forget()
    passwordEntry.pack_forget()
    userText.pack_forget()
    passText.pack_forget()
    btnCancel.pack_forget()
    btnConfirmLogin.pack_forget()
    btnConfirmCreate.pack_forget()
    btnLogout.pack_forget()
    #standard_video.pack_forget()
    #hand_video.pack_forget()
    #resultLabel.pack_forget()
    btnStartGame.pack_forget()
    btnReset.pack_forget()
    gameInfo.pack_forget()
    gameTimerLabel.pack_forget()
    currentLetterLabel.pack_forget()
    scoreValueLabel.pack_forget()
    highscore1Label.pack_forget()
    highscore2Label.pack_forget()
    highscore3Label.pack_forget()
    highscore4Label.pack_forget()
    highscore5Label.pack_forget()
    btnHighscoreB.pack_forget()
    btnHS.pack_forget()


def guided_practice():
    hide_all()
    btnB.pack(side=BOTTOM)
    btnReset.pack(side=BOTTOM)
    photoLabel.pack()
    standard_video.pack()
    hand_video.pack()
    resultLabel.pack()


def unassisted_practice():
    hide_all()
    btnB.pack()
    standard_video.pack()
    hand_video.pack()
    resultLabel.pack()
    print("Hello2")


def time_trial():
    hide_all()
    btnB.pack()
    gameInfo.pack(anchor="center")
    btnStartGame.pack(anchor="center")
    print("Hello3")


def login():
    hide_all()
    userText.pack()
    usernameEntry.pack()
    passText.pack()
    passwordEntry.pack()
    btnConfirmLogin.pack()
    btnCancel.pack()
    print("Login")


def logout():
    if online == True:
        if usernameString.get() == "User: Not Logged In":
            messagebox.showinfo("Error!", "No user is currently logged in")
        else:
            messagebox.showinfo("Success!", "%s has been succesfully logged out" % usernameString.get())
            usernameString.set("User: Not Logged In")


def create_account():
    print("Creaet login")
    hide_all()
    userText.pack()
    usernameEntry.pack()
    passText.pack()
    passwordEntry.pack()
    btnConfirmCreate.pack()
    btnCancel.pack()
    print(usernameEntry.get())
    print(passwordEntry.get())


def clear():
    hide_all()
    Tk.update(window)
    btnGP.pack()
    btnTT.pack()
    btnCL.pack()
    btnL.pack()
    btnLogout.pack()
    btnHS.pack()
    btnReset.pack()
    standard_video.pack()
    hand_video.pack()
    resultLabel.pack()
    usernameEntry.delete(0, 'end')
    passwordEntry.delete(0, 'end')


def send_login():
    query = "SELECT * FROM logins WHERE username='%s'" % (usernameEntry.get())

    if online == True:
        if usernameEntry.get() == "" or passwordEntry.get() == "":
            messagebox.showerror("Error!", "One or more fields is unfilled.")
        else:
            result = pd.read_sql(query, con=conn)
            if result.empty != True:
                if result.get_value(0, col="password") == passwordEntry.get():
                    usernameString.set("User: %s" % usernameEntry.get())
                    messagebox.showinfo("Success!", "%s has been logged in!" % usernameString.get())
                    clear()
                else:
                    messagebox.showerror("Error!", "Password is incorrect.")
            else:
                messagebox.showerror("Error!", "No such user exists.")
    else:
        messagebox.showinfo("Error!", "Can't connect to the server.")

    #network, check if user is taken or if user exists


def send_create():
    queryInsert = "INSERT INTO logins (username, password) VALUES ('%s', '%s')" % (usernameEntry.get(), passwordEntry.get())
    queryAnalyze = "SELECT * FROM logins WHERE username='%s'" % (usernameEntry.get())
    passTest = passwordEntry.get()

    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error!", "One or more fields is unfilled.")
    else:
        result = pd.read_sql(queryAnalyze, con=conn)
        if result.empty == True:
            if len(passTest) < 6:
                messagebox.showerror("Error!", "Password must contain at least 6 characters.")
            else:
                cursor = conn.cursor()
                cursor.execute(queryInsert)
                conn.commit()
                cursor.close()
                messagebox.showinfo("Success!", "Account created. Login to your new account from the home page!")
                clear()
        else:
            messagebox.showerror("Error!", "User with that username already exists.")


def refresh_image():
    try:
        frame2 = PhotoImage(file="hand_images/TestFiles/GUI_display.png")
        frame_hand2 = PhotoImage(file="hand_images/TestFiles/bitwise_hand.png")
        standard_video.configure(image=frame2)
        standard_video.image = frame2
        hand_video.configure(image=frame_hand2)
        hand_video.image = frame_hand2
        Tk.update(window)
    except:
        Tk.update(window)
    window.after(1, refresh_image)


def get_data():
    try:
        letter = results.get(False)
        resultLabel.configure(text=("%s" % letter[0]).capitalize())
        global currentVideoLetter
        currentVideoLetter = letter[0]
    except queue.Empty:
        pass
    window.after(500, get_data)


def start_game():
    hide_all()
    global gameTimer
    global timerValue
    timerValue = 60
    global gameRunning
    gameRunning = True
    global gameStarted
    gameStarted = False
    standard_video.pack()
    hand_video.pack()
    resultLabel.pack()
    gameTimerLabel.pack()
    scoreValueLabel.pack(side=BOTTOM)
    currentLetterLabel.pack()
    btnB.pack()
    btnReset.pack()
    try:
        gameTimer.start()
    except RuntimeError:
        gameTimer.cancel()
        gameTimer = Timer(1.0, timer_deprecate)
        gameTimer.start()
    game_logic()


def game_logic():
    global scoreValue
    global gameStarted
    global gameRunning
    global currentGameLetter
    if gameStarted == False:
        currentGameLetter = random.choice(alphabet)
        currentLetterLabel.configure(text="Letter: %s" % currentGameLetter.capitalize())
        gameStarted = True
    if gameRunning == True:
        print("%s" % currentGameLetter)
        print("%s" % currentVideoLetter)
        if currentVideoLetter == currentGameLetter:
            scoreValue = scoreValue + 100
            scoreValueLabel.configure(text=("Score: %s" % scoreValue))
            currentGameLetter = random.choice(alphabet)
            currentLetterLabel.configure(text="Letter: %s" % currentGameLetter.capitalize())
    window.after(500, game_logic)


def timer_deprecate():
    global timerValue
    global gameRunning
    if gameRunning == True:
        timerValue = timerValue - 1
        gameTimerLabel.configure(text=("Time Remaining (seconds): %s" % timerValue))
        if timerValue == 0:
            gameRunning = False
            gameTimer.cancel()
            game_complete()
        else:
            Timer(1.0, timer_deprecate).start()


def game_complete():
    global scoreValue
    messagebox.showinfo("Success!", "Game completed with a score of %s" % scoreValue)
    if online == True:
        if usernameString.get() == "User: Not Logged In":
            messagebox.showinfo("Error!", "Login to see and store highscores.")
            clear()
        else:
            print(usernameString.get()[6:100])
            queryAnalyze = "SELECT * FROM highscores WHERE username='%s'" % (usernameString.get()[6:100])
            result = pd.read_sql(queryAnalyze, con=conn)
            if result.empty == True:
                queryUpdate = "INSERT INTO highscores (username, highscore1, highscore2, highscore3, highscore4, highscore5)" \
                              " VALUES ('%s', '%s', '0', '0', '0', '0')" % (usernameString.get()[6:100], scoreValue)
                print(queryUpdate)
                cursor = conn.cursor()
                cursor.execute(queryUpdate)
                conn.commit()
                cursor.close()
            else:
                for i in range(1, 6):
                    print(result.get_value(0, col="highscore%s" % i))
                    print(scoreValue)
                    if result.get_value(0, col="highscore%s" % i) < scoreValue:
                        print(result)
                        if i == 1:
                            queryUpdate = "UPDATE highscores SET highscore1='%s', highscore2='%s', highscore3='%s', highscore4='%s', highscore5='%s'" \
                                          " WHERE username='%s'" % (scoreValue,result.get_value(0, col="highscore1"),result.get_value(0, col="highscore2"),
                                                                    result.get_value(0, col="highscore3"),result.get_value(0, col="highscore4"),usernameString.get()[6:100])

                        if i == 2:
                            queryUpdate = "UPDATE highscores SET highscore2='%s', highscore3='%s', highscore4='%s', highscore5='%s'" \
                                          " WHERE username='%s'" % (scoreValue,result.get_value(0, col="highscore2"),result.get_value(0, col="highscore3"),
                                                                    result.get_value(0, col="highscore4"),usernameString.get()[6:100])
                        if i == 3:
                            queryUpdate = "UPDATE highscores SET highscore3='%s', highscore4='%s', highscore5='%s'" \
                                          " WHERE username='%s'" % (scoreValue,result.get_value(0, col="highscore3"),result.get_value(0, col="highscore3"),
                                                                    usernameString.get()[6:100])

                        if i == 4:
                            queryUpdate = "UPDATE highscores SET highscore4='%s', highscore5='%s'" \
                                          " WHERE username='%s'" % (scoreValue,result.get_value(0, col="highscore4"),usernameString.get()[6:100])

                        if i == 5:
                            queryUpdate = "UPDATE highscores SET highscore5='%s' WHERE username='%s'" % (scoreValue,usernameString.get()[6:100])

                        print(queryUpdate)
                        cursor = conn.cursor()
                        cursor.execute(queryUpdate)
                        conn.commit()
                        cursor.close()
                        break;
            show_highscores()

    #queryInsert = "INSERT INTO logins (username, password) VALUES ('%s', '%s')" % (
    #usernameEntry.get(), passwordEntry.get())
    #queryAnalyze = "SELECT * FROM highscores WHERE username='%s'" % (usernameString.get())


def show_highscores():
    if online == True:
        if usernameString.get() == "User: Not Logged In":
            messagebox.showinfo("Error!", "Login to see high scores.")
        else:
            hide_all()
            queryAnalyze = "SELECT * FROM highscores WHERE username='%s'" % (usernameString.get()[6:100])
            result = pd.read_sql(queryAnalyze, con=conn)
            if result.empty != True:
                highscore1Label.configure(text="Highscore 1: %s" % result.get_value(0, col="highscore1"))
                highscore2Label.configure(text="Highscore 2: %s" % result.get_value(0, col="highscore2"))
                highscore3Label.configure(text="Highscore 3: %s" % result.get_value(0, col="highscore3"))
                highscore4Label.configure(text="Highscore 4: %s" % result.get_value(0, col="highscore4"))
                highscore5Label.configure(text="Highscore 5: %s" % result.get_value(0, col="highscore5"))
                highscore1Label.pack()
                highscore2Label.pack()
                highscore3Label.pack()
                highscore4Label.pack()
                highscore5Label.pack()
                btnHighscoreB.pack()
            else:
                messagebox.showinfo("Error!", "No highscores yet for this user.")
                clear()


def reset_frame():
    TrainedModelTesting.reset = True


#connect to sql server first
try:
    host="asltranslationdb.cd7r6ezvw3xo.us-east-2.rds.amazonaws.com"
    port=3306
    dbname="userinfo"
    user="admin"
    password="tFFQCUO12321"
    conn = pymysql.connect(host, user=user,port=port, passwd=password, db=dbname)
    online = True
except:
    online = False

window = Tk()
window.state('zoomed')

options = Frame(window)
options.pack(side=RIGHT)
cameras = Frame(window)
cameras.pack(side=LEFT)
information = Frame(window)
information.pack(side=BOTTOM)

#create Queue to get data from threads
results = Queue()

#run the hand gesture recognition
c = Thread(target=TrainedModelTesting.GUIcall, args=(results,))
c.start()
frame = PhotoImage(file="loading.png")
frame_hand = PhotoImage(file="loading.png")
try:
    frame = PhotoImage(file="hand_images/TestFiles/GUI_display.png")
    frame_hand = PhotoImage(file="hand_images/TestFiles/bitwise_hand.png")
except:
    Tk.update(window)
standard_video = Label(cameras, image=frame)
hand_video = Label(cameras, image=frame_hand)
resultLabel = Label(cameras, font=("Calibri", 64), text="Waiting...")


#variables
usernameString = StringVar()
usernameString.set("User: Not Logged In")

#images
chart = PhotoImage(file="asl_chart.png")
photoLabel = Label(options, image=chart)

#logins
userText = Label(text="Username")
passText = Label(text="Password")
loggedInText = Label(window, font=("Calibri:, 24"), textvariable=usernameString)
usernameEntry = Entry(window, width=20, bg="white")
passwordEntry = Entry(window, width=20, bg="white", textvariable=password, show="*")
btnCancel = ttk.Button(window, text='Cancel', command=clear, width=15)
btnConfirmLogin = ttk.Button(window, text='Login', command=send_login, width=15)
btnConfirmCreate = ttk.Button(window, text='Create Account', command=send_create, width=15)


#buttons
btnB = ttk.Button(options, text='Back', command=clear, width=20)
btnGP = ttk.Button(options, text='Guided Practice', command=guided_practice, width = 20)
btnTT = ttk.Button(options, text='Time Trial', command=time_trial, width=20)
btnL = ttk.Button(options, text='Login', command=login, width=20)
btnCL = ttk.Button(options, text='Create Account', command=create_account, width=20)
btnLogout = ttk.Button(options, text='Logout', command=logout, width=20)
btnHS = ttk.Button(options, text='High Scores', command=show_highscores, width=20)
btnStartGame = ttk.Button(window, text='Start Game!', command=start_game, width=20)
btnReset = ttk.Button(options, text='Reset Frame', command=reset_frame, width=20)

#Game text/variables
gameInfo = Label(wraplength=400, anchor=CENTER, text="Welcome to the ASL sign language time trial! As letters appear on the screen, sign the correct letter in the rectangular image of your video feed! Don't worry if you don't get it right, there's no negative to signing an incorrect letter! See how many you can get correct before time runs out!")
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
scoreValue = 0
scoreValueLabel = Label(window, font=("Calibiri", 64), text="Score: %s" % scoreValue)
timerValue = 60
gameTimer = Timer(1.0, timer_deprecate)
currentLetterLabel = Label(window, font=("Calibri", 64), text="Waiting...")
gameTimerLabel = Label(window, font=("Calibri", 32), text="Time Remaining (seconds): %s" % timerValue)

#Highscore Labels
highscore1Label = Label(window, font=("Calibri", 32), text="Highscore 1: %s" % 0)
highscore2Label = Label(window, font=("Calibri", 32), text="Highscore 2: %s" % 0)
highscore3Label = Label(window, font=("Calibri", 32), text="Highscore 3: %s" % 0)
highscore4Label = Label(window, font=("Calibri", 32), text="Highscore 4: %s" % 0)
highscore5Label = Label(window, font=("Calibri", 32), text="Highscore 5: %s" % 0)
btnHighscoreB = ttk.Button(window, text='Back to Home', command=clear, width=20)




btnGP.pack()
btnTT.pack()
btnCL.pack()
btnL.pack()
btnLogout.pack()
btnHS.pack()
btnReset.pack()
loggedInText.pack(side=TOP, anchor="w")
standard_video.pack()
hand_video.pack()
resultLabel.pack()

get_data()
refresh_image()
window.mainloop()