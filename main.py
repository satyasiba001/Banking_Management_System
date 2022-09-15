from tkinter import *
import os
from PIL import ImageTk, Image

# Main screen

master = Tk()
master.geometry("280x360")
master.resizable(0, 0)
master.title('Banking App')


# Functions
def finish():
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    password = temp_password.get()

    files = os.listdir()
    # print(files)

    if name == '' or age == '' or gender == '' or password == '':
        notif.config(fg='red', text='All field required*')
        return

    for name_check in files:
        if name == name_check:
            notif.config(fg='red', text='Account already exist')
        else:
            new_file = open(name, 'w')
            new_file.write(name + '\n')
            new_file.write(age + '\n')
            new_file.write(gender + '\n')
            new_file.write(password + '\n')
            new_file.write('0')
            new_file.close()
            notif.config(fg='green', text='Account is created')


def personal_func():
    # Reading from file
    file = open(login_name, 'r')
    user_details = file.read()
    user_details = user_details.split('\n')

    # Variable
    user_name = user_details[0]
    user_age = user_details[1]
    user_gender = user_details[2]
    user_balance = user_details[4]

    # New window and Labels to see personal details
    personal_detail_screen = Toplevel(master)
    personal_detail_screen.title("USER PROFILE")

    Label(personal_detail_screen, relief=RAISED, text='NAME ' + user_name).grid(row=0, sticky=N, pady=10)
    Label(personal_detail_screen, relief=RAISED, text='AGE ' + user_age).grid(row=1, sticky=N, pady=10)
    Label(personal_detail_screen, relief=RAISED, text='GENDER ' + user_gender).grid(row=2, sticky=N, pady=10)
    Label(personal_detail_screen, relief=RAISED, text='BALANCE :$' + user_balance).grid(row=3, sticky=N, pady=10)


def deposit_finish():
    if amount.get() == '':
        deposit_notif.config(text='Please Enter some Amount', fg='red')
        return

    if float(amount.get()) <= 0:
        deposit_notif.config(text='Please Enter some valid amount', fg='red')
        return
    file = open(login_name, 'r+')
    file_data = file.read()
    user_details = file_data.split('\n')
    current_balance = user_details[-1]
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_lebel.config(text='Your Account Balance: $' + str(updated_balance))
    deposit_notif.config(text='Balance Updated', fg='green')


def deposit_func():
    # Variables
    global amount
    global deposit_notif
    global current_balance_lebel
    amount = StringVar()
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[-1]

    # Deposit screen
    deposit_screen = Toplevel(master)
    deposit_screen.title('DEPOSIT WINDOW')
    # Labels
    Label(deposit_screen, text='Your Deposit').grid(row=0, sticky=N, pady=10)
    current_balance_lebel = Label(deposit_screen, relief=RAISED, fg='navy',
                                  text='Your Account Balance: $' + details_balance)
    current_balance_lebel.grid(pady=10, row=1, sticky=W)
    Label(deposit_screen, text='Amount to deposit', relief=RAISED).grid(row=2, sticky=W)
    deposit_notif = Label(deposit_screen)
    deposit_notif.grid(row=4, sticky=N, padx=5)

    # Entry
    Entry(deposit_screen, textvariable=amount, bg='SlateBlue1').grid(row=2, column=1, sticky=N)
    # Buttons
    Button(deposit_screen, text='Done', fg='green', command=deposit_finish).grid(row=3, column=2, sticky=E, pady=10)


def withdraw_func():
    global withdraw_amount
    global withdraw_notif
    global current_balance_lebel

    withdraw_amount = StringVar()
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[-1]

    # Withdraw screen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title('WITHDRAW WINDOW')
    # Labels
    # Label(deposit_screen, text='Your Deposit').grid(row=0, sticky=N, pady=10)
    current_balance_lebel = Label(withdraw_screen, relief=RAISED, fg='navy',
                                  text='Your Account Balance: $' + details_balance)
    current_balance_lebel.grid(pady=10, row=1, sticky=W)
    Label(withdraw_screen, text='Amount to withdraw', relief=RAISED).grid(row=2, sticky=W)
    withdraw_notif = Label(withdraw_screen)
    withdraw_notif.grid(row=4, sticky=N, padx=5)

    # Entry
    Entry(withdraw_screen, textvariable=withdraw_amount, bg='SlateBlue1').grid(row=2, column=1, sticky=N)
    # Buttons
    Button(withdraw_screen, text='Done', fg='green', command=withdraw_finish).grid(row=3, column=2, sticky=E, pady=10)


def withdraw_finish():
    global withdraw_notif

    if withdraw_amount.get() == '':
        withdraw_notif.config(text='Please Enter some Amount', fg='red')
        return

    if float(withdraw_amount.get()) <= 0:
        withdraw_notif.config(text='Please Enter some valid amount', fg='red')
        return
    file = open(login_name, 'r+')
    file_data = file.read()
    user_details = file_data.split('\n')
    current_balance = user_details[-1]

    if float(withdraw_amount.get()) > float(current_balance):
        withdraw_notif.config(text='Insufficient Balance in Your Account', fg='red')
        return
    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_lebel.config(text='Your Account Balance: $' + str(updated_balance))
    withdraw_notif.config(text='Balance Updated', fg='green')


