class Convert:    
    def to_cups( o_yield, unit, amt):

        adj_amt = (amt/o_yield) 

        if unit == "fl_oz":
            cup_amt = (1/8) * adj_amt
            return cup_amt
        elif unit == "pints":
            cup_amt = 2 * adj_amt
            return cup_amt
        elif unit == "quarts":
            cup_amt = 4 * adj_amt
            return cup_amt
        elif unit == "gallons":
            cup_amt = 16 * adj_amt
            return cup_amt
        elif unit == "tsp":
            cup_amt = (1/48) * adj_amt
            return cup_amt
        elif unit == "Tbsp":
            cup_amt = (1/16) * adj_amt
            return cup_amt
        elif unit == "cups":
            cup_amt = adj_amt
            return cup_amt
        elif unit == "fl_cups":
            cup_amt = adj_amt
            return cup_amt
        elif unit == 'mL':
            cup_amt = adj_amt/237
            return cup_amt
        elif unit == 'liters':
            cup_amt = adj_amt * 0.237
            return cup_amt 
        elif unit == "ea":
            return adj_amt, unit
        else:
            return print("You dun messed up AA-ron")

    def update_d_units(cup_amt, t_yield):
        adj_amt = cup_amt * t_yield

        # If the amount is 1/4 cup or more, maintain measurement in cups
        if adj_amt >= (1/4):
            unit = 'cup'
            return adj_amt, unit
        # If the amount is less than 1/4 cup but more than 1/8 cup, convert to tbsp
        elif adj_amt < (1/4) and adj_amt >= (1/8):
            unit = 'tbsp'
            return 16 * adj_amt, unit
        # If the amount is less than 1/8 cup, convert to tsp
        else:
            unit = 'tsp'
            return 48 * adj_amt, unit

    def update_l_units(cup_amt, t_yield):
        adj_amt = cup_amt * t_yield

        # If the amt is less than 1 cup, convert to fl oz
        if adj_amt < 1:
            unit = "fl oz"
            return 8 * adj_amt, unit
        # If the amt is between 1 and 4 cups, maintain measurement in cups
        elif adj_amt >= 1 and adj_amt <= 4:
            unit = 'cup'
            return adj_amt, unit
        # if the amt is more than 3 but no more than 8 cups, convert to pints
        elif adj_amt > 5 and adj_amt < 8:
            unit = 'pint'
            return (1/2) * adj_amt, unit
        # If the amt is more than 3 but no more than 15 cups, convert to quarts
        elif adj_amt >= 8 and adj_amt < 16:
            unit = 'quart'
            return (1/4) * adj_amt, unit
        # if the amt is more than 16 cups, convert to gallons
        else:
            unit = 'gallon'
            return (1/16) * adj_amt, unit

    def metric_imperial(amt, unit):
        # 1 - 14 mL --> tsp             0.2 tsp = 1 mL
        # 15 - 29 mL --> Tbsp           15 mL = 1 Tbsp
        # 30 - 236 mL --> fl oz         30 mL = 1 fl oz
        # 237 - 472 mL --> cups         237 mL = 1 cup
        # 473 - 949 mL --> pints        473 mL = 1 pint
        # 0.95 - 3.7 L --> quarts       0.95 L = 1 quart
        # 3.8 and up L --> gallons      3.8 L = 1 gallon
        # 0.01 - 0.34 oz --> grams      0.35 oz = 1 gram
        # 0.35 - 34 oz --> Kg           35 oz = 1 Kg
        # lbs to grams                  1 lb = 0.45 Kg
        conv_amt = None
        
        return conv_amt
        