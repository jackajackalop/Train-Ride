import pygame

class land(object):
	pass

if __name__ == '__main__':
	width,height = 800,600
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("land")
	# seat = seats(width,height,(255,210,170))
	running = True
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		# seat.draw(canvas)
		pygame.display.flip()
		# screen.blit(canvas,(0,0))
	pygame.quit()