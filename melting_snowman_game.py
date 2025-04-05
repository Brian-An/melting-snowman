import pygame
import random

# Initialize Pygame
pygame.init()

# Define color constants
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED   = (255,0, 0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
LIGHT_BLUE = (102,255,255)
GREY = (128,128,128)

# Define font styles
btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
main_screen_font = pygame.font.SysFont("monospace", 30)
clue_font = pygame.font.SysFont("monospace", 16)

# Load sounds and images for game
wrong = pygame.mixer.Sound('assets/sound/wrong.ogg')
correct = pygame.mixer.Sound('assets/sound/correct.ogg')
winner = pygame.mixer.Sound('assets/sound/winner.ogg')
gameover = pygame.mixer.Sound('assets/sound/gameover.ogg')
correct_image1 = pygame.transform.scale(pygame.image.load('assets/YAY.png'),(125,125))

# List of category buttons with their positions and labels
catButtons = [[(54, 200, 160, 80), 'Geography'], 
              [(271, 200, 160, 80), 'Science'], 
              [(486, 200, 160, 80), 'Food']]

# Load surfaces and texts for different screens
wonSurface = guess_font.render("YOU WIN!", True, BLACK)
lostSurface = guess_font.render("YOU LOST!", True, BLACK)
game_title = main_screen_font.render('MELTING SNOWMAN GAME!!', True, BLACK)
play_again = guess_font.render('PRESS S TO GO TO START', True, BLACK)
quit_game = guess_font.render('PRESS Q TO QUIT', True, BLACK)
same_cat = guess_font.render('PRESS P TO PLAY', True, BLACK)
same_cat2 = guess_font.render('WITH SAME CATEGORY', True, BLACK)
over = main_screen_font.render('GOOD JOB!! THANKS FOR PLAYING!', True, WHITE)
over2 = main_screen_font.render('Thanks for playing!', True, WHITE)
leave = main_screen_font.render('Click ESC to leave', True, WHITE)

# Define the current screen
currentScreen = 1

# List to store used letters and used puzzles
used_letters = []
usedPuzz = []

# Initialize game window
win = pygame.display.set_mode((700,480))
pygame.display.set_caption('Melting Snowman Game')

# Initializes variable to control the main game loop.
inPlay = True

# Function that redraws all objects in the game window
def redraw_game_window():
    if currentScreen == 1:
        win.fill(LIGHT_BLUE)
        win.blit(game_title, (20,60))
        drawCatagoryButtons(catButtons)
    elif currentScreen == 2:
        win.fill(LIGHT_BLUE)
        drawButtons(buttons)
        win.blit(smImages[wrongCount],(175,50))
        drawGuess() 
        if wrongCount == 8:
            win.blit(lostSurface,(220,8))
            win.blit(play_again,(10,50))
            win.blit(quit_game,(10,90))
            win.blit(same_cat, (10,130))
            win.blit(same_cat2, (10, 150))
        elif puzzle == guess:
            win.blit(wonSurface,(220,8))
            win.blit(play_again,(10,50))
            win.blit(quit_game,(10,90))
            win.blit(same_cat, (10,130))
            win.blit(same_cat2, (10, 145))
    elif currentScreen == 3:
        win.fill(BLUE)
        win.blit(over, (50, 100))
        win.blit(over2, (100, 200))
        win.blit(leave, (150, 300))
    pygame.display.update()

# Function to create the letter buttons on the game screen
def createButtons():
    x = 98
    y = 400
    buttons = []
    for btn in range(26):
        buttons.append((x, y))
        x += 42
        if btn == 12:
            x = 98
            y += 42
    return buttons

# Function to draw the letter buttons on the game screen
# and checks weather the button is clicked or not and changes
# colours if it was hovered over or clicked on
def drawButtons(buttons):
    mousePos = pygame.mouse.get_pos()
    for i, xy in enumerate(buttons):
        ltrToRender = chr(i + 65)
        a = mousePos[0] - xy[0]
        b = mousePos[1] - xy[1]
        c = (a**2 + b**2) ** 0.5
        if c <= 15:
            btn_colour = BLUE
        else:
            btn_colour = WHITE
            
            if ltrToRender in used_letters:
                btn_colour = GREY
            else:
                btn_colour = WHITE

        pygame.draw.circle(win, btn_colour, xy, 15, 0)
        pygame.draw.circle(win, BLACK, xy, 15, 1)
        ltrSurface = btn_font.render(ltrToRender, True, BLACK)
        win.blit(ltrSurface, (xy[0]-ltrSurface.get_width()//2,xy[1]-ltrSurface.get_height()//2))

# Function to handle button click events
def clickBtn(mp, buttons):
    for i,xy in enumerate(buttons):
        a = mp[0] - xy[0]
        b = mp[1] - xy[1]
        c = (a**2 + b**2)**.5
        if c <= 15:
            used_letters.append(chr(i + 65))
            return i
    return -1

# Function to load snowman images in the game window
def loadSnowmanImages():
    smImages = []
    for imgNum in range(9):
        fileName = 'snowman' + str(imgNum) + '.png'
        smImages.append(pygame.image.load('assets/snowman/' + fileName))
    return smImages

# Function to load puzzles from a file
def loadPuzzles():
    puzzles = [[], [], []]
    fi = open('assets/puzzles.txt', 'r')
    for p in fi:
        puz = p.strip().split(',')
        catIndex = int(puz[0]) - 1
        puzzles[catIndex].append(puz[1:])
    fi.close()
    return puzzles

# Function to get a random puzzle from the given category
def getRandomPuzzle(cat,puzzles):
    pIndex = random.randrange (0, len(puzzles[cat]))
    while True:
        if pIndex in usedPuzz:
            pIndex = random.randrange(0, len(puzzles[cat]))
        else:
            break
    usedPuzz.append(pIndex)
   
    randomPuz = puzzles[cat][pIndex]
    return randomPuz

# Function to initialize the guess string for the puzzle
def initializeGuess(puzzle):
    guess = ''
    for c in puzzle:
        if c == ' ':
            guess += ' '
        else:
            guess += '_'
    return guess

# Function to draw the current guess on the game screen
def drawGuess():
    guessSurface = guess_font.render(spacedOut(guess), True, BLACK)
    x = (win.get_width() - guessSurface.get_width()) // 2
    win.blit(guessSurface, (x, 310))
    clueSurface = clue_font.render(clue, True, BLACK)
    x = (win.get_width() - clueSurface.get_width()) // 2
    win.blit(clueSurface, (x, 340))

# Function to add spaces between characters in the guess string
def spacedOut(guess):
    newGuess = ''
    for i in guess:
        newGuess += i + ' '
    return newGuess[:-1]

# Function to update the guess string with the correctly guessed letter
def updateGuess(ltrGuess, guess, puzzle):
    newGuess = ''
    for i, ltr in enumerate(puzzle):
        if ltrGuess == ltr:
            newGuess += ltr
        else:
            newGuess += guess[i]
    return newGuess

# Function to draw category buttons on the game screen
# and changes the colour if it is hovered over
def drawCatagoryButtons(catButtons):
    catMousePos = pygame.mouse.get_pos()
    for b in catButtons:
        if pygame.Rect(b[0]).collidepoint(catMousePos):
            catBtncolour = GREY
            pygame.draw.rect(win, catBtncolour, b[0], 0)
            pygame.draw.rect(win, RED, b[0], 3)
            txtSurface = btn_font.render(b[1], True, WHITE)
            x = b[0][0] + (b[0][2] - txtSurface.get_width()) // 2
            y = b[0][1] + (b[0][3] - txtSurface.get_height()) // 2
            win.blit(txtSurface, (x, y))
        else:
            catBtncolour = BLUE
            pygame.draw.rect(win, catBtncolour, b[0], 0)
            pygame.draw.rect(win, RED, b[0], 3)
            txtSurface = btn_font.render(b[1], True, WHITE)
            x = b[0][0] + (b[0][2] - txtSurface.get_width()) // 2
            y = b[0][1] + (b[0][3] - txtSurface.get_height()) // 2
            win.blit(txtSurface, (x, y))

# Function to handle category button click events
def catBtnClick(mp, buttons):
    for i, b in enumerate(buttons):
        if pygame.Rect(b[0]).collidepoint(mp):
            return i
    return -1


while inPlay:
    redraw_game_window() # Updates game continously
    pygame.time.delay(10) # pause for 10 milliseconds
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # If user clicks "x" on the top right
            inPlay = False                  # it quits the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:    # If user clicks "ESC" it quits the game
                inPlay = False
            if event.key == pygame.K_q:         # If the user clicks "Q" it quits the game
                inPlay = False
            if event.key == pygame.K_s:         # If the user clicks "S" it goes to the start menu
                usedPuzz.clear()                # and resets the variables to the original values
                wrongCount = 0
                currentScreen = 1                     
                buttons = createButtons()
                smImages = loadSnowmanImages()
                puzzles = loadPuzzles()
                randomPuz = getRandomPuzzle(cat,puzzles)
                puzzle = randomPuz[0]
                clue = randomPuz[1]
                used_letters = []
                guess = initializeGuess(puzzle)
            if event.key == pygame.K_p:                 # If the user clicks "P", it continues the game in the same
                wrongCount = 0                          # category and resets some of the variables
                buttons = createButtons()
                smImages = loadSnowmanImages()
                puzzles = loadPuzzles()
                randomPuz = getRandomPuzzle(cat,puzzles)
                puzzle = randomPuz[0]
                clue = randomPuz[1]
                used_letters = []
                guess = initializeGuess(puzzle)   
            
        if event.type == pygame.MOUSEBUTTONDOWN:       # Determines the mouse positions when clicked on the game window
            clickPos = pygame.mouse.get_pos()       

            if currentScreen == 1:                          # if the user is in the main menu,
                cat = catBtnClick(clickPos, catButtons)     # it will see which category they clicked on
                if cat != -1:                               
                    currentScreen = 2
                    buttons = createButtons()
                    smImages = loadSnowmanImages()
                    puzzles = loadPuzzles()
                    randomPuz = getRandomPuzzle(cat,puzzles)
                    puzzle = randomPuz[0]
                    clue = randomPuz[1]
                    used_letters = []
                    guess = initializeGuess(puzzle)
                    wrongCount = 0

            elif currentScreen == 2:                                # if the user is in the game screen and clicked a button
                if clickBtn(clickPos, buttons) != -1:               # it determines the button clicked and changes it to a letter
                    letter = chr(clickBtn(clickPos,buttons)+65)
                    used_letters.append(letter)

                    if letter in puzzle:                            
                        guess = updateGuess(letter,guess,puzzle)    # if the letter is correct, it will update the guess
                        correct.play()                              # play the sound
                        win.blit(correct_image1,(180,25))           # show a image on the coordinate
                        pygame.display.update()                     # update the display
                        pygame.time.wait(500)                       # and waits 500 milliseconds
                        
                    else:                  # if the guess is wrong, it will add 1 to wrongCount 
                        wrongCount += 1    # and play a sound
                        wrong.play()

                    if wrongCount == 8:                 # if they use all the guesses, it will play a sound 
                        gameover.play()
                        if len(usedPuzz) == 6:          # if you run out of puzzles, it will wait 300 milliseconds
                            pygame.time.wait(300)       # and change screens to the end screen
                            currentScreen = 3
                         
                    elif guess == puzzle:               # if the word is guessed, a sond is played
                        winner.play()
                        if len(usedPuzz) == 6:          # and it waits 300 milliseconds and goes to the end screen
                            pygame.time.wait(300)
                            currentScreen = 3

    pygame.display.update()     #updates the display
                                        
pygame.quit()       # pygame quits when it is done