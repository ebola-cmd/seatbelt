import os
import datetime
import json
import requests
import yfinance as yf
import time
from characterai import aiocai
import asyncio
from rich.console import Console
from rich.table import Table
from rich.text import Text
import keyboard


WIDTH, HEIGHT = 20, 10
x, y = 0, 0  # Initial cursor position
draw_char = "*"  # Character to draw with
drawing_pad = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
console = Console()
virtual_balance = 10000.00
portfolio = {}
BIRTHDAY_FILE = "birthdays.json"

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
    print(f"{GREEN}[>] {RESET}{BLUE}Version{RESET}      : 1.7")
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

    if choice == "-stocks":
        get_top_stock_data()

    if choice == "-s":
        symbol = input("Enter stock ticker symbol: ")
        get_additional_stock_data(symbol)
    
    if choice == "-ai":
        ai()

    if choice == "-tt":
        tt()

    if choice == "-ssim":
        ssim()
    
    if choice == "-ab":
        add_birthday()

    if choice == "-vb":
        view_birthdays()

    if choice == "-ub":
        view_upcoming_birthdays()
        
    else:
        input(f"{YELLOW}[!] Invalid command enter to continue... :{RESET}")
        menu()
    
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
    print("-stocks           : Get the current price, daily high, and low for the top 5 stocks and the S&P 500.")
    print("-s                : Get the current price, daily high, and low for a specific stock.")
    print('-ai               : Chatgpt.')
    print("-tt               : Display the school timetable.")
    print("-ssim             : Start Stock Simulator to buy/sell stocks and track portfolio.")
    print("-ab               : Add a new birthday.")
    print("-vb               : View all birthdays.")
    print("-ub               : View upcoming birthdays within the next 30 days.")
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

def get_top_stock_data():
    top_stocks = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "^GSPC"]  # S&P 500 is "^GSPC"
    print("\nTop 5 Stocks and S&P 500 Index Prices:\n")
    print(f"{'Ticker':<10}{'Current Price':<15}{'High Price':<15}{'Low Price':<15}")
    print("-" * 50)
                    
    for stock in top_stocks:
        ticker = yf.Ticker(stock)
        info = ticker.history(period="1d")
        if not info.empty:
            current_price = info['Close'].iloc[-1]
            high_price = info['High'].iloc[-1]
            low_price = info['Low'].iloc[-1]
            print(f"{stock:<10}${current_price:<14.2f}${high_price:<14.2f}${low_price:<14.2f}")

        else:
            print(f"{stock:<10}Data unavailable")
    
    input("\nPress Enter to return to the menu...")
    menu()

def get_additional_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.history(period="1d")
    if not info.empty:
        current_price = info['Close'].iloc[-1]
        high_price = info['High'].iloc[-1]
        low_price = info['Low'].iloc[-1]
        print("\nCustom Stock Search:\n")
        print(f"{'Ticker':<10}{'Current Price':<15}{'High Price':<15}{'Low Price':<15}")
        print("-" * 50)
        print(f"{symbol.upper():<10}${current_price:<14.2f}${high_price:<14.2f}${low_price:<14.2f}")
    else:
        print("\nData unavailable for the specified ticker.")
    
    input("\nPress Enter to return to the menu...")
    menu()

def ai():
    async def main():
        char = '7IA8Bw3NsyjruZH-8gLLKqzo3UdZ_2QBvqrCBlS0__U'
        client = aiocai.Client('4db9b2da990ca50b07a6ecf109621d47b4d2ad49')

        me = await client.get_me()

        async with await client.connect() as chat:
            new, answer = await chat.new_chat(
                char, me.id
            )

            print(f'{answer.name}: {answer.text}')
                                                                                
            while True:
                text = input('YOU: ')

                message = await chat.send_message(
                    char, new.chat_id, text
                )

                print(f'{message.name}: {message.text}')
                                                                                                                                                                
                if text == "/bye":
                    menu()
                    break

    asyncio.run(main())

def tt():
    timetable = {
    "Monday": ["CTP", "CTP", "SST", "Math", "CP", "Arabic", "English", "CTP", "STEM", "STEM", "X"],
    "Tuesday": ["CTP", "CTP", "Electives", "Electives", "English", "Arabic", "Hindi", "Math", "Math", "Science", "SST"],
    "Wednesday": ["CTP", "PE", "Hindi", "Math", "SST", "Science", "English", "Arabic", "Library", "Science", "Math"],
    "Thursday": ["CTP", "Math", "M.E", "UAE SST", "Math", "CP", "Hindi", "Science", "English", "Arabic", "Science"],
    }
        
    # Set up the table layout
    table = Table(title="", header_style="bold cyan")
                
    # Adding columns
    table.add_column("Period", style="bold yellow")
    for day in timetable.keys():
        table.add_column(day, style="bold magenta")
                                            
    # Adding rows by period (up to 11 periods)
    for period in range(1, 12):
        row = [f"Period {period}"]
        for day, subjects in timetable.items():
            row.append(subjects[period - 1])
        table.add_row(*row)

    # Display the timetable with animations
    console.print(Text("\n=== Weekly School Timetable ===", style="bold green"))
    console.print(table)
    input('enter to continue...')
    menu()

