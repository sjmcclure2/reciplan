from django.apps import AppConfig


class ReciplanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reciplan'


class Y_Conversions(AppConfig):
    # Takes in the amount of cups and converts to an appropriate DRY unit based on amount
    def update_d_units(cup_amt): 
        # If the amount is 1/4 cup or more, maintain measurement in cups
        if cup_amt >= (1/4):
            unit = 'cup'
            return cup_amt, unit
        # If the amount is less than 1/4 cup but more than 1/8 cup, convert to tbsp
        elif cup_amt < (1/4) and cup_amt >= (1/8):
            unit = 'tbsp'
            return 16 * cup_amt, unit
        # If the amount is less than 1/8 cup, convert to tsp
        else:
            unit = 'tsp'
            return 48 * cup_amt, unit

    # Takes in the amount of cups and converts to an appropriate LIQUID unit based on amount
    def update_l_units(cup_amt):
        # If the amt is less than 1 cup, convert to fl oz
        if cup_amt < 1:
            unit = "fl oz"
            return 8 * cup_amt, unit
        # If the amt is between 1 and 4 cups, maintain measurement in cups
        elif cup_amt >= 1 and cup_amt <= 4:
            unit = 'cup'
            return cup_amt, unit
        # if the amt is more than 3 but no more than 8, convert to pints
        elif cup_amt > 5 and cup_amt < 8:
            unit = 'pint'
            return (1/2) * cup_amt, unit
        # If the amt is more than 3 but no more than 15, convert to quarts
        elif cup_amt >= 8 and cup_amt < 16:
            unit = 'quart'
            return (1/4) * cup_amt, unit
        # if the amt is more than 16 cups, convert to gallons
        else:
            unit = 'gallon'
            return (1/16) * cup_amt, unit
    
    def update_yield(o_yield, t_yield, unit, amt):
        # Converts the original yield ingredient amount into the target yield amount
        adj_amt = (amt/o_yield) * t_yield

        if unit == "fl oz":
            cup_amt = (1/8) * adj_amt
            output = update_l_units(cup_amt)
            return output
        elif unit == "pint":
            cup_amt = 2 * adj_amt
            output = update_l_units(cup_amt)
            return output
        elif unit == "quart":
            cup_amt = 4 * adj_amt
            output = update_l_units(cup_amt)
            return output
        elif unit == "gallon":
            cup_amt = 16 * adj_amt
            output = update_l_units(cup_amt)
            return output
        elif unit == "tsp":
            cup_amt = (1/48) * adj_amt
            output = update_d_units(cup_amt)
            return output
        elif unit == "tbsp":
            cup_amt = (1/16) * adj_amt
            output = update_d_units(cup_amt)
            return output
        elif unit == "cup":
            cup_amt = adj_amt
            output = update_d_units(cup_amt)
            return output
        elif unit == "l_cup":
            cup_amt = adj_amt
            output = update_l_units(cup_amt)
            return output
        elif unit == "ea":
            return adj_amt, unit
        else:
            return print("Error!")