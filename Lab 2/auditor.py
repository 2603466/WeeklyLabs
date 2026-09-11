print("Hello and Welcome to the Auditor")
print("============================")
stock_quantity = 0
print("Stock quantity is :", stock_quantity)

while True:
    stock_quantity = input("Enter stock quantity or 'Quit' to quit: ")

    if stock_quantity == "Quit":
        break
    elif stock_quantity[0] == "-":
        print("Invalid because negative number")
        stock_quantity = int(stock_quantity)
        print("Stock Quantity is now :", stock_quantity)
    else:
        print("Enter valid number or \"Quit\" to Quit") 