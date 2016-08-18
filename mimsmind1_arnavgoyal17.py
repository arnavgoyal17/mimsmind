"""
Version 1: 'Bulls and Cows' Feedback

After you have gotten Version 0 working, you can proceed to implement this slightly more advanced version.

usage: python mimsmind1.py [length]
Once again, the program generates a random number with number of digits equal to length. 
If the command line argument length is not provided, the default value is 3. 
This means that, by default, the random number is in the range of 000 and 999. 

In this version, the program will establish a maximum number of rounds, maxrounds, equal to (2^length) + length. 
For example, if length = 3, then maxrounds = 11.

Then, the program prompts the user to type in a guess, informing the user of the number of digits expected. 
The program will then read the user input, and provide 'bulls and cows' feedback to the user. 
A matching digit in the correct position will result in a 'bull', 
while a matching digit in the wrong position will result in a 'cow'. 
For example, if the correct answer is '123', and the guess is '324', 
then the feedback will be one bull (for the digit '2') and one cow (for the digit '3'). 
More examples are provided below.

At each round, if the user guess is incorrect and maxrounds is not yet reached, 
the program should increment the counter for round and issue a new prompt for user input. 
Otherwise, the program should print a congratulatory or an apologetic message with the number of guesses made, 
and terminate the game.

"""

# Imports
import random
import sys

# Body

# define global variables
numberDigits = 3 # number of digits
mainNumber = 0 # the corrent answer to the game
numberTries = 0

# function to start the game
def StartGame(numberDigits):
    # generate a random number based on the length input by the user
    upperLimit = (10**numberDigits) - 1
    mainNumber = random.randint(0, upperLimit)
    mainNumber = str(mainNumber).zfill(numberDigits)
    numberTries = (2**numberDigits) + numberDigits
    # print(mainNumber)

    print("\nLet's play the mimsmind1 game. You have " + str(numberTries) + " guesses.\n")

    StartGuessing(numberDigits, mainNumber, numberTries)

def StartGuessing(numberDigits, mainNumber, numberTries):
    userInput = ''
    userInputInt = 0
    userTries = 0
    numberBulls = 0
    numberCows = 0
    validInput = False
    firstInput = False

    while True:
        # check if the user has more tries left or not
        if(userTries < numberTries):
            try:
                # different prompt for user's first input
                if(not firstInput):
                    userInput = input("Guess a " + str(numberDigits) + " digit number: ")
                    firstInput = True
                else:
                    if(validInput):
                        userInput = input(str(numberBulls) + " bull(s), " + str(numberCows) + " cow(s). Try again: ")
                        numberBulls = 0
                        numberCows = 0
                    else:
                        # userInput = input("Invalid number. Please enter a " + str(numberDigits) + " digit number: ")
                        userInput = input("Invalid input. Try again: ")
                        numberBulls = 0
                        numberCows = 0
                
                userInputInt = int(userInput)
                if(len(userInput) != numberDigits):
                    raise ValueError
                else:
                    userTries += 1
                    validInput = True
            except ValueError:
                validInput = False
            finally:            
            # continuously ask for User Input and count the number of guesses it took to guess the right answer
                if(validInput):
                    numberBulls = 0
                    numberCows = 0
                    if(userInput == mainNumber):
                        print("Congratulations. You guessed the correct number in " + str(userTries) + " tries.")
                        return
                    else:
                        numberBulls, numberCows = GetCowsBulls(userInput, mainNumber)
        else:
            print("Sorry. You did not guess the number in " + str(numberTries) + " tries. The correct number is " + str(mainNumber) + ".")
            break

def GetCowsBulls(userInput, mainNumber):
    # this would return the number of bulls for the input given by the user
    numberBulls = 0
    numberCows = 0

    # keep a dictionary of digits and indexes where a bull was found
    dictBullIndex = {}

    for n in range(len(str(userInput))):
        # if the position of digit in the input matches with the mainNumber then add 1 to numberBulls
        if(str(mainNumber)[n] == str(userInput)[n]):
            numberBulls += 1

            # append the index to the list so that we know which places were exactly matched
            dictBullIndex[int(mainNumber[n])] = dictBullIndex.get(int(mainNumber[n]), []) + [n]
        else:
            # if the digits at the corresponding position don't match, check if the digit is present at any other position
            numberCows += CalcCows(str(userInput)[n], mainNumber, dictBullIndex)

    return numberBulls, numberCows

def CalcCows(userInputChar, mainNumber, dictBullIndex):
    # find the list of index(s) of the userInputChar in the mainNumber
    # if index != -1 and the index is not in dictBullIndex, then return 1
    # else return 0

    listIndex = []
    n = 0
    isCowFound = False

    for characters in str(mainNumber):
        if(characters == userInputChar):
            listIndex.append(n)
            isCowFound = True
        n += 1

    # get the list of indexes from dictBullIndex corresponding to the userInputChar, if it exists in the list
    listBullIndex = dictBullIndex.get(int(userInputChar), "None")

    if(isCowFound):
        if(type(listBullIndex) == str):
            return 1
        elif(type(listBullIndex) == list):
            for index in listBullIndex:
                if(index in listIndex):
                    listIndex.remove(index)

            # if the list is empty then return 0. This means that the input had repeated digits and the main number had only 1 occurance of the digit
            if(len(listIndex) == 0):
                return 0
            else:
                return 1
    else:
        return 0


def main():
    numberDigits = 3 # number of digits
    numberTries = 0
    
    # check user input
    if(len(sys.argv) == 1):
        StartGame(numberDigits)
    elif(len(sys.argv) == 2):
        # check if the 2nd input is actually an integer
        try:
            userLengthInput = int(sys.argv[1])
            if(userLengthInput <= 0):
                raise ValueError
            else:
                numberDigits = userLengthInput
                StartGame(numberDigits)
            return True
        except ValueError:
            print("Invalid user input: " + str(sys.argv[1]) + ". Please enter a valid positive integer")
            return False

if __name__ == '__main__':
    main()
