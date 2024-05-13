from menu import MENU
from menu import resources


# ====Introduction====
espresso_price = MENU["espresso"]["cost"]
latte_price = MENU["latte"]["cost"]
cappuccino_price = MENU["cappuccino"]["cost"]


# ====Functions====
# Reading the amount of resources
def report(data):
    print(f"Voda: {data['water']}")
    print(f"Voda: {data['milk']}")
    print(f"Voda: {data['coffee']}")

# Choosing how much coins user inserted and calculating the sum of it
def money():
  print("Insert coins 1, 2, 5, 10, 20, 50")
  coins = [0, 0, 0, 0, 0, 0]  # List to store coin counts (1s, 2s, 5s, etc.)
  coin_values = [1, 2, 5, 10, 20, 50]  # List of coin values

  for index in range(len(coin_values)):
    count = int(input(f"How many {coin_values[index]}s you want to insert?: "))
    coins[index] = count

  total_sum = 0
  for index in range(len(coins)):
    total_sum += coins[index] * coin_values[index]  # Calculate sum using multiplication

  print(f"You have inserted: {total_sum} coins")
  return total_sum


# How much change it needs to be refunded back to user
def withdraw_change(user_sum_coins, price):
   refund = user_sum_coins - price
   if refund >= 0:
      print("We are making your drink.")
      if refund > 0:
         print(f"Here is your change: {refund}")
   else:
      print(f"Not enough money. You need to insert {price - user_sum_coins} more coins.")

# Amount of ingredients it needs to make a drink
def ingredients():
   return resources


# Calculating ingredients and resources
def consumptions_of_ingredients(name_of_drink, ingredients):
   ingredients["water"] = ingredients["water"] - MENU[name_of_drink]["ingredients"]["water"]
   ingredients["milk"] = ingredients["milk"] - MENU[name_of_drink]["ingredients"]["milk"]
   ingredients["coffee"] = ingredients["coffee"] - MENU[name_of_drink]["ingredients"]["coffee"]

def calculate_ingredients(drink):
   if drink == "espresso":
      consumptions_of_ingredients(drink, rest_of_ingredients)
   elif drink == "latte":
      consumptions_of_ingredients(drink, rest_of_ingredients)
   elif drink == "cappuccino":
      consumptions_of_ingredients(drink, rest_of_ingredients)


#Checking amount of ingredients
def ingredients_checker(in_water, in_milk, in_coffee):
   if in_water < 0:
      print("We dont have enough ingredients for drink.")
      return False
   elif in_milk < 0:
      print("We dont have enough ingredients for drink.")
      return False
   elif in_coffee < 0:
      print("We dont have enough ingredients for drink.")
      return False
   else:
      print("We have enough ingredients for your drink.")
      return True


# ====Main script====

# Reading ingredients
rest_of_ingredients = ingredients()

again = True
while(again):
    # User choice
    user_choice = input("What is your choice? (espresso/latte/cappuccino): ")

    # Calculate ingredients
    calculate_ingredients(user_choice)

    # Checker of ingredients
    if user_choice != "report":
       again = ingredients_checker(rest_of_ingredients["water"], rest_of_ingredients["milk"], rest_of_ingredients["coffee"])

    # Continue?
    if again == False:
       break

    # Control report
    if user_choice == "report":
        # run function report() and modify data
        report(rest_of_ingredients)

    # Menu choices
    if user_choice == "espresso":
        sum = money()
        print(f"Price of the espresso is: {espresso_price} coins")
        withdraw_change(sum, espresso_price)
    elif user_choice == "latte":
        sum = money()
        print(f"Price of the latte is: {latte_price} coins")
        withdraw_change(sum, latte_price)
    elif user_choice == "cappuccino":
        sum = money()
        print(f"Price of the cappuccino is: {cappuccino_price} coins")
        withdraw_change(sum, cappuccino_price)