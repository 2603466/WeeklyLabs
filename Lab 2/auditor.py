inventory = 0

while True:
    
    quantity = input("Enter stock quantity, or \"q\" to quit: ")

    if quantity == "q":
        break

    quantity = int(quantity)
    print(type(quantity))

    inventory += quantity
    print(inventory)