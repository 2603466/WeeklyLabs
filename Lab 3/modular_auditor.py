MAX_CAPACITY = 500
TAX_RATE = 0.1

def get_valid_input():
    int = input("Input Stoack Quantity or \"quit\" to quit: " )
    if int == "quit":
        return "q"
    elif int.isdigit() and not "": 
        print(int)    

def main():
    inventory = 0

    while True:
        if get_valid_input() == "q":
            break
        


main()

    

    