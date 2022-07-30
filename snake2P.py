import pygame, sys, random, time

"""TODO

Menu creation (DONE!!!!!)
-create title (done)
-create exit, newgame (done)
--create exit functionality, newgame opens game window (done)

Snake creation (DONE!!!!!!)
-create a snake that can move across the screen(done)
---mechanism of snake movement is, the snake has segments, when the player turns the snake, all the individual segments rotate in the direction moved by player when reaching the point where the head was when the player gave rotation input
-should despawn and show defeat screen when collides (done)
-should despawn and show defeat screen when collides with itself (done)

food pellets creation(DONE!!!!!)
-randomly generate food pellets on random unoccupied spots, one on the screen at any time (done)
-on being eaten by snake, snake should have size incremeted by one(done)

create two-player functionality(LONG TERM)(DONE!!!!)
- get a second snake on the board on the same time as the first snake, with its own seperate controls (done)
- get the snake to kill the other snake upon collision(done)

"""
#-->Game Constants

"""
Vampire Black (13, 2, 8)
Dark Green   (0, 59, 0)
Islamic green (0, 143, 17)
Malachite (0, 255, 65)
"""


FPS = 60
WIDTH = 512
HEIGHT = 512
TIMEGAP = 0.1
CUBE_LENGTH = 16
CENTER_X = WIDTH//2 +  (CUBE_LENGTH // 2)
CENTER_Y = HEIGHT//2 + (CUBE_LENGTH // 2)

#-->Game Booleans
game_start = True
menu_start = True

#--> initialization
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("snake")


#-->Color Values

BCG_COLOR = (0,0,0)
TITLE_COLOR = (0,255,0)
TITLE_BCG_COLOR = (214, 137, 16)
MENUBUTTON_COLOR = (0,255,0)
MENUBUTTON_BCG_COLOR = (214, 137, 16)
HIGHLIGHT_COLOR = (0, 59, 0)

RGB = [( 0, 0, 255), (0,255,0), (255, 0, 0)]

BODY1COLOR = ( 0, 0, 255)
HEAD1COLOR = ( 255, 0, 0)

BODY2COLOR = (255, 0, 0)
HEAD2COLOR = (0, 0, 255)

PELLETCOLOR = (0,255,0)

#-->Text Assets

FONTSIZE = 32
#------->fonts

# Corbel, Times New Roman, berlinsanafb
HEADER_FONT = pygame.font.SysFont("berlinsanafb", FONTSIZE*3)#heading font
NORMAL_FONT = pygame.font.SysFont("berlinsanafb", FONTSIZE)#font for everything else
#------->text used
TITLE_TEXT = HEADER_FONT.render("Snake", True, TITLE_COLOR)
EXIT_BUTTON_TEXT = NORMAL_FONT.render("Exit", True, MENUBUTTON_COLOR)
NEWGAME_BUTTON_TEXT = NORMAL_FONT.render("New Game", True, MENUBUTTON_COLOR)

#------->text class

class Text(): # class that encompasses anything with text, i.e a button or header or score
	def __init__(self, x, y, text, color, font):
		self.color = color
		self.font = font
		self.text = text
		self.textRender = font.render(text, True, color)
		self.rect = self.textRender.get_rect(center=(x,y))


	def drawText(self, event):
		mouseX, mouseY = pygame.mouse.get_pos() # coords of the mouse
		
		if self.rect.collidepoint((mouseX, mouseY)): # to see if the cursor is over the button
			self.textRender = self.font.render(self.text, True, HIGHLIGHT_COLOR)
			if event.type == 1025 and event.button == 1: # if it is a mouse button down, and the button is a left click
				return True

		else:
			self.textRender = self.font.render(self.text, True, self.color)
		
		screen.blit(self.textRender, self.rect)

#-------> pellets class

class Pellet():
	def __init__(self, color, on_screen):
		self.centerX, self.centerY = 0,0
		self.color = color
		self.on_screen = on_screen

	def pelletDraw(self):
		if self.on_screen:
			topLeftX, topLeftY = (self.centerX + (CUBE_LENGTH//2), self.centerY  + (CUBE_LENGTH//2))
			pygame.draw.rect(screen, self.color, [topLeftX, topLeftY , CUBE_LENGTH, CUBE_LENGTH]) #pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
		
		elif not self.on_screen:
			# (2 * (i) + 1) * (CUBE_LENGTH/ 2)
			
			noOfCubesX = WIDTH//CUBE_LENGTH - 1
			noOfCubesY = HEIGHT//CUBE_LENGTH - 1

			self.centerX = (2 * (random.randrange(noOfCubesX)) + 1) * (CUBE_LENGTH/ 2)
			self.centerY = (2 * (random.randrange(noOfCubesY)) + 1) * (CUBE_LENGTH/ 2)

			topLeftX, topLeftY = (self.centerX + (CUBE_LENGTH//2), self.centerY  + (CUBE_LENGTH//2))
			pygame.draw.rect(screen, self.color, [topLeftX, topLeftY , CUBE_LENGTH, CUBE_LENGTH]) #pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
			self.on_screen = True

		pygame.display.update()


#------->snake class

class Snake():
	def __init__(self, centerX, centerY, bodyColor, headColor, length, alive):
		self.bodyColor = bodyColor
		self.headColor = headColor
		self.length = length
		self.centerX =  [centerX for i in range(self.length)]
		self.centerY =  [(centerY - (i*CUBE_LENGTH)) for i in range(self.length)]
		self.direction = "down"
		self.alive = alive

	def snakeIncrement(self):

		self.length += 1

		if self.direction == "up":
			(self.centerX).append(self.centerX[-1])
			(self.centerY).append(self.centerY[-1] + CUBE_LENGTH)
		
		if self.direction == "down":
			(self.centerX).append(self.centerX[-1])
			(self.centerY).append(self.centerY[-1] - CUBE_LENGTH)
		
		if self.direction == "right":
			(self.centerX).append(self.centerX[-1] - CUBE_LENGTH)
			(self.centerY).append(self.centerY[-1])
		
		if self.direction == "left":
			(self.centerX).append(self.centerX[-1] + CUBE_LENGTH)
			(self.centerY).append(self.centerY[-1])
	
	def drawSnake(self):

		for i in range(self.length):
			topLeftX, topLeftY = (self.centerX[i] + (CUBE_LENGTH//2), self.centerY[i]  + (CUBE_LENGTH//2))
			if i == 0:
				pygame.draw.rect(screen, self.headColor, [topLeftX, topLeftY , CUBE_LENGTH, CUBE_LENGTH]) #pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
			else:
				pygame.draw.rect(screen, self.bodyColor, [topLeftX, topLeftY , CUBE_LENGTH, CUBE_LENGTH]) #pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
			
		pygame.display.update()
	
	def move(self): # moves the center depending on the direction of the head

		if self.alive: # dead snake no move

			for i in range(self.length-1, -1, -1): # for segment of the body

				if i != 0:
					self.centerY[i] = self.centerY[i-1]
					self.centerX[i] = self.centerX[i-1]

				if i == 0: # i.e the head of the snake

					if self.direction == "up":
						self.centerY[i] -= CUBE_LENGTH
						
					if self.direction == "down":
						self.centerY[i] += CUBE_LENGTH
					
					if self.direction == "left":
						self.centerX[i] -= CUBE_LENGTH
					
					if self.direction == "right":
						self.centerX[i] += CUBE_LENGTH	
					
			self.drawSnake()
 
	def headCollisions(self, pellet, enemy): # checks if the head collides with the pellet, snake, or border
		
		headRect = pygame.Rect( ((self.centerX[0] + (CUBE_LENGTH//2), self.centerY[0]  + (CUBE_LENGTH//2))) , (CUBE_LENGTH, CUBE_LENGTH) )		#   pygame.Rect((topleft coordinates), (width, height))
		pelletRect = pygame.Rect( ((pellet.centerX + (CUBE_LENGTH//2), pellet.centerY  + (CUBE_LENGTH//2))) , (CUBE_LENGTH, CUBE_LENGTH) )

		headRectTop = ( (self.centerX[0], self.centerY[0]  - (CUBE_LENGTH//2)) )
		headRectBottom = ( (self.centerX[0], self.centerY[0]  + (CUBE_LENGTH//2)) )

		# border collision for sides
		if headRect.right >= WIDTH + 5 or headRect.left <= -5: # checks if the left or the right parts of the head have collided with the borders  
			self.alive = False
			return True
		if headRect.top <= -5 or headRect.bottom >= HEIGHT + 5: # checks if the bottom or the top parts of the head have collided with the borders  
			self.alive = False
			return True

		# collision for snake body with head
		for i in range(self.length-1, 1, -1):
			bodySegmentRect = pygame.Rect( ((self.centerX[i] + (CUBE_LENGTH//2), self.centerY[i]  + (CUBE_LENGTH//2))) , (CUBE_LENGTH, CUBE_LENGTH) )
			
			if headRect.colliderect(bodySegmentRect):
				self.alive = False
				return True
		
		for i in range(enemy.length):
			enemyBodySegmentRect = pygame.Rect( ((enemy.centerX[i] + (CUBE_LENGTH//2), enemy.centerY[i]  + (CUBE_LENGTH//2))) , (CUBE_LENGTH, CUBE_LENGTH) )
			if headRect.colliderect(enemyBodySegmentRect):
				self.alive = False
				return True			
		
		if (abs(self.centerX[0] - pellet.centerX) < CUBE_LENGTH) and (abs(self.centerY[0] - pellet.centerY) < CUBE_LENGTH):
			pellet.on_screen = False
			self.snakeIncrement()


		return False


#-------->text instances

title = Text(CENTER_X, CENTER_Y - (HEIGHT//4), "Snake", TITLE_COLOR, HEADER_FONT)
exitButton = Text(CENTER_X , CENTER_Y, "Exit", MENUBUTTON_COLOR, NORMAL_FONT)
newgameButton = Text(CENTER_X , CENTER_Y - (HEIGHT//8), "New Game", MENUBUTTON_COLOR, NORMAL_FONT)

#--> mainGame

def menu():
	global menu_start, game_start
	while menu_start:
		screen.fill(BCG_COLOR)
		for event in pygame.event.get():			
			
			title.drawText(event)
			if exitButton.drawText(event):
				menu_start = False
				game_start = False
				return False
			
			if newgameButton.drawText(event):
				game_start = True
				menu_start = False
				return True
			
			if event.type == pygame.QUIT:
				menu_start = False
				game_start = False
				return False
		

			pygame.display.update()

def game():
	global menu_start, game_start
	if game_start:
		
		player1 = Snake(CENTER_X, CENTER_Y, BODY1COLOR, HEAD1COLOR, 1, True)
		player2 = Snake(CENTER_X - (CUBE_LENGTH*5), CENTER_Y - (CUBE_LENGTH*5), BODY2COLOR, HEAD2COLOR, 1, True)
		pellet1 = Pellet(PELLETCOLOR, False)
		
		screen = pygame.display.set_mode([WIDTH,HEIGHT])
		pygame.display.set_caption("snake")
		
		while game_start:
			clock.tick(120)
			for event in pygame.event.get():
				
				if event.type == pygame.KEYDOWN:
					
					# player1 movement

					if event.unicode == "w":
						player1.direction = "up"
					
					if event.unicode == "s":
						player1.direction = "down"					
					
					if event.unicode == "a":
						player1.direction = "left"
					
					if event.unicode == "d":
						player1.direction = "right"
					
					# player2 movement

					if event.key == pygame.K_UP:
						player2.direction = "up"
					
					if event.key == pygame.K_DOWN:
						player2.direction = "down"					
					
					if event.key == pygame.K_LEFT:
						player2.direction = "left"
					
					if event.key == pygame.K_RIGHT:
						player2.direction = "right"

				if event.type == pygame.QUIT: # exits the game
					game_start = False
					menu_start = False
					return False
			
			player1.headCollisions(pellet1, player2)
			player2.headCollisions(pellet1, player1)

			if (not player1.alive) and (not player2.alive): # if both players are dead, ends game
				game_start = False
				menu_start = True
				return True	
			
			screen.fill(BCG_COLOR)
			
			player1.move()
			player2.move()
			pellet1.pelletDraw()
			
			time.sleep(TIMEGAP)	
		
	

def main():
	running = True

	while running:	
		if menu_start:
			running = menu()
		if game_start:
			running = game()
	
	pygame.quit()
	sys.exit()	






main()

pygame.quit()