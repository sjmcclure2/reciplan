class Convert:   
    # This function will convert every unit into cups for 
    # to be stored in the database for later use
    def to_cups( o_yield, unit, amt):
        adj_amt = (amt/o_yield) 
        if unit == "fl_oz":
            cup_amt = adj_amt/8.115
            return round(cup_amt, 2) 
        elif unit == "pints":
            cup_amt = adj_amt/0.507
            return round(cup_amt, 2) 
        elif unit == "quarts":
            cup_amt = adj_amt/0.254
            return round(cup_amt, 2) 
        elif unit == "gallons":
            cup_amt = adj_amt/0.063
            return round(cup_amt, 2) 
        elif unit == "tsp":
            cup_amt = adj_amt/48.692
            return round(cup_amt, 2) 
        elif unit == "Tbsp":
            cup_amt = adj_amt/16.231
            return round(cup_amt, 2) 
        elif unit == 'mL':
            cup_amt = adj_amt/240
            return round(cup_amt, 2) 
        elif unit == 'liters':
            cup_amt = adj_amt/0.240
            return round(cup_amt, 2) 
        else:
            return round(adj_amt, 2)
    
    # 1 - 14 mL --> tsp           
    # 15 - 29 mL --> Tbsp  
    # 237 - 473 mL --> cup    
    @staticmethod
    def update_d_units(cup_amt, t_yield):
        adj_amt = cup_amt * t_yield
        # If the amount is 1/4 cup or more, maintain measurement in cups
        if adj_amt >= (1/4):
            unit = 'cups'
            return round(adj_amt, 2), unit
        # If the amount is less than 1/4 cup but more than 1/8 cup, convert to tbsp
        elif adj_amt < (1/4) and adj_amt >= (1/8):
            unit = 'tbsp'
            return round(16 * adj_amt, 2), unit
        # If the amount is less than 1/8 cup, convert to tsp
        else:
            unit = 'tsp'
            return round(48 * adj_amt, 2), unit

        
    # 30 - 236 mL --> fl oz  
    #              --> fl_cups            
    # 474 - 949 mL --> pint     
    # 0.95 - 3.7 L --> quart     
    # 3.8 and up L --> gallon                
    @staticmethod
    def update_l_units(cup_amt, t_yield):
        adj_amt = cup_amt * t_yield
        # If the amt is less than 1 cup, convert to fl oz
        if adj_amt < 1:
            unit = "fl_oz"
            return round(8.115 * adj_amt, 2), unit
        # If the amt is between 1 and 4 cups, maintain measurement in cups
        elif adj_amt >= 1 and adj_amt <= 4:
            unit = 'fl_cups'
            return round(adj_amt, 2), unit
        # if the amt is more than 5 but no more than 8 cups, convert to pints
        elif adj_amt > 5 and adj_amt < 8:
            unit = 'pints'
            return round((1/2) * adj_amt, 2), unit
        # If the amt is greater or equal to 8 but less than 16 cups, convert to quarts
        elif adj_amt >= 8 and adj_amt < 16:
            unit = 'quarts'
            return round((1/4) * adj_amt, 2), unit
        # if the amt is 16 or more cups, convert to gallons
        else:
            unit = 'gallons'
            return round((1/16) * adj_amt, 2), unit
        
    @staticmethod
    def update_m_units(cup_amt, t_yield):
        adj_amt = cup_amt * t_yield
        if(unit == "Kg"):
            unit = "lbs"
            return round(adj_amt, 2), unit
        elif(unit == "grams"):
            unit = "oz"
            return round(adj_amt, 2), unit
        # Add lbs and oz to be converted into the proper imperial yield ready for metric conversion
        
    @staticmethod  
    def to_metric(amt, unit):         
        if(unit == "tsp"):
            conv_amt = amt * 4.929
            unit = "mL"
            return round(conv_amt, 2), unit
        elif(unit == "tbsp"):
            conv_amt = amt * 14.787
            unit = "mL"
            return round(conv_amt, 2), unit
        elif(unit == "fl_oz"):
            conv_amt = amt * 29.574
            unit = "mL"
            return round(conv_amt, 2), unit
        elif(unit == "cups"):
            conv_amt = amt * 284
            unit = "mL"
            return round(conv_amt, 2), unit
        elif(unit == "pints"):
            conv_amt = amt * 568
            unit = "mL"
            return round(conv_amt, 2), unit
        elif(unit == "quarts"):
            conv_amt = amt * 1.137
            unit = "liter"
            return round(conv_amt, 2), unit
        elif(unit == "gallons"):
            conv_amt = amt * 4.564
            unit = "liter"
            return round(conv_amt, 2), unit
        #oz to grams
        elif(unit == "oz"):
            conv_amt = amt * 28.35
            unit = "grams"
            return round(conv_amt, 2), unit
        #lbs to Kg      
        elif(unit == "lbs"):
            conv_amt = amt/2.205
            unit = "Kg"
            return round(conv_amt, 2), unit
        else:
            return round(amt, 2), unit

# This function is what will be called to perform target yield conversions from the templates   
def convert_yield(t_yield, unit, cup_amt):
    if(unit == "tsp" or unit == "Tbsp" or unit == "cups" or unit == "l_cups"):
        return Convert.update_d_units(cup_amt, t_yield)  
    elif(unit == "fl_oz" or unit == "fl_cups" or unit == "pints" or unit == "quarts" or unit == "gallons" or unit == "mL" or unit == "liters"):
        return Convert.update_l_units(cup_amt, t_yield)
    elif(unit == "lbs" or unit == "Kg" or unit == "oz" or unit == "grams"):
        return Convert.update_m_units(cup_amt, t_yield)
    else:
        output = cup_amt * t_yield
        return round(output, 2), unit