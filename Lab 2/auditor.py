inventory = 0

while True:
    
    quantity = input("Enter stock quantity, or \"q\" to quit: ")

    if quantity == "q":
        break

    if quantity.isdigit() and int(quantity) >= 0:
        inventory += int(quantity)
        print(inventory)

    else:
        print("Invalid Input")      
        