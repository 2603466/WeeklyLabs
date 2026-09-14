inventory = 0 # running total
failed_entries = 0

while True:
    
    quantity = input("Enter stock quantity, or \"q\" to quit: ")

    if quantity == "q":
        print("failed entires: ",failed_entries)
        print("total inventory: ",inventory)
        break

    if quantity.isdigit() and int(quantity) >= 0:
        inventory += int(quantity)
        print(inventory)

    else:
        failed_entries += 1
        print("Invalid Input")

    if int(inventory) > 500:
        print("Overstock Quantity: ", inventory)
        break