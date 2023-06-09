import random
import json
import os

class BankAccount:
    'base class for accounts. all methods that save to accounts.json use save_info().'
    def __init__(self, account_name: str, account_sn: str= "", balance: int = 0, pin: str =""):
        self.account_name = account_name
        self.account_sn = account_sn
        self.balance = balance
        self.pin = pin
              
    def deposit(self, amount: int):
        'add amount to self.balance, raise exception if amount is non-positive. save to accounts.json.'
        if amount<=0:
            raise Exception("Non-positive amount")
        else:
            self.balance += amount
            self.save_info()

    def withdraw(self, amount: int):
        '''subtract amount from self.balance, raise exception if not enough in self.balance or amount is non-positive. 
        save to accounts.json.'''
        if self.balance < amount:
            raise Exception("Not enough in balance")
        if amount<=0:
            raise Exception("Non-positive amount")
        else:
            self.balance -= amount
            self.save_info()

    def transfer(self, account_sn: str, amount: int):
        '''search accounts.json for account with 'sn': account_sn. 
        if found, subtract amount from self.balance, and add amount to that account 'balance' value.
        raise exception if amount is non-positive, if there is not enough in self.balance, 
        if account_sn is self.account_sn of if account_sn wasn't found.
        save to accounts.json.'''
        if account_sn == self.account_sn:
            raise Exception("Cannot transfer to self")    
        if self.balance < amount:
            raise Exception("Not enough in balance")
        if amount<=0:
            raise Exception("Non-positive amount")
        else:
            with open('accounts.json') as file:
                data = json.load(file)
            for account in data:
                if account['sn'] == account_sn:
                    account['balance'] += amount
                    self.balance -= amount
                    with open('accounts.json', 'w') as file:
                        json.dump(data, file, indent=4)
                    self.save_info()
                    return
            raise Exception("Account serial number not found, transfer canceled")
        
    def show_balance(self):
        'return self.balance as str'
        return str(self.balance)

    def change_pin(self, new_pin: str):
        'change pin to new_pin, raises exception if new_pin contains non-digits or isnt of length 4. save to accounts.json.'
        if len(new_pin) !=4 or not new_pin.isdigit():
            raise Exception("Invalid PIN")
        else:
            self.pin = new_pin
            self.save_info()
      
    def save_info(self):
        '''search in accounts.json for account with 'sn': account_sn.
        if found, update information in accounts.json.
        if not found, create a new account and save information to accounts.json.'''
        with open('accounts.json') as file:
            data = json.load(file)
        for account in data:
            if account['sn'] == self.account_sn:
                account['balance'] = self.balance
                account['pin'] = self.pin
                with open('accounts.json', 'w') as file:
                    json.dump(data, file, indent=4)
                return 
        new_account = {'name': self.account_name, 'sn': self.account_sn, 'balance': self.balance, 'pin': self.pin}
        data.append(new_account)
        with open('accounts.json', 'w') as file:
            json.dump(data, file, indent=4)

    def assign_sn(self):
        '''generate a 7 digit string, and check no existing account in accounts.json has it in 'sn'.
        if so, assign it to self.account_sn.
        this method does not save to accounts.json.'''
        with open('accounts.json') as file:
            data = json.load(file)
        sn_list = [account['sn'] for account in data]
        sn = str(random.randint(1000000,9999999))
        while sn in sn_list:
            sn = str(random.randint(1000000,9999999))
        self.account_sn = sn

class Interface:
    '''base class of graphical interface. each line is up to 58 characters long:

    one line for menu.

    one line for instructions.

    up to 6 lines for options, each item is a line.

    up to 7 lines for output, each items is a line.'''

    def __init__(self, menu: str, instructions = "", options: list = [], output: list= []):
        self.menu = menu
        self.instructions = instructions
        self.options = options
        self.output = output

    def present(self, instructions = "", inp = True, err: Exception | str = False):
        '''clear screen and draw the graphical interface with current properties.

        every item in self.options and self.output is a new line.

        afterward, clear all properties except self.menu.

        return input() by default, can be set to False.

        can be given instructions to present, otherwise uses self.instructions.

        can be given Exception object or string in err argument to return a generic error screen.'''

        os.system('cls')
        if err:
            self.output = [f"An error has occurred:", str(err), "Press any key to continue..."]
        menu = self.menu
        if not instructions:
            instructions = self.instructions
        options = iter(self.options)
        output = iter(self.output)
        
        print(f'''
╔══════════════════════════════════════════════════════════╗
║{menu.ljust(58)                                          }║
║──────────────────────────────────────────────────────────║
║{instructions.ljust(58)                                  }║
║{next(options,"").ljust(58)                              }║
║{next(options,"").ljust(58)                              }║
║{next(options,"").ljust(58)                              }║
║{next(options,"").ljust(58)                              }║
║{next(options,"").ljust(58)                              }║
║{next(options,"").ljust(58)                              }║
║──────────────────────────────────────────────────────────║
║{next(output, "").ljust(58)                              }║
║{next(output, "").ljust(58)                              }║
║{next(output, "").ljust(58)                              }║
║{next(output, "").ljust(58)                              }║
║{next(output, "").ljust(58)                              }║
║{next(output, "").ljust(58)                              }║
║{next(output, "").ljust(58)                              }║
╚══════════════════════════════════════════════════════════╝  
''')
        self.instructions = ""
        self.options = []
        self.output = []
        if inp:
            return input("Input: ")