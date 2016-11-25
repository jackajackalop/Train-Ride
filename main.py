import pygame
import scene, landscape

#framework referenced from blog.lukasperaza.com and hermit 
#code for taking commands taken from hermit

def trainStart(width=1200,height=900):
	def draw():
		screen.fill((255,255,255))
		seats.draw(canvas)
		scenery.draw(window)
		windowFrame.draw(window)
		screen.blit(canvas,(0,0))
		screen.blit(window,(0,0))

	pygame.init()
	screen = pygame.display.set_mode((width,height))
	canvas= pygame.Surface((width,height))
	window = pygame.Surface((width*2/3,height*2/3))
	pygame.display.set_caption("choo-choo")
	clock = pygame.time.Clock()
	running = True
	commandlist = ["set time","set month","set speed"]
	color = (255,210,170)
	seats = scene.seats(width,height,color)
	windowFrame = scene.frame(width,height,color)
	scenery = landscape.plain(width*2/3,height*2/3,0,"clear")
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		draw()
		pygame.display.flip()
		clock.tick()
	pygame.quit()


trainStart()