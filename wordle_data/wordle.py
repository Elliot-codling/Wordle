#new wordle 2.0
from engine import game_engine_50123 as game_engine
from random import randint
import os, pygame
file_dir = os.getcwd()
pygame.font.init()

#create window
w, h, = 310, 400
window = game_engine.window.define("Wordle 2.0", w, h)

#variables
run = True
clock = pygame.time.Clock()

#lists
display = []
background = game_engine.properties_object("bg", f"{file_dir}/textures/black_bg.jpg", 0, 0, w, h, False)            #create the background
display += [background]
for y in range(6):      #create sqaures
    for x in range(5):
        square = game_engine.properties_object("square", f"{file_dir}/textures/square_box.png", (60 * x) + 10, (60 * y) + 10, 50, 50, False)
        display += [square]

#sub programs
def update(display, display_sprite, foreground, text_foreground):               #updates the display
    game_engine.window.update(window, display, display_sprite, foreground, text_foreground, clock, 0)

def reset_game():           #resets all the lists and variables
    global display_sprite, foreground, text_foreground
    global number_letters, inputted_word, number_words, word
    number_letters = 0          #number of letters inputted
    inputted_word = ""          #text version of the number of inputted words
    number_words = 0            #number of words already entered
    word = generate_word()
    print(word)
    
    #lists
    display_sprite = []             
    foreground = []
    text_foreground = []

def generate_word():                #generates a word to be guessed by the user
    file = open ("{}/words.txt".format(file_dir),"r")
    words = file.readlines()
    word = words[randint(0, len(words) - 1)]
    
    return word[0:len(word) - 1].upper()

def color_fill(color, x, y):                #create a color box in the inputted x and y values
    global display_sprite   
    if color == "GREEN":
        green_sqaure = game_engine.properties_object("green_sqaure", f"{file_dir}/textures/green_square.png",x, y, 50, 50, False)
        display_sprite += [green_sqaure]

    elif color == "YELLOW":
        yellow_square = game_engine.properties_object("yellow_square", f"{file_dir}/textures/yellow_square.png",x, y, 50, 50, False)
        display_sprite += [yellow_square]
        
    elif color == "GREY":
        grey_sqaure = game_engine.properties_object("grey_sqaure", f"{file_dir}/textures/grey_square.png",x, y, 50, 50, False)
        display_sprite += [grey_sqaure]
        
def letter_check(inputted_word, index):           #requires a letter to be inputted and the current index, depending on its index, it can be g, y, g
    yellow = False
    if inputted_word[index] == word[index]:
        color_fill("GREEN", (60 * index) + 10, (60 * number_words) + 10)
    else:

        for gen_index in range(len(word)):
            if word[gen_index] == inputted_word[index]:
                yellow = True
        
        if yellow:
            color_fill("YELLOW", (60 * index) + 10, (60 * number_words) + 10)
        else:
            color_fill("GREY", (60 * index) + 10, (60 * number_words) + 10)

def letter_fill(inputted_word):          #fills the squares with the letters inputted by the user.
    global foreground
    for x in range(5):
        letter = game_engine.properties_text("letter", f"{inputted_word[x]}", "white", (60 * x) + 25, (60 * number_words) + 25, 30)
        foreground += [letter]
    
#main
def main(events):
    global text_foreground
    global number_letters, inputted_word, number_words       

    if not keys[pygame.K_BACKSPACE]:
        for event in events:
            if event.type == pygame.KEYDOWN and number_letters <= 4:
                pygame.time.delay(80)           #pause for 80ms
                input_text = game_engine.properties_text("input", event.unicode.upper(), "white", (number_letters * 20) + 10, h - 30, 30)
                number_letters += 1
                text_foreground += [input_text]
                inputted_word += event.unicode.upper()

    else:
        if not number_letters <= 0:         #not to backspace if the number of letters is not less than or equal to 0
            pygame.time.delay(80)
            number_letters -= 1
            del text_foreground[len(text_foreground) - 1]
            inputted_word = inputted_word[:-1]

    if number_words == 6:
        try_again = game_engine.properties_text("try_again", "Try again! The word was:", "RED", w, h, 30, True)
        generated_word = game_engine.properties_text("gen_word", word, "RED", w, h + 80, 45, True)
        text_foreground += [try_again, generated_word]
        update(display, display_sprite, foreground, text_foreground)
        pygame.time.delay(1000)         #pause for 100ms
        reset_game()

    if keys[pygame.K_RETURN] and number_letters == 5 and number_words <= 5:
        pygame.time.delay(80)
        letter_fill(inputted_word)
        for index in range(len(inputted_word)):
            letter_check(inputted_word, index)
        number_words += 1
        #check if the inputted word is the generated word
        if inputted_word == word:
            winText = game_engine.properties_text("win", "Guessed Correctly!", "RED", w, h, 45, True)
            text_foreground += [winText]
            update(display, display_sprite, foreground, text_foreground)
            pygame.time.delay(1000)
            reset_game()
        inputted_word = ""
        text_foreground = []
        number_letters = 0

reset_game()
while run:
    # keyboard and exit button, main code -----------------------------
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    
    main(events)
    update(display, display_sprite, foreground, text_foreground)
    clock.tick(60)
pygame.quit()
print("Quiting...")