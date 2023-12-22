import turtle as t
import random

t.hideturtle()
lettersEDGE = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'N', 'O', 'P', 'Q', 'R', 'S', 'U', 'V', 'W', 'X']
lettersCORNERS = ['B', 'C', 'D','F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'S', 'U', 'V', 'W', 'X']

def edge(piece):
    if piece == "A":
        colour = "white"
        colour2 = "blue"
    elif piece == "C":
        colour = "white"
        colour2 = "green"
    elif piece == "D":
        colour = "white"
        colour2 = "orange"
    elif piece == "E":
        colour = "orange"
        colour2 = "white"
    elif piece == "F":
        colour = "orange"
        colour2 = "green"
    elif piece == "G":
        colour = "orange"
        colour2 = "yellow"
    elif piece == "H":
        colour = "orange"
        colour2 = "blue"
    elif piece == "I":
        colour = "green"
        colour2 = "white"
    elif piece == "J":
        colour = "green"
        colour2 = "red"
    elif piece == "K":
        colour = "green"
        colour2 = "yellow"
    elif piece == "L":
        colour = "green"
        colour2 = "orange"
    elif piece == "N":
        colour = "red"
        colour2 = "blue"
    elif piece == "O":
        colour = "red"
        colour2 = "yellow"
    elif piece == "P":
        colour = "red"
        colour2 = "green"
    elif piece == "Q":
        colour = "blue"
        colour2 = "white"
    elif piece == "R":
        colour = "blue"
        colour2 = "orange"
    elif piece == "S":
        colour = "blue"
        colour2 = "yellow"
    elif piece == "T":
        colour = "blue"
        colour2 = "red"
    elif piece == "U":
        colour = "yellow"
        colour2 = "green"
    elif piece == "V":
        colour = "yellow"
        colour2 = "red"
    elif piece == "W":
        colour = "yellow"
        colour2 = "blue"
    else:
        colour = "yellow"
        colour2 = "orange"
        
    t.fillcolor(colour)
    t.begin_fill()
    for i in range (4):
        t.forward(100)
        t.left(90)
    t.end_fill()
    t.left(90)
    t.penup()
    t.setpos(100 , -120)
    t.pendown()
    t.fillcolor(colour2)
    t.begin_fill()
    for i in range(4):
        t.forward(100)
        t.left(90)
    t.end_fill()

lettersCORNERS = ['B', 'C', 'D', 'BUFFER E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'BUFFER R', 'T', 'S', 'U', 'V', 'W', 'X']

def corner(piece):
    if piece == "B":
        colour = "white"
        colour2 = "red"
        colour3 = "blue"
    elif piece == "C":
        colour = "white"
        colour2 = "green"
        colour3 = "red"
    elif piece == "D":
        colour = "white"
        colour2 = "orange"
        colour3 = "green"
    elif piece == "F":
        colour = "orange"
        colour2 = "green"
        colour3 = "white"
    elif piece == "G":
        colour = "orange"
        colour2 = "yellow"
        colour3 = "green"
    elif piece == "H":
        colour = "orange"
        colour2 = "blue"
        colour3 = "yellow"
    elif piece == "I":
        colour = "green"
        colour2 = "white"
        colour3 = "orange"
    elif piece == "J":
        colour = "green"
        colour2 = "red"
        colour3 = "white"
    elif piece == "K":
        colour = "green"
        colour2 = "yellow"
        colour3 = "red"
    elif piece == "L":
        colour = "green"
        colour2 = "orange"
        colour3 = "yellow"
    elif piece == "M":
        colour = "red"
        colour2 = "white"
        colour3 = "green"
    elif piece == "N":
        colour = "red"
        colour2 = "blue"
        colour3 = "white"
    elif piece == "O":
        colour = "red"
        colour2 = "yellow"
        colour3 = "blue"
    elif piece == "P":
        colour = "red"
        colour2 = "green"
        colour3 = "yellow"
    elif piece == "Q":
        colour = "blue"
        colour2 = "white"
        colour3 = "red"
    elif piece == "S":
        colour = "blue"
        colour2 = "yellow"
        colour3 = "orange"
    elif piece == "T":
        colour = "blue"
        colour2 = "red"
        colour3 = "yellow"
    elif piece == "U":
        colour = "yellow"
        colour2 = "green"
        colour3 = "orange"
    elif piece == "V":
        colour = "yellow"
        colour2 = "red"
        colour3 = "green"
    elif piece == "W":
        colour = "yellow"
        colour2 = "blue"
        colour3 = "red"
    else:
        colour = "yellow"
        colour2 = "orange"
        colour3 = "blue"
    t.fillcolor(colour)
    t.begin_fill()
    for i in range (4):
        t.forward(100)
        t.left(90)
    t.end_fill()
    t.left(90)
    t.penup()
    t.setpos(50 , -120)
    t.pendown()
    t.fillcolor(colour2)
    t.begin_fill()
    for i in range(4):
        t.forward(100)
        t.left(90)
    t.end_fill()
    t.left(-90)
    t.penup()
    t.setpos(70, -120)
    t.pendown()
    t.fillcolor(colour3)
    t.begin_fill()
    for i in range(4):
        t.forward(100)
        t.left(90)
    t.end_fill()
        
        


Input = input("(E)dge or (C)orners memo?")

while Input != "":
    if Input == "E":
        while True:
            piece = random.choice(lettersEDGE)
            t.reset()
            t.tracer(0,0)
            edge(piece)
            t.update()
            Ask = input("what is the name of this piece?")
            if Ask == piece:
                t.reset()
            else:
                print("that piece was ", piece)
    elif Input == "C":
        while True:
            piece = random.choice(lettersCORNERS)
            t.reset()
            t.tracer(0,0)
            corner(piece)
            t.update()
            Ask = input("what is the name of this piece?")
            if Ask == piece:
                t.reset()
            else:
                print("that piece was ", piece)
    else:
        Input = input("invalid input, try again")
        
        
        