def ssim():
    def get_stock_price(symbol):
        """Fetch the current stock price for a given symbol."""
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        return data['Close'].iloc[-1]

    def buy_stock(symbol, quantity):
        """Simulate buying a stock."""
        global virtual_balance
        stock_price = get_stock_price(symbol)
        cost = stock_price * quantity

        if virtual_balance >= cost:
            virtual_balance -= cost
            if symbol in portfolio:
                portfolio[symbol] += quantity
            else:
                portfolio[symbol] = quantity
            print(f"Successfully bought {quantity} shares of {symbol}!")
            input('enter to continue')
        else:
            print("Insufficient funds!")
            input('enter to continue')

    def sell_stock(symbol, quantity):
        """Simulate selling a stock."""
        global virtual_balance
        if symbol in portfolio and portfolio[symbol] >= quantity:
            stock_price = get_stock_price(symbol)
            revenue = stock_price * quantity
            portfolio[symbol] -= quantity
            virtual_balance += revenue
            print(f"Successfully sold {quantity} shares of {symbol}!")
            input('enter to continue')
        else:
            print("You don't own enough of this stock!")
            input('enter to continue')

    def check_portfolio():
        """Display the user's current stock portfolio and virtual balance."""
        print("\nCurrent Portfolio:")
        for symbol, quantity in portfolio.items():
            stock_price = get_stock_price(symbol)
            print(f"{symbol}: {quantity} shares (Current Price: ${stock_price:.2f})")
            print(f"Virtual Balance: ${virtual_balance:.2f}")
            input('enter to continue')

    def display_menu():
        os.system('cls')
        """Display the custom ASCII menu with color options."""
        menu_art = """

    ███████╗████████╗ ██████╗  ██████╗██╗  ██╗    ███████╗██╗███╗   ███╗
    ██╔════╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝    ██╔════╝██║████╗ ████║
    ███████╗   ██║   ██║   ██║██║     █████╔╝     ███████╗██║██╔████╔██║
    ╚════██║   ██║   ██║   ██║██║     ██╔═██╗     ╚════██║██║██║╚██╔╝██║
    ███████║   ██║   ╚██████╔╝╚██████╗██║  ██╗    ███████║██║██║ ╚═╝ ██║
    ╚══════╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝    ╚══════╝╚═╝╚═╝     ╚═╝
        """
        print(menu_art)

    def smenu():
        """Main menu for interacting with the stock simulator."""
        while True:
            display_menu()  # Show the ASCII menu

            # Colorful options in the menu
            print(f"{YELLOW}[!] Select an Option :{RESET}")
            print('')
            print(f"{GREEN}[1] {RESET}{BLUE}Buy Stock{RESET}")
            print(f"{GREEN}[2] {RESET}{BLUE}Sell Stock{RESET}")
            print(f"{GREEN}[3] {RESET}{BLUE}Check Portfolio{RESET}")
            print(f"{GREEN}[4] {RESET}{BLUE}Exit{RESET}")

            choice = input(f"{YELLOW}Enter your choice: {RESET}")

            if choice == "1":
                symbol = input(f"{YELLOW}Enter the stock symbol (e.g., AAPL, TSLA): {RESET}").upper()
                quantity = int(input(f"{YELLOW}Enter the number of shares to buy: {RESET}"))
                buy_stock(symbol, quantity)
            elif choice == "2":
                symbol = input(f"{YELLOW}Enter the stock symbol to sell: {RESET}").upper()
                quantity = int(input(f"{YELLOW}Enter the number of shares to sell: {RESET}"))
                sell_stock(symbol, quantity)
            elif choice == "3":
                check_portfolio()
            elif choice == "4":
                print(f"{RED}Thank you for using the Stock Simulator!{RESET}")
                menu()
                break
            else:
                print(f"{RED}Invalid option. Please try again.{RESET}")

    if __name__ == "__main__":
        smenu()

def load_birthdays():
    if os.path.exists(BIRTHDAY_FILE):
        with open(BIRTHDAY_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

def save_birthdays(birthday_data):
    with open(BIRTHDAY_FILE, "w") as file:
        json.dump(birthday_data, file, indent=4)

def add_birthday():
    name = input("Enter name: ")
    date = input("Enter birthday (YYYY-MM-DD): ")
    try:
        # Validate date
        datetime.datetime.strptime(date, "%Y-%m-%d")
        birthdays[name] = date
        save_birthdays(birthdays)  # Save to file
        print(f"{GREEN}Birthday added for {name}.{RESET}")
        input('enter to continue...')
        menu()
    except ValueError:
        print(f"{YELLOW}Invalid date format. Please use YYYY-MM-DD.{RESET}")
        input('enter to continue...')
        menu()

def view_birthdays():
    print(f"\n{YELLOW}All Birthdays:{RESET}")
    if birthdays:
        for name, date in birthdays.items():
            print(f"{name}: {date}")
        input('enter to continue...')
        menu()
    else:
        print(f"{YELLOW}No birthdays available.{RESET}")
        input('enter to continue...')
        menu()

def view_upcoming_birthdays():
    today = datetime.date.today()
    upcoming_birthdays = []

    for name, date in birthdays.items():
        birthday_this_year = datetime.date(today.year, int(date[5:7]), int(date[8:]))
        if today <= birthday_this_year <= (today + datetime.timedelta(days=30)):
            upcoming_birthdays.append((name, birthday_this_year))

    if upcoming_birthdays:
        print(f"\n{YELLOW}Upcoming Birthdays in the Next 30 Days:{RESET}")
        for name, date in sorted(upcoming_birthdays, key=lambda x: x[1]):
            days_left = (date - today).days
            print(f"{name}: {date.strftime('%Y-%m-%d')} ({days_left} days left)")
        input('enter to continue...')
        menu()

    else:
        print(f"{YELLOW}No upcoming birthdays in the next 30 days.{RESET}")
        input('enter to continue...')
        menu()

birthdays = load_birthdays()

menu()
