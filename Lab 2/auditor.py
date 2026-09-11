print("Hello and Welcome to the Auditor")
print("============================")
stock_quantity = 0
inventory = 0
failed_entries = 0
failed_entries_total = 0
print("Stock quantity is :", stock_quantity)

while True:
    stock_quantity = input("Enter stock quantity or 'Quit' to quit: ")

    if stock_quantity.isdigit():
        stock_quantity = int(stock_quantity)
        inventory += stock_quantity
        if stock_quantity == 0:
            print("No Inventory Keyed")
            failed_entries += 1
            failed_entries_total += failed_entries
            
        if inventory > 500:
            print("Inventory Exceed 500: "), inventory
            failed_entires += 1
            failed_entries_total += failed_entries

        print("Total Inverntory is :", inventory)
    else:
        if stock_quantity == "Quit":
            print("User has quit")
            print("Total failed entries :", failed_entries_total)
            break
        elif stock_quantity[0] == "-":
            print("Invalid because negative number")
            failed_entries += 1
            failed_entries_total += failed_entries
        else: 
            print("Invalid input") 

