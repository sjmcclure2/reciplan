class Convert:   
     
    # This function will convert every unit into cups for 
    # to be stored in the database for later use
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
            return adj_amt
        else:
            return print("Error Message")  
        
     
    # This helper function will convert dry units of measure based on yield size
    # Example: we wouldn’t want the recipe to return 48 tsp when it could
    # be summed up as 1 cup.
    @staticmethod
    def update_d_units(cup_amt, t_yield):
        adj_amt = cup_amt * t_yield
        # If the amount is 1/4 cup or more, maintain measurement in cups
        if adj_amt >= (1/4):
            unit = 'cups'
            return adj_amt, unit
        # If the amount is less than 1/4 cup but more than 1/8 cup, convert to tbsp
        elif adj_amt < (1/4) and adj_amt >= (1/8):
            unit = 'tbsp'
            return 16 * adj_amt, unit
        # If the amount is less than 1/8 cup, convert to tsp
        else:
            unit = 'tsp'
            return 48 * adj_amt, unit


    # This helper function will convert liquid units of measure based on yield size
    # Example: we wouldn’t want the recipe to return 8 fl oz when it could
    # be summed up as 1 cup.
    @staticmethod
    def update_l_units(cup_amt, t_yield):
        adj_amt = cup_amt * t_yield
        # If the amt is less than 1 cup, convert to fl oz
        if adj_amt < 1:
            unit = "fl oz"
            return 8 * adj_amt, unit
        # If the amt is between 1 and 4 cups, maintain measurement in cups
        elif adj_amt >= 1 and adj_amt <= 4:
            unit = 'cups'
            return adj_amt, unit
        # if the amt is more than 5 but no more than 8 cups, convert to pints
        elif adj_amt > 5 and adj_amt < 8:
            unit = 'pints'
            return (1/2) * adj_amt, unit
        # If the amt is greater or equal to 8 but less than 16 cups, convert to quarts
        elif adj_amt >= 8 and adj_amt < 16:
            unit = 'quarts'
            return (1/4) * adj_amt, unit
        # if the amt is 16 or more cups, convert to gallons
        else:
            unit = 'gallons'
            return (1/16) * adj_amt, unit
        
    
    # 1 - 14 mL --> tsp           
    # 15 - 29 mL --> Tbsp           
    # 30 - 236 mL --> fl oz         
    # 237 - 473 mL --> cup        
    # 474 - 949 mL --> pint     
    # 0.95 - 3.7 L --> quart     
    # 3.8 and up L --> gallon                
    # 0 - 454 grams --> oz
    # 455+ --> lbs   
    # Kg (always) --> lbs    
    def metric_imperial(amt, unit):         
        if(unit == "mL" and amt <= 14):
            conv_amt =  amt * 0.202
            new_unit = "tsp"
            return conv_amt, new_unit
        elif(unit == "mL" and amt >= 15 and amt <= 29):
            conv_amt = amt * 0.0676
            new_unit = "Tbsp"
            return conv_amt, new_unit
        elif(unit == "mL" and amt >= 30 and amt <= 236):
            conv_amt = amt * 0.0338
            new_unit = "fl oz"
            return conv_amt, new_unit
        elif(unit == "mL" and amt >= 237 and amt <= 473):
            conv_amt = amt * 0.0035
            if(conv_amt <= 1):
                new_unit = "cup"
            else:
                new_unit = "cups"
            return conv_amt, new_unit
        elif(unit == "mL" and amt >= 474 and amt <= 949):
            conv_amt = amt * 0.0021
            if(conv_amt <= 1):
                new_unit = "pint"
            else:
                new_unit = "pints"
            return conv_amt, new_unit
        elif(unit == "liters" and amt <= 3.7):
            conv_amt = amt * 1.06
            if(conv_amt <= 1):
                new_unit = "quart"
            else:
                new_unit = "quarts"
            return conv_amt, new_unit
        elif(unit == "liters" and amt > 3.7):
            conv_amt = amt * 0.264
            if(conv_amt <= 1):
                new_unit = "gallon"
            else:
                new_unit = "gallons"
            return conv_amt, new_unit
        elif(unit == "grams" and amt <= 454): 
            conv_amt = amt/28.35
            new_unit = "oz"   
            return conv_amt, new_unit
        elif(unit == "grams" and amt > 454):
            conv_amt = amt/454 
            new_unit = "lbs"
            return conv_amt, new_unit
        elif(unit == "Kg"):
            conv_amt = amt * 2.205
            new_unit = "lbs"
            return conv_amt, new_unit
        if(unit == "tsp"):
            conv_amt = amt * 4.929
            unit = "mL"
            return conv_amt, unit
        elif(unit == "tbsp"):
            conv_amt = amt * 14.787
            unit = "mL"
            return conv_amt, unit
        elif(unit == "fl oz"):
            conv_amt = amt * 29.574
            unit = "mL"
            return conv_amt, unit
        elif(unit == "cups"):
            conv_amt = amt * 284
            unit = "mL"
            return conv_amt, unit
        elif(unit == "pints"):
            conv_amt = amt * 568
            unit = "mL"
            return conv_amt, unit
        elif(unit == "quarts"):
            conv_amt = amt * 1.137
            unit = "liter"
            return conv_amt, unit
        elif(unit == "gallons"):
            conv_amt = amt * 4.564
            unit = "liter"
            return conv_amt, unit
        #oz to grams
        elif(unit == "oz"):
            conv_amt = amt * 28.35
            unit = "grams"
            return conv_amt, unit
        #lbs to Kg      
        elif(unit == "lbs"):
            conv_amt = amt/2.205
            unit = "Kg"
            return conv_amt, unit
        else:
            return print("Error: In-correct unit sent to function")
        
        
# This function is what will be called to perform target yield conversions from the templates   
def convert_yield(t_yield, unit, cup_amt):
    if(unit == "ea"):
        output = cup_amt * t_yield
        return output, unit
    elif(unit == "tsp" or unit == "Tbsp" or unit == "cups"):
        return Convert.update_d_units(cup_amt, t_yield)  
    elif(unit == "fl oz" or unit == "fl_cups" or unit == "pints" or unit == "quarts" or unit == "gallons"):
        return Convert.update_l_units(cup_amt, t_yield)