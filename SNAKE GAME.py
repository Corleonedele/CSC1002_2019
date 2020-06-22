# import the necessary module
import turtle
import random

welcomeWords = """      Welcome to the SNAKE game 
        click to begin this game
        use for arrow keys to control the movement of snake
        eat all the foods --- WIN
        eaten by monster --- LOSE
        hope you enjoy"""


# define global variables
screen = turtle.Screen()
welcomePen = turtle.Turtle()
boundryPen = turtle.Turtle()
snake = turtle.Turtle()
monster = turtle.Turtle()
foodPen = turtle.Turtle()
grassPen = turtle.Turtle()
food = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
contract = 0 # number of contract
time = 0
foodLength = 0
bodyLength = 5
snakePosition = (0, 0)
monsterPosition = (0, 0)
direction = (0, 1)
grass = []
foodPosition = []
bodyPositions = []
win = None
state = False
screen.mode("standard")
grid = [(i, j) for i in range(-12, 13) for j in range(-12, 13)]
initFoodPosition = [(i, j) for i in range(-11, 12) for j in range(-11, 12)]
initMonsterPosition = [(i, j) for i in range(-11, 12) for j in range(-11, -4)]

def drawBoundary():
    """ a function to draw the boundry"""
    boundryPen.speed(0)
    boundryPen.goto(-250, 250)
    boundryPen.pendown()
    for i in range(4):
        boundryPen.forward(500)
        boundryPen.right(90)

def setUpInterface():
    """ set the basic game interface and the basic setting of pens"""
    screen.setup(width = 600, height = 600)
    screen.title('THE SNAKE')
    for pen in [welcomePen, boundryPen, foodPen]:
        pen.hideturtle()
        pen.up()
        pen.speed(0)
    for pen in snake, monster, grassPen:
        pen.shape("square")
        pen.penup()
        pen.speed(0)
    snake.color("red")
    monster.color("purple")
    grassPen.color("green")
    drawBoundary()

def initGame():
    """ randomly set the satisfied position of monster"""
    global monsterPosition
    monsterPosition = random.choice(initMonsterPosition)
    monster.goto(monsterPosition[0] * 20 + 10, monsterPosition[1] * 20 + 10)

def welcome(begin):
    """ a function to write the introduction of the game"""
    welcomePen.goto(-25, 75)
    welcomePen.write(welcomeWords, align = "center", font = ("Arial", 14, "normal"))
    screen.onclick(begin)

def start(x, y):
    """ a function to set the food and memorize its position"""
    global foodPosition, initFoodPosition
    welcomePen.clear()
    for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]: # avoid the food in home position
        initFoodPosition.remove(i)
    for f in food: # draw the food one by one
        pos = random.choice(initFoodPosition)
        foodPosition.append(pos)        
        foodPen.goto(pos[0] * 20 + 10, pos[1] * 20)
        foodPen.write(f, align = "center", font = ("Arial", 16, "normal"))
        initFoodPosition.remove(pos)
    for g in range(8):
        pos = random.choice(initFoodPosition)
        grass.append(pos)
        grassPen.goto(pos[0] * 20, pos[1] * 20)
        grassPen.stamp()
        grid.remove(pos)
    defineControlKeys()
    runGame()

def refreshGame():
    """ refresh game and check if already win or lose"""
    screen.title("Snake:  Contract:{}, Time:{}".format(contract, time))
    checkCollision()

def checkWin():
    """ check if game win"""
    global win
    if len(set(food)) == 1:
        win = True
        snake.write("Winner!!!", align = "center", font = ("Arial", 16, "normal"))

def checkCollision():
    """ check if game lose"""
    global win
    if monsterPosition in [(snakePosition[0], snakePosition[1]), (snakePosition[0] - 1, snakePosition[1]),
    (snakePosition[0], snakePosition[1] - 1), (snakePosition[0] - 1, snakePosition[1] - 1)]:
        win = False
        snake.write("Game over!!", align = "center", font = ("Arial", 16, "normal"))

def checkContact():
    """ check if monster contacts with the snake body"""
    global contract
    body = []
    for b in bodyPositions:
        body += [(b[0], b[1]), (b[0] - 1,b[1]), 
        (b[0], b[1] - 1), (b[0] - 1, b[1] - 1)]
    body = set(body)
    if  monsterPosition in body:
        contract += 1

