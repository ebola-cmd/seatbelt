import os
import datetime
import json
import requests

GREEN = "\033[32m"
BLUE = "\033[36m"
RESET = "\033[0m"
YELLOW = "\033[33m"
RED = '\033[91m'

def menu():
    os.system('cls')
    habits = load_habits()
    ascii_art = """
    ███████╗███████╗ █████╗ ████████╗██████╗ ███████╗██╗  ████████╗
    ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██╔════╝██║  ╚══██╔══╝
    ███████╗█████╗  ███████║   ██║   ██████╔╝█████╗  ██║     ██║   
    ╚════██║██╔══╝  ██╔══██║   ██║   ██╔══██╗██╔══╝  ██║     ██║   
    ███████║███████╗██║  ██║   ██║   ██████╔╝███████╗███████╗██║   
    ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚══════╝╚═╝
    """

    print(ascii_art)
    print('')
    print(f"{GREEN}[>] {RESET}{BLUE}Created By{RESET}   : ebola-cmd")
    print(f"{GREEN}[>] {RESET}{BLUE}Version{RESET}      : 1.0")
    print('')
    print(f"{YELLOW}[!] -help for commands :{RESET}")
    print('')
    choice = input(f"{GREEN}[>]{RESET}")
    if choice == "-help":
        help()

    if choice == "-r":
        add_reminder()

    if choice == "-rs":
        show_reminders()

    if choice == "-ah":
        add_habit(habits)

    if choice == "-mh":
        mark_habit_done(habits)

    if choice == "-vh":
        view_progress(habits)

    if choice == "-gp":
        get_gold_price_in_aed()
   
    if choice == "-exit":
        print('bye...')

        


def help():
    print("\n=== Help Menu ===")
    print("-r                : Set a reminder.")
    print("-rs               : Show all reminders saved.")
    print("-ah               : Add a new habit.")
    print("-mh               : Mark a habit as done for today.")
    print("-vh               : View progress of your habits.")
    print("-gp               : Get the current 24k gold price in AED.")
    print("-help             : Display this help menu with available commands.")
    print("-exit             : Exit the program.")
    print("===================\n")
    input('Press Enter to return to the menu...')
    menu()


def add_reminder():
    reminder_text = input(f"{YELLOW}[!] enter what you want to get reminded : {RESET}")
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    reminder_entry = f"{timestamp} - {reminder_text}\n"

    try:

        # Save the reminder to a file
        with open("reminders.txt", "a") as file:
            file.write(reminder_entry)

        input("Reminder saved!")
        menu()
    except Exception as e:
        print(f"Error writing to file: {e}")


def show_reminders():
    try:
        with open("reminders.txt", "r") as file:
            reminders = file.readlines()

            if reminders:
                print('your reminders')
                for reminder in reminders:
                    input(reminder.strip())

                menu() 

            else:
                input(f"{YELLOW}[!] You have no reminders :{RESET}")
                menu()

    except FileNotFoundError:
        print(f"{YELLOW}[!] You have no reminders :{RESET}")

def load_habits():
    try:
        with open("habits.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return{}

def save_habits(habits):
    with open("habits.json", "w") as file:
        json.dump(habits, file, indent=4)

def add_habit(habits):
    habit_name = input(f"{YELLOW}[!] Enter the name of the new habit: {RESET}")
    if habit_name not in habits:
        habits[habit_name] = []
        input(f"Habit '{habit_name}' added!")
        save_habits(habits)  # Save after adding
        menu()

    else:
        input("Habit already exists.")
        menu()

def mark_habit_done(habits):            
    habit_name = input(f"{YELLOW}[!] Enter the habbit you completed today: {RESET}")
    if habit_name in habits:
        today = datetime.date.today().isoformat()
        if today not in habits[habit_name]:
            habits[habit_name].append(today)
            input(f"Habit '{habit_name}' marked as done for today!")
            save_habits(habits)
            menu()
        else:
            input(f"Habit '{habit_name}' was already marked as done today.")
            menu()
    else:
        input("Habit not found.")
        menu()

def view_progress(habits):
    habits = load_habits()
    print("\n=== Habit Progress ===")
    if habits:
        for habit, dates in habits.items():
            print(f"{habit}: {len(dates)} days completed")
            
    else:
        input("no habits to show progress for\n")
        menu()

    print("======================\n")
    input("Press Enter to return to the menu.")
    menu()

def get_gold_price_in_aed():
    # Replace with your GoldAPI key
    api_key = 'goldapi-2wen00ksm3a44sxs-io'

    # Make the API request to GoldAPI
    url = f'https://www.goldapi.io/api/XAU/USD'
    headers = {'x-access-token': api_key}

    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            gold_price_usd_per_gram = data.get('price')  # USD price of 1 gram of gold

            if gold_price_usd_per_gram:
                # Convert USD to AED (simple example, you can use any reliable source for conversion)
                usd_to_aed_rate = 3.67  # Example: USD to AED rate, replace with actual or dynamic rate
                gold_price_aed = gold_price_usd_per_gram * usd_to_aed_rate / 31.1035

                print(f"The price of 24-carat gold in AED is approximately {gold_price_aed:.2f} per gram.")
                input('enter to continue...')
                menu()
            else:
                print("Error: Gold price data not found.")
                input('enter to continue...')
                menu()
        else:
            print("Error fetching gold price data. Please try again later.")        
            input('enter to continue...')
            menu()
    
    except requests.exceptions.RequestException as e:
        print(f"Error in the API request: {e}")
        input('enter to continue...')
        menu()

menu()
