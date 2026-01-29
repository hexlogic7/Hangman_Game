import random
import socket

def get_random_word():
    words = ["apple", "grape", "plane", "tiger", "house", "river",
             "brick", "snake", "chair", "smile", "bread", "light",
             "stone", "cloud", "music", "beach", "train", "grass"
    ]
    return random.choice(words)

stages = [r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']


# =======Mode Selection ============

print("1. Single Player")
print("2. Multiplayer (Same Wifi)")
mode = input("Choose mode: ")

# ======= Multiplayer ============== 

def multiplayer_host(chosen_word):
    host = ""
    port = 5555

    server = socket.socket()
    server.bind((host, port))
    server.listen(1)

    print("Waiting for another player to join...")
    conn, addr = server.accept()
    print("Player joined: ", addr)

    lives = 6
    correct_letters = []
    guessed_letters = []

    while lives > 0:
        display = ""
        for letter in  chosen_word:
            if letter in correct_letters:
                display += letter
            else:
                display += "_"

        conn.send(f"{display}|{lives}".encode())

        if "_" not in  display:
            conn.send(b"WIN")
            break

        guess = conn.recv(1024).decode().lower()

        if guess in guessed_letters:
            continue

        guessed_letters.append(guess)

        if guess in chosen_word:
            if guess not in correct_letters:
                correct_letters.append(guess)
        else:
            lives -= 1

    if lives == 0:
        conn.send(b"LOSE")

    conn.close()
    server.close()

def multiplayer_join():
    ip = input("Enter host IP address: ")
    port = 5555

    client = socket.socket()
    client.connect((ip, port))

    while True:
        data = client.recv(1024).decode()

        if data == "WIN":
            print("You win!")
            break

        if data == "LOSE":
            print("You lose!")
            break

        display, lives = data.split("|")
        lives = int(lives)

        print("Word: ", display)
        print("Lives: ", lives)
        print(stages[lives])

        guess = input("Guess a letter: ").lower()
        client.send(guess.encode())

    client.close()

#======Multiplayer Entry point=======


if mode == "2":
    choice = input("1.Host game\n2.Join game\nChoose: ")

    if choice == "1":
        chosen_word = get_random_word()
        multiplayer_host(chosen_word)
    else:
        multiplayer_join()

    exit()
# TODO-1: - Create a variable called 'lives' to keep track of the number of lives left.
#  Set 'lives' to equal 6.

lives = 6
chosen_word = get_random_word()

placeholder = "_" * len(chosen_word)
print(placeholder)

correct_letters = []
guessed_letters = []

while True:
    guess = input("Guess a letter: ").lower()

    if guess in guessed_letters:
        print("Already guessed!")
        continue

    guessed_letters.append(guess)

    display = ""

    for letter in chosen_word:
        if letter == guess:
            display += letter
            correct_letters.append(guess)
        elif letter in correct_letters:
            display += letter
        else:
            display += "_"

    print(display)

    # TODO-2: - If guess is not a letter in the chosen_word, Then reduce 'lives' by 1.
    #  If lives goes down to 0 then the game should stop and it should print "You lose."

    if "_" not in display:
        print("You win!")
        break


    if guess not in chosen_word:
        lives -= 1
        print(stages[lives])

    # TODO-3: - print the ASCII art from 'stages'
    #  that corresponds to the current number of 'lives' the user has remaining.
    if lives == 0:
        print("GAME OVER")
        break