def checkEat():
    """ check if snake eat the food"""
    global food, foodPosition, foodLength, bodyLength
    for index, i in enumerate(food):
        f = foodPosition[index]
        if i == "0":
            continue
        if snakePosition in [(f[0], f[1]), (f[0] + 1, f[1]),(f[0], f[1] + 1), (f[0] + 1, f[1] + 1)]:
            foodLength = int(i)
            food[index] = "0"
            foodPen.clear()
            drawFood()
            bodyLength += foodLength # chenge the body length of snake

def checkEating():
    """check if snake eating or not and judge if it needs to cut the last trail"""
    global bodyPositions
    if len(bodyPositions) > bodyLength:
        snake.clearstamps(1)
        bodyPositions.pop(0)

def drawFood():
    """ a function to draw all the food again"""
    global food
    for index, i in enumerate(food):
        if i != "0":
            foodPen.goto(foodPosition[index][0] * 20 + 10, foodPosition[index][1] * 20)
            foodPen.write(food[index], align = "center", font = ("Arial", 16, "normal"))

def timeGoes():
    """ start the time indices"""
    global time
    if win is None:
        time += 1
        refreshGame()
        screen.ontimer(timeGoes, 1000)

def snakeGoes():
    """ start the snake move"""
    if win is None and state is False:
        moveSnake()
        refreshGame()
    if len(bodyPositions) == bodyLength: # check if snake is eating, if is, slow down, else return normal speed
        checkWin()
        screen.ontimer(snakeGoes, 500)
    else:
        screen.ontimer(snakeGoes, 730)

def monsterGoes():
    """ start the monster move"""
    if win is None:
        track()
        checkContact()
        refreshGame()
        screen.ontimer(monsterGoes, 800 + random.randint(-150, 150)) # to get random speed for monster

def moveSnake():
    """ a function to control the move of snake, also includes the solution of eaten"""
    global snakePosition, bodyPositions, foodLength
    if (snakePosition[0] + direction[0], snakePosition[1] + direction[1]) in grid:
        bodyPositions.append(snakePosition)
        checkEat() # check if snake eat something
        movement()
        checkEating() # if snake is eating, we don't clear the last body, if not, clear it

def track():
    """ control the monster to track the snake"""
    global monsterPosition, snakePosition
    if abs(snakePosition[0] - monsterPosition[0]) <= abs(snakePosition[1] - monsterPosition[1]):
        if snakePosition[1] <= monsterPosition[1]:
            monsterPosition = (monsterPosition[0], monsterPosition[1] - 1)
        else: 
            monsterPosition = (monsterPosition[0], monsterPosition[1] + 1)
    else:
        if snakePosition[0] <= monsterPosition[0]:
            monsterPosition = (monsterPosition[0] - 1, monsterPosition[1])
        else: 
            monsterPosition = (monsterPosition[0] + 1, monsterPosition[1])
    monster.goto(monsterPosition[0] * 20 + 10, monsterPosition[1] * 20 + 10)

def movement():
    """ a funtion to control the movement of snake"""
    global snakePosition
    snake.color("blue","black")
    snake.stamp()
    snake.color("red")
    snakePosition = (snakePosition[0] + direction[0], snakePosition[1] + direction[1])
    snake.goto(snakePosition[0] * 20, snakePosition[1] * 20)

## four functions to set the four directions of snake
def moveUp():
    global direction
    direction = (0, 1)

def moveDown():
    global direction
    direction = (0, -1)

def moveLeft():
    global direction
    direction = (-1, 0)

def moveRight():
    global direction
    direction = (1, 0)

def pause():
    """ change the state of snake"""
    global state
    state = not state # chenge the state into opposite bool

def defineControlKeys():
    """ binding the keys with corresponding movement"""
    screen.onkey(moveUp, "Up")
    screen.onkey(moveDown, "Down")
    screen.onkey(moveRight, "Right")
    screen.onkey(moveLeft, "Left")
    screen.onkey(pause, "space")
    screen.listen()

def runGame():
    """ run the game"""
    timeGoes()
    snakeGoes()
    monsterGoes()

def drawGrid():
    peng = turtle.Turtle()
    peng.speed(0)
    peng.up()
    peng.goto(-250, -250)
    peng.right(270)
    for i in range(-12,14):
        peng.goto(i*20-10,-250)
        peng.down()
        peng.forward(500)
        peng.up()
    peng.left(270)
    peng.goto(-250, 250)
    for i in range(-12,14):
        peng.goto(-250,i*20-10)
        peng.down()
        peng.forward(500)
        peng.up()
    peng.home()
    peng.hideturtle()
    screen.update()

def main():
    setUpInterface()
    initGame()
    # drawGrid()
    welcome(start)
    screen.mainloop()

if __name__ == "__main__":
    main()

