MAX_CAPACITY = 500
TAX_RATE = 0.1

def get_valid_input():
    quantity = input("Input Stock Quantity or \"quit\" to quit: " ) #check if input is to quit
    if quantity == "quit":
        return "q"
    
    if quantity.isdigit() and int(quantity) > 0: #check for if digit is bool and if its a -ve int
        return int(quantity)

    else:
        print("Error not valid input")
        return "error"

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * TAX_RATE

def generate_report(total_units, failed_entries):
    print("Total errors: ",failed_entries)
    print("Total Inventory: ",total_units)
    return

def main():
    inventory = 0
    failed_entries = 0
    
    while True:
        stock = get_valid_input()
        total_tax = calculate_tax(inventory)

        if stock == "q":
            generate_report(inventory, failed_entries)
            break

        elif stock == "error":
            failed_entries += 1

        else:
            inventory = process_delivery(inventory, stock)
            print ("Total Inventory is: ", inventory)

            calculate_tax(inventory)
            print("Total Tax is: ", total_tax)

main()

    

    