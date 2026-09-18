MAX_CAPACITY = 500
TAX_RATE = 0.1

def get_valid_input():
    quantity = input("Input Stock Quantity or \"quit\" to quit: " ) #check if input is to quit
    if quantity == "quit":
        return "q"
    
    if quantity.isdigit() and int(quantity) > 0: #check for if digit is bool and if its a -ve int
        print("valid input")
        return int(quantity)

    else:
        print("Error not valid input")
        return "quantity"

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * TAX_RATE

def main():
    inventory = 0
    
    while True:
        stock = get_valid_input()
        total_tax = calculate_tax(inventory)

        if stock == "q":
            break

        else:
            inventory = process_delivery(inventory, stock)
            print ("Total Inventory is: ", inventory)

            calculate_tax(inventory)
            print("Total Tax is: ", total_tax)

main()

    

    