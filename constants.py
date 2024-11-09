import json

light_bg = "#C77DFF"
dark_bg = "#240046"
sec_bg = "#4C197C" 
clr1 = "#10002B"

UNITS = {
    'Rupee': '₹',
    'Doller': '$',
    'Euro': '€',
}

CATEGORIES = ["Others", "Food and Snacks", "Shopping and Clothing", "Medical and Healthcar", "Utilities", "Rent and Recharges", "Miscellaneous"]

UNIT = '$'
LIMITS = [1, 1, 1]

CONFIG_FILENAME = 'config.json'

def load_config():
    global UNIT, LIMITS
    try:
        with open(CONFIG_FILENAME) as file:
            configuration =  json.load(file)
    except FileNotFoundError:
        configuration = {
            'unit': '₹',
            'daily_limit': 150,
            'weekly_limit': 1200,
            'month_limit': 4500
        }
        with open(CONFIG_FILENAME, 'w') as file:
            json.dump(configuration, file)
    finally:
        UNIT = configuration['unit']
        LIMITS = list(configuration.values())[1:4]
        return configuration

def update_config(unit=None, daily_limit=None, weekly_limit=None, monthly_limit=None):
    configuration = load_config()
    if unit:
        configuration['unit'] = UNITS[unit]
    if daily_limit:
        configuration['daily_limit'] = float(daily_limit)
    if weekly_limit:
        configuration['weekly_limit'] = float(weekly_limit)
    if monthly_limit:
        configuration['monthly_limit'] = float(monthly_limit)
    with open(CONFIG_FILENAME, 'w') as file:
        json.dump(configuration, file)
    load_config()
load_config()

def get_currency(unit=UNIT):
   for x, y in UNITS.items():
       if y == UNIT:
           return x
   