inventory = 0

while True:
    
    quantity = input("Enter stock quantity, or \"q\" to quit: ")

    if quantity == "q":
        break

    inventory += int(quantity)
    print(inventory)    