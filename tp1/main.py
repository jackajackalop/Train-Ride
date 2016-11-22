import pygame
import scene

#framework referenced from blog.lukasperaza.com and hermit 


def trainStart(width=1500,height=1000):
	def draw():
		screen.fill((255,255,255))
		seats.draw(canvas)
		screen.blit(canvas,(0,0))
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	canvas= pygame.Surface((width,height))
	pygame.display.set_caption("choo-choo")
	clock = pygame.time.Clock()
	running = True

	seats = scene.seats(1500,1000)

	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		draw()
		pygame.display.flip()
		clock.tick()
	pygame.quit()


trainStart()