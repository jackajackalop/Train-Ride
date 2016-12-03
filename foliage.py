import pygame

class trees(object):
	def __init__(self,surf,color,location,size):
		self.color = color
		self.x,self.y = location
		self.width,self.height = size

class shrub(trees):
	def __init__(self,surf,color,location,size):
		super().__init__(surf,color,location,size)

	def draw(self):
		pass

class deciduous(trees):
	def __init__(self,surf,color,location,size):
		super().__init__(surf,color,location,size)

class pine(trees):
	def __init__(self,surf,color,location,size):
		super().__init__(surf,color,location,size)

if __name__ == "main":
	width,height = 800,600
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("happy little trees :DDDD")
	running = True
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		# test.draw(screen)
		pygame.display.flip()
		# screen.blit(canvas,(0,0))
	pygame.quit()
