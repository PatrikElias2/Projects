import random
import os
from Stages import stages
from Words import get_words


def Hangman():
    # Welcome print
    print("Welcome to the game called Hangman. You got 6 lives to guess the word. Good Luck!")
    # Random word generator
    words = get_words()
    random_word = words[random.randint(0, len(words)-1)]

    # Generator  of "_"
    hidden_word = []
    for one_letter in random_word:
        hidden_word.append("_")


    # Lives
    lives = 6
    print(stages[lives])

    # Printing word in string
    printedWord = ""
    for one_letter in hidden_word:
        printedWord += one_letter
    print(printedWord)

    while "_" in hidden_word:
        guess = input("Guess the letter\n").lower()
        for index in range(0, len(random_word)):
            if guess == random_word[index]:
                hidden_word[index] = guess

        # Checking lives
        if guess not in random_word:
            lives -= 1
            print(stages[lives])

        print(f"Remaining lives: {lives}")

        if lives == 0:
            print("You Lost!")
            print("The word was "+ random_word)
            again = input("Do you want to play the game again? yes/no\n")
            
            if again == "yes":
                os.system("cls")
                lives = 6  # Reset lives
                hidden_word = []  # Reset hidden word
                # ... other variable resets if needed
                Hangman()  # Call the function again
            elif again == "no":
                os.system("cls")
                break
            else:
                print("Wrong input. If you want to start the game again, you have to do it manually.")
                break

        # Printing word in string
        printedWord = ""
        for one_letter in hidden_word:
            printedWord += one_letter
        print(printedWord)

        # Checking victory
        if "_" not in hidden_word:
            print("You Won!!!")
            print("The word was "+ random_word)
            again = input("Do you want to play the game again? yes/no\n")
            if again == "yes":
                os.system("cls")
                lives = 6  # Reset lives
                hidden_word = []  # Reset hidden word
                # ... other variable resets if needed
                Hangman()  # Call the function again
            elif again == "no":
                os.system("cls")
                break
            else:
                print("Wrong input. If you want to start the game again, you have to do it manually.")
                break

        
Hangman()
            
        

        