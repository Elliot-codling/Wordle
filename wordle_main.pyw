#wordle by Elliot Codling
import pygame, os, random
from engine import game_engine_000 as game_engine
file_dir = os.getcwd() + "" # get the current directory    
pygame.font.init()


# create window ---------------------------------
w, h = 310, 400
window = game_engine.update.define("Wordle", w, h)

# -----------------------------------------------
#create variable stuff
clock = pygame.time.Clock()


# functions ----------------------------------------------------------
def reset_screen():
    #background
    global display, display_sprite, foreground, text_foreground, font, green_texture, yellow_texture, grey_texture
    display = []
    color = (255, 0, 255)
    background_texture = pygame.image.load("{}/textures/black_bg.jpg".format(file_dir))
    background = game_engine.properties_object("background", background_texture, 0, 0, w, h, False)

    green_texture = pygame.image.load("{}/textures/green_square.png".format(file_dir))
    yellow_texture = pygame.image.load("{}/textures/yellow_square.png".format(file_dir))
    grey_texture = pygame.image.load("{}/textures/grey_square.png".format(file_dir))

    display += [background]

    #display sprites
    display_sprite = []
    square_texture = pygame.image.load("{}/textures/square_box.png".format(file_dir))


    #create a 5 x 6 squares
    for x in range(1, 6):
        for y in range(1, 7):
            square = game_engine.properties_object("sqaure{}{}".format(x, y), square_texture, 60*x-50, 60*y-50, square_size, square_size, True)
            display_sprite += [square]
    #foreground
    foreground = []


    #text_foreground
    text_foreground = []
    font = pygame.font.SysFont(None, 30)

    start_text_texture = font.render(": ", True, pygame.Color("WHITE"))
    start_text = game_engine.properties_text("input_start", start_text_texture, 10, 370)
    text_foreground += [start_text]

        
def generate_word():
    file = open ("{}/words.txt".format(file_dir),"r")
    words = file.readlines()
    word = words[random.randint(0, len(words) - 1)]
    
    return word[0:len(word) - 1]

def update(window, display, display_sprite, foreground, text_foreground, clock, debug):                    #update the screen
    game_engine.update.window(window, display, display_sprite, foreground, text_foreground, clock, debug)


def color_fill(letter, color, x, y, display, foreground):
    if color == "GREEN":
        #colour in green
        green_square = game_engine.properties_object("green_square{}{}".format(x, y), green_texture, x, y, square_size, square_size, True)
        
        display += [green_square]
        
    elif color == "YELLOW":
        #colour in yellow
        yellow_square = game_engine.properties_object("yellow_square", yellow_texture, x, y, square_size, square_size, True)
        
        display += [yellow_square]
    elif color == "GREY":
        #colour in yellow
        grey_square = game_engine.properties_object("grey_square", grey_texture, x, y, square_size, square_size, True)
        
        display += [grey_square]

    letter_texture = font.render("{}".format(letter), True, pygame.Color("WHITE"))
    letter = game_engine.properties_text("letter{}".format(letter), letter_texture, x, y)
    foreground += [letter]

    return display, foreground
    


def yellow_grey(index, letter, generated_word, number_words, display, foreground):
    yellow = False
    x = (index+1) * 60 - 50
    y = 60*number_words-50
    for gen_index in range(len(generated_word)):
        if generated_word[gen_index] == letter:
            yellow = True
            
            display, foreground = color_fill(letter, "YELLOW", x, y, display, foreground)
                     #colour yellow
    if not yellow:
        display, foreground = color_fill(letter, "GREY", x, y, display, foreground)
                    #colour grey

    return display, foreground

def green_check(index, letter, generated_word, number_words, display, foreground):
    x = (index+1) * 60 - 50
    y = 60*number_words-50
    if letter == generated_word[index]:
        
        display, foreground = color_fill(letter, "GREEN", x, y, display, foreground)
        
    else:
        display, foreground = yellow_grey(index, letter, generated_word, number_words, display, foreground)

    return display, foreground


def game_reset():
    global display, display_sprite, foreground, text_foreground, x_multiplier, font, number_words, number_letters, inputted_word, word, square_size, x_multiplier
    display = []
    display_sprite = []
    foreground = []
    text_foreground = []
    word = generate_word().upper()

    number_letters = 0      #number of letters printed
    inputted_word = ""
    number_words = 0
    square_size = 50
    x_multiplier = 20     #position of inputted letters

# main game code -------------------------------------------------------

def main_game(events):
    global display, display_sprite, foreground, text_foreground, x_multiplier, font, number_words, number_letters, inputted_word, word
    #print out "try again"
    if number_words == 6:
        #text
        font = pygame.font.SysFont(None, 60)
        end_texture = font.render("Try again!".format(word), True, pygame.Color("RED"))
        text_rect = end_texture.get_rect(center=(w / 2, h / 2))
        end_text = game_engine.properties_text("end_text", end_texture, text_rect[0], text_rect[1])
        text_foreground += [end_text]
        #update
        update(window, display, display_sprite, foreground, text_foreground, clock, 0)     #update the window

        #reset
        font = pygame.font.SysFont(None, 30)
        pygame.time.delay(1000)

        game_reset()
        reset_screen()

    
    if keys[pygame.K_RETURN]:           #enter the inputted letters
        if number_letters == 5:
            number_words += 1
            for input_index in range(5):        #check each letter
                display, foreground = green_check(input_index, inputted_word[input_index], word, number_words, display, foreground)

            pygame.time.delay(80)       #wait 80 miliseconds

        #winning
        if str(inputted_word) == str(word):
            #text
            font = pygame.font.SysFont(None, 45)
            win_texture = font.render("Guessed Correctly!".format(word), True, pygame.Color("RED"))
            text_rect = win_texture.get_rect(center=(w / 2, h / 2))
            win_text = game_engine.properties_text("win_text", win_texture, text_rect[0], text_rect[1])
            text_foreground += [win_text]

            #update
            update(window, display, display_sprite, foreground, text_foreground, clock, 0)     #update the window

            #reset
            font = pygame.font.SysFont(None, 30)
            pygame.time.delay(1000)

            game_reset()
            reset_screen()
        
    else:
        
        if not keys[pygame.K_BACKSPACE]:        #if backspace isnt pressed, continue with this code
            #input letters
            for event in events:
                if event.type == pygame.KEYDOWN and number_letters <= 4:            
                    pygame.time.delay(80)       #wait 80 miliseconds

                    text_texture = font.render("{}".format(event.unicode.upper()), True, pygame.Color("WHITE"))
                    input_text = game_engine.properties_text("input", text_texture, x_multiplier, 370)

                    x_multiplier += 20
                    number_letters += 1
                    text_foreground += [input_text]
                    inputted_word += event.unicode.upper()
                    
                
                
        #backspace
        else:
            if not number_letters <= 0:     #backspace if no. letters is greater than 0 
                pygame.time.delay(80)       #wait 80 miliseconds
                x_multiplier -= 20
                number_letters -= 1
                del text_foreground[len(text_foreground) - 1]       #delete from list
                inputted_word = inputted_word[:-1]          #delete from inputted word variable

    
game_reset()
reset_screen()

# main game loop ------------------------------------------------------------------
run = True
while run:
    # keyboard and exit button, main code -----------------------------
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    main_game(events)


    #exit
    if keys[pygame.K_ESCAPE]:
        run = False

    
    update(window, display, display_sprite, foreground, text_foreground, clock, 0)     #update the window
    clock.tick(30)

print("Quiting...")
pygame.quit()
