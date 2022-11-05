from tkinter import *
import argparse
import json
import sys

from dejavu import Dejavu
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer


# Connect to db
DEFAULT_CONFIG_FILE = "dejavu.cnf.SAMPLE"
def init(configpath):
    """
    Load config from a JSON file
    """
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print(f"Cannot open configuration: {str(err)}. Exiting")
        sys.exit(1)

    # create a Dejavu instance
    return Dejavu(config)

# Font
font = "Segoe UI"
# Colours
backgroundColor = "#357ec7"
labelColor = "#357ec7"
inputColor = "#808080"
fontColor = "#ffffff"

# GUI Dimension
loginPage = Tk()
screenWidth=850
screenHeight=800
loginPage.geometry(str(screenWidth) + "x" + str(screenHeight))
loginPage.configure(bg=backgroundColor)
canvas = Canvas(
    loginPage,
    bg=backgroundColor,
    height=screenHeight,
    width=screenWidth,
    bd=0,
    highlightthickness=0)
canvas.place(x=0, y=0)

loginPage.title("Login")

# TODO admin and user screen functions?
def mainScreen():
    # GUI Dimension
    mainPage = Tk()
    screenWidth=850
    screenHeight=800
    mainPage.geometry(str(screenWidth) + "x" + str(screenHeight))
    mainPage.configure(bg=backgroundColor)
    canvas = Canvas(
        mainPage,
        bg=backgroundColor,
        height=screenHeight,
        width=screenWidth,
        bd=0,
        highlightthickness=0)
    canvas.place(x=0, y=0)

    mainPage.title("Desktop")

    labelMainpage = Label(mainPage, text="Login successful!", bg=backgroundColor,fg=fontColor,font=("Arial",50))
    labelMainpage.place(x=150, y=350)
    mainPage.resizable(False, False)
    mainPage.mainloop()

# Autenticate user
def authentication():
    config_file = DEFAULT_CONFIG_FILE
    djv = init(config_file)
    global username
    authenticateUser = username	
    PinUsername = "b'"+ str(authenticateUser) +"'" 				# set format from database
    songs = None 							# get match from database
    source = 'mic' 							# input type for audio
    # opt_arg = 5
    # opt_arg = 10
    opt_arg = 6
    # opt_arg = 18
    # opt_arg = 13
    # opt_arg = 14 							# number of sec to recorded
    songs = djv.recognize(MicrophoneRecognizer, seconds=opt_arg)
    
    if str(songs[0]) != "[]":						# check for no database output
     checkuser =str(songs[0][0]['song_name'])				# username with most match
    
     inputMatchRatio = float(songs[0][0]['input_confidence'])		# get ratio match from input audio
    
     print("confident level max is 1: ",inputMatchRatio)
     print(checkuser)
    
     if checkuser == PinUsername and inputMatchRatio >= 0.1:		# username must be equal from user name from database, ratio match must be more then 0.1 for now
      recoverSuccess()
     else:
      errorMessage("Audio authentication fail ")
    else:
     errorMessage("Audio authentication fail ")
     
     

# ----------------------------------------------------------------------------------
# PROFILE ICON
# ----------------------------------------------------------------------------------
profileIcon = PhotoImage(file=f"./images/profile.png")
profileLabel = Label(loginPage, image=profileIcon, relief=FLAT, bg=backgroundColor)
profileLabel.place(x=305, y=50)

# ----------------------------------------------------------------------------------
# USERNAME
# ----------------------------------------------------------------------------------

# Username based on selected local user. Default: User
def getUser(selectedUser):
    if selectedUser == user:
        labelUsername.config(text="User")
    elif selectedUser == admin:
        labelUsername.config(text="Admin")
    else:
        labelUsername.config(text="User")

# labelUsername = Label(loginPage, text="User")

def inFocusLogin(args):
    inputUsername.delete(0, END)

inputUsername = Entry(
    bg=inputColor,
    fg=fontColor,
    bd=3,
    font=20)
inputUsername.place(
    x=260, y=350,
    width=350, height=42)
inputUsername.config(font=(font, 12))
inputUsername.insert(0, "Username")
inputUsername.bind("<FocusIn>", inFocusLogin)



# ----------------------------------------------------------------------------------
# PASSWORD / AUDIO KEY INPUT
# ----------------------------------------------------------------------------------

def inFocus(args):
    inputPassword.delete(0, END)
    inputPassword.config(show="•")

def outFocus(args):
    inputPassword.delete(0, END)
    inputPassword.insert(0, "Password")
    loginPage.focus()

inputPassword = Entry(
    bg=inputColor,
    fg=fontColor,
    bd=3,
    font=20)
inputPassword.place(
    x=260, y=400, 
    width=350, height=42)
inputPassword.config(font=(font, 12))
inputPassword.insert(0, "Password")

inputPassword.bind("<FocusIn>", inFocus)
inputPassword.bind("<FocusOut>", outFocus)

def showPassword():
    hidePwd = Button(image=hideIcon, command=hidePassword, relief=FLAT, bg=inputColor, activebackground=inputColor)
    hidePwd.place(x=550, y=410)
    inputPassword.config(show="")