def Login_done():
    all_files = os.listdir()
    global login_name
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()
    for name in all_files:
        if name == login_name:
            file = open(name, 'r')
            file_data = file.read()
            file_data = file_data.split('\n')
            password = file_data[-2]
            # Account Dashboard
            if password == login_password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Users profile')
                # Labels
                Label(account_dashboard, text='USER DASHBOARD', fg='maroon').grid(row=0, sticky=N, pady=10)
                Label(account_dashboard, text='WELCOME ' + name).grid(row=1, sticky=N, pady=10)
                # Buttons
                Button(account_dashboard, text='PERSONAL DETAILS', fg='navy', width=15, command=personal_func,
                       font=('Calibri', 12)).grid(row=2,
                                                  sticky=N)
                Button(account_dashboard, text='DEPOSIT', fg='navy', width=15, command=deposit_func,
                       font=('Calibri', 12)).grid(row=3,
                                                  sticky=N)
                Button(account_dashboard, text='WITHDRAW', fg='midnight blue', width=15, command=withdraw_func,
                       font=('Calibri', 12)).grid(row=4,
                                                  sticky=N)

                return
            else:
                login_notif.config(text='Wrong Login Credential', fg='red')
                return
    login_notif.config(text='No account found !!', fg='red')


def register():
    # Variable Declaration
    global temp_name
    global temp_age
    global temp_gender
    global temp_password
    global notif

    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_password = StringVar()

    # Making Register Screen
    screen = Toplevel(master)
    screen.title("REGISTER SCREEN")

    Label(screen, anchor=CENTER, bg='red', bd=1, relief=RAISED, text='Fill your details here', font='Calibri,12').grid(
        row=0, sticky=N, pady=10)
    Label(screen, anchor=CENTER, bd=1, relief=RAISED, text='Name', font=('Calibri', 12)).grid(row=1, sticky=W, pady=5)
    Label(screen, anchor=CENTER, bd=1, relief=RAISED, text='Age', font='Dotum,12').grid(row=2, sticky=W, pady=5)
    Label(screen, anchor=CENTER, bd=1, relief=RAISED, text='Gender', font='Times,12').grid(row=3, sticky=W, pady=5)
    Label(screen, anchor=CENTER, bd=1, relief=RAISED, text='Password', font='Calibri,12').grid(row=4, sticky=W, pady=5)
    notif = Label(screen, relief=RAISED, font='Calibri,12')
    notif.grid(row=6, sticky=N, pady=10)

    # Entries
    Entry(screen, textvariable=temp_name).grid(row=1, column=1)
    Entry(screen, textvariable=temp_age).grid(row=2, column=1)
    Entry(screen, textvariable=temp_gender).grid(row=3, column=1)
    Entry(screen, textvariable=temp_password, show='*').grid(row=4, column=1)

    # Buttons
    Button(screen, text='Finish', font=('Calibri,12'), command=finish).grid(sticky=W, column=2, row=5)


def login():
    # Varibale Declaration
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen

    temp_login_password = StringVar()
    temp_login_name = StringVar()

    # Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login Window')

    # Labels
    Label(login_screen, text='You Can Login Here', fg='DodgerBlue4', font=('Calibri', 12)).grid(row=0, sticky=N)
    Label(login_screen, text='NAME', relief=RAISED, font=('Calibri', 12)).grid(row=1, sticky=W, pady=7)
    Label(login_screen, text='PASSWORD', relief=RAISED, font=('Calibri', 12)).grid(row=2, sticky=W, pady=7)
    login_notif = Label(login_screen, relief=RAISED, font=('Calibri', 12))
    login_notif.grid(row=3, sticky=N, pady=10)

    # Entries
    Entry(login_screen, textvariable=temp_login_name, width=20).grid(row=1, column=1)
    Entry(login_screen, textvariable=temp_login_password, show='*', width=20).grid(row=2, column=1)

    # Buttons
    Button(login_screen, text='Sign in', command=Login_done, width=10, activebackground='green').grid(row=3, column=3)


# Image import
img = Image.open('bank-icon-19.png')
img = img.resize((150, 150))
img = ImageTk.PhotoImage(img)

# Labels

Label(master, text='BANKING SYSTEM', font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
Label(master, text='The most secure bank for you', font=('Calibri', 14)).grid(row=1, sticky=N)
Label(master, image=img).grid(row=2, sticky=N, pady=15)
# Buttons
Button(master, text='Register', font=('Calibri', 14), activebackground='green', width=17, command=register).grid(
    sticky=N)
Button(master, text='Login', font=('Calibri', 14), activebackground='green', width=17, command=login).grid(pady=15,
                                                                                                           sticky=N)

master.mainloop()
