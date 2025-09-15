# Task 1:
def calculate_discount(price, discount_percent):
    
    if discount_percent >= 0.20:
        
        return price*discount_percent
    else:
        return price
    
    
print(calculate_discount(5000, 0.20))

#Task 2:
price = int(input("Please input the origin price:"))
discount_percent = float(input("Please input the discount percent:"))
def calculate_discount1():
    if discount_percent >= 0.20:
         return price*discount_percent
    else:
        return price
    
    