def hidePassword():
    showPwd = Button(image=showIcon, command=showPassword, relief=FLAT, bg=inputColor, activebackground=inputColor)
    showPwd.place(x=550, y=410)
    inputPassword.config(show="•")

hideIcon = PhotoImage(file=f"./images/eye.png")
showIcon = PhotoImage(file=f"./images/eye-slash.png")
hideBtn = Button(image=hideIcon, command=showPassword, relief=FLAT, bg=inputColor, activebackground=inputColor)
hideBtn.place(x=550, y=410)

# Login logic here
maxLoginAttempts = 3
def login():
    global maxLoginAttempts
    global username
    username = inputUsername.get()
    getpassword = inputPassword.get()
    password = username + "Password"
    passwordError = "The password is incorrect. Try again."
    passwordLimitError = "Account locked. Please input audio key"
    if maxLoginAttempts > 1:
        if password == "":
            print("No password entered")
            maxLoginAttempts -=1
            errorMessage(passwordError,0)

        elif getpassword == password:
            print("Logged in as " + username)
            loginPage.destroy()
            mainScreen()

        else:
            print("Wrong user password")
            inputPassword.delete(0, END)
            maxLoginAttempts -=1
            labelErrorMsg.after(0, labelErrorMsg.destroy)
            errorMessage(passwordError)

    elif maxLoginAttempts == 1:
        if password == "":
            print("No password entered")
            maxLoginAttempts -=1
            errorMessage(passwordError)

        elif getpassword == password:
            print("Logged in as User")
            loginPage.destroy()
            mainScreen()

        else:
            print("No more attempts.  Password field disabled")
            inputPassword.delete(0, END)
            inputPassword.insert(0, "DISABLED")
            inputPassword.config(state="disabled", show="", justify="center", disabledbackground="grey")
            hideBtn.config(state="disabled")
            labelErrorMsg.after(0, labelErrorMsg.destroy)
            errorMessage(passwordLimitError)
            audioKeyInput()

# Enter key for login
enterIcon = PhotoImage(file=f"./images/arrow-right.png")
enterBtn = Button(image=enterIcon, command=login, relief=FLAT, bg=inputColor, activebackground=inputColor)
enterBtn.place(x=580, y=410)

# Error message label
labelErrorMsg = Label(loginPage, text="", bg=labelColor)
def errorMessage(msg):
    labelErrorMsg = Label(loginPage, text=msg, bg=labelColor)
    labelErrorMsg.config(font=(font, 9), fg=fontColor, justify='center')
    labelErrorMsg.place(
        x=330, y=445)

# After 3 failed attempts - Password Input becomes Audio Input
# TODO Bind to audio recognition
audioBtn = Button(text="Audio Key", command=authentication, relief=FLAT, bg=backgroundColor, activebackground=backgroundColor)
def audioKeyInput():
    audioBtn.config(font=(font, 12), fg=fontColor)
    audioBtn.place(
        x=380, y=480,
        width=100, height=50)


def recoverSuccess():
    global maxLoginAttempts
    maxLoginAttempts += 3
    recoverAccount = "Account recovered. Please enter your password."
    errorMessage(recoverAccount)
    inputPassword.config(font=(font, 12), state="normal", justify="left", show="")
    hideBtn.config(state="normal")
    inputPassword.delete(0, END)
    inputPassword.insert(0, "Password")

    inputPassword.bind("<FocusIn>", inFocus)
    inputPassword.bind("<FocusOut>", outFocus)
    labelErrorMsg.after(0, labelErrorMsg.destroy)
    audioBtn.place_forget()


# ----------------------------------------------------------------------------------
# USER CREDENTIALS
# ----------------------------------------------------------------------------------
# users = {
#    "user": "userPassword",
#    "admin": "adminPassword"}

# user = list(users.keys())[0]
# userPwd = list(users.values())[0]

# admin = list(users.keys())[1]
# adminPwd = list(users.values())[1]

# List of Local Users
# userIcon = PhotoImage(file=f"./images/user.png")
# userLabel = Label(loginPage, image=userIcon, relief=FLAT, bg=backgroundColor)
# userLabel.place(x=1, y=650)
# userBtn = Button(text=user, command=lambda username=user: getUser(username), relief=FLAT, bg=backgroundColor, activebackground=backgroundColor)
# userBtn.config(font=(font, 12), fg=fontColor)
# userBtn.place(
#    x=55, y=650,
#    width=50, height=50) 

# adminLabel = Label(loginPage, image=userIcon, relief=FLAT, bg=backgroundColor)
# adminLabel.place(x=1, y=705)
# adminBtn = Button(text=admin, command=lambda username=admin: getUser(username), relief=FLAT, bg=backgroundColor, activebackground=backgroundColor)
# adminBtn.config(font=(font, 12), fg=fontColor)
# adminBtn.place(
#    x=55, y=705,
#    width=50, height=50) 

# ----------------------------------------------------------------------------------
# RUN TK WINDOW
# ----------------------------------------------------------------------------------
# Resizable?
loginPage.resizable(False, False)
# Keep app window running
loginPage.mainloop()
