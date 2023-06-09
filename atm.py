from BankAccount import BankAccount, Interface
import os
import json
import time

# make the folder containing atm.py the working directory 
os.chdir(os.path.dirname(__file__))

def account_menu(user_sn = "", user_pin = "") -> None:
    'connecting to account menu and performing actions'
    acc_menu = Interface("Account menu")
    if user_sn == "":
        user_sn = acc_menu.present("Enter serial number:")
    if user_pin == "":
        user_pin = acc_menu.present("Enter PIN:")
    with open('accounts.json') as file:
            data = json.load(file)
    for account in data:
        if account['sn'] == user_sn and account['pin'] == user_pin:
            agent = BankAccount(account['name'], user_sn, account['balance'], user_pin)
            break
    else:
        agent = False
        acc_menu.output = ["Wrong credentials, no account found.", "press any key to continue..."]
        acc_menu.present()
    if agent:
        while True:
            # account is connected, user can perform actions or go back to main menu
            acc_menu.menu = f"Account menu - {agent.account_name}"
            acc_menu.options = [
            "(1) Withdraw", 
            "(2) Deposit", 
            "(3) Transfer", 
            "(4) Change PIN", 
            "(5) Show balance",
            "(any other key) Back to main menu"
            ]
            user = acc_menu.present("Choose option:")

            if user == "1":
                # withdraw amount from account
                acc_menu.menu = "Withdraw"
                try:
                    acc_menu.options = ["(Whole positive numbers only)"]
                    amount = int(acc_menu.present("Enter amount to withdraw:"))
                    agent.withdraw(amount)
                    acc_menu.output = ["Amount withdrawn."]
                    acc_menu.options = ["(1) Back to account menu", "(any other key) Back to main menu"]
                    if acc_menu.present("Choose option:") != "1":
                        break
                except ValueError:
                    acc_menu.present(err = "Amount contains non-digits or a fraction")
                except Exception as error:
                    acc_menu.present(err = error)
            
            elif user == "2":
                # deposit amount into account
                acc_menu.menu = "Deposit"
                try:
                    acc_menu.options = ["(Whole positive numbers only)"]
                    amount = int(acc_menu.present("Enter amount to deposit:"))
                    agent.deposit(amount)
                    acc_menu.output = ["Amount deposited."]
                    acc_menu.options = ["(1) Back to account menu", "(any other key) Back to main menu"]
                    if acc_menu.present("Choose option:") != "1":
                        break
                except ValueError:
                    acc_menu.present(err = "Amount contains non-digits or a fraction")
                except Exception as error:
                    acc_menu.present(err = error)
            
            elif user == "3":
                # transfer amount from account to other account
                acc_menu.menu = "Transfer"
                try:
                    other = acc_menu.present("Enter receiving account serial number:")
                    acc_menu.options = ["(Whole positive numbers only)"]
                    amount = int(acc_menu.present("Enter amount to transfer"))
                    agent.transfer(other, amount)
                    acc_menu.output = ["Amount transferred."]
                    acc_menu.options = ["(1) Back to account menu", "(any other key) Back to main menu"]
                    if acc_menu.present("Choose option:") != "1":
                        break
                except ValueError:
                    acc_menu.present(err = "Amount contains non-digits or a fraction")
                except Exception as error:
                    acc_menu.present(err = error)
            
            elif user == "4":
                # change account pin
                acc_menu.menu = "Change PIN"
                new_pin = acc_menu.present("Enter new PIN (4 digits):")
                while True: 
                    try:
                        agent.change_pin(new_pin)
                        break
                    except Exception as error:
                        acc_menu.output = [f"An error has occured:", str(error), "(PIN must have exactly 4 digits)"]
                        new_pin = acc_menu.present("Please enter valid PIN:")
                acc_menu.output = ["PIN changed."]
                acc_menu.options = ["(1) Back to account menu", "(any other key) Back to main menu"]
                if acc_menu.present("Choose option:") != "1":
                    break
            
            elif user == "5":
                # show account balance
                acc_menu.menu = "Show balance"
                acc_menu.output = ["Your balance is: ", agent.show_balance(), "Press any key to continue..."]
                acc_menu.present()
            
            else:
                # go to main menu
                return

while True:
    # start program, show main menu
    main_menu = Interface("Main menu")
    main_menu.options = ["(1) Create new account", "(2) Connect to existing account", "(any other key) Exit"]
    user = main_menu.present("Choose option:")
    if user == "1":
        # create new account by accepting name and pin
        main_menu.menu = "Create new account"
        user_name = main_menu.present("Enter new name:")
        agent = BankAccount(user_name)
        user_pin = main_menu.present("Enter new PIN (4 digits):")
        try:
            agent.assign_sn()
            agent.change_pin(user_pin)
        except Exception as error:
            main_menu.present(err = error)
            continue
        main_menu.menu = "Account created!"
        main_menu.output = [
        "New account information:",          
        f"Account name: {agent.account_name}",
        f"Account serial number: {agent.account_sn}",
        f"Acount PIN: {agent.pin}",
        f"Acount balance: {agent.balance}",
        ]
        main_menu.options = ["(1) Connect to new account", "(2) Back to main menu", "(any other key) Exit"]
        user = main_menu.present("Choose option:")
        if user == "1":
            # connecting to an account by passing the newly created account sn and pin
            account_menu(agent.account_sn, agent.pin) 
        elif user == "2":
            continue
        else:
            break
    
    elif user == "2": 
        # connecting to an account by accepting sn and pin
        account_menu()

    else:
        # go to exit screen
        break

# show exit screen for 3 seconds, then exit the program
goodbye_menu = Interface("Thank you and goodbye!")
goodbye_menu.present(inp = False)
time.sleep(3)