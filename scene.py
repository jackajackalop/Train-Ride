import pygame

class compartment(object):
	def __init__(self,width,height,color):
		self.width =width
		self.height = height
		self.color = color
		self.lvx,self.lvy = -.25*width,.6*height#left vanishing point for 2pt perspective
		self.rvx,self.rvy = 2.5*width,.6*height#left vanishing point for 2pt perspective

	def shake(self):
		pass
	def colorChange(self,change):
		newColor = list(self.color)
		for color in range(len(self.color)):
			newColor[color]+=change*color/2
		return (newColor )
	def perspective(self,side,x1,y1,x2):
		if(side=="l"):vy,vx = self.lvy,self.lvx
		else: vy,vx = self.rvy,self.rvx
		slope = (vy-y1)/(vx-x1)
		y2 = y1+(x2-x1)*slope
		return int(y2)

class seats(compartment):
	def __init__(self,width,height,color):
		super().__init__(width,height,color)


	def draw(self,surf):
		w,h = self.width,self.height
		surf.fill(self.color)
		#couch and walls
		couchBase = self.colorChange(30)
		otherWall = self.colorChange(-20)
		pygame.draw.rect(surf,otherWall,(0,0,w*2/3+20,h))
		shadow = self.colorChange(-35)
		pygame.draw.rect(surf,shadow,(w/2+40,self.perspective('l',w/2,
							self.perspective('r',w*2/3,
							self.perspective('l',w,h*3/4,w*2/3),w/2)+h*.04,w/2+40),
										w,h))
		pygame.draw.polygon(surf,couchBase,[[w*2/3,h*.4], 
							[w,self.perspective('l',w*2/3,h*.4,w)],
							[w,h*.8], 
							[w*2/3,self.perspective('l',w,h*.8,w*2/3)]])
		couchSeat=self.colorChange(50)
		pygame.draw.polygon(surf,couchSeat, 
							[[w*2/3,self.perspective('l',w,h*3/4,w*2/3)],
							[w,self.perspective('l',w*2/3,
									self.perspective('l',w,h*3/4,w*2/3),w)],
							[w,self.perspective('l',w/2,self.perspective('r',w*2/3,
									self.perspective('l',w,h*3/4,w*2/3),w/2),w)], 
							[w/2,self.perspective('r',w*2/3,self.perspective('l',w,h*3/4,w*2/3),w/2)]])
		pygame.draw.polygon(surf,couchBase,
							[[w/2,self.perspective('r',w*2/3,self.perspective('l',w,h*3/4,w*2/3),w/2)],
							[w,self.perspective('l',w/2,self.perspective('r',w*2/3,
									self.perspective('l',w,h*3/4,w*2/3),w/2),w)],
							[w,self.perspective('l',w/2,self.perspective('r',w*2/3,
								self.perspective('l',w,h*3/4,w*2/3),w/2)+h*.04,w)],
							[w/2,self.perspective('l',w,self.perspective('l',w/2,self.perspective('r',w*2/3,
								self.perspective('l',w,h*3/4,w*2/3),w/2)+h*.04,w),w/2)]])

class frame(compartment):
	def draw(self,surf):
		w,h = self.width,self.height
		
		#blocks off wall based on perspective
		otherWall=self.colorChange(-20)
		pygame.draw.polygon(surf,otherWall,[[0,h/20],
							[w*2/3-20, self.perspective('r',0,h/20,w*2/3-20)],
							[w*2/3-20,0],[0,0]])
		pygame.draw.polygon(surf,otherWall,
							[[w*2/3-20,0],[w*2/3-20,h*2/3+h/20],
							[w*2/3,h*2/3+h/20],[w*2/3,0]])
		pygame.draw.polygon(surf,otherWall,[[w*2/3-20,h*2/3-h/20],
							[0,self.perspective('r',w*2/3-20,h*2/3-h/20,0)],
							[0,self.perspective('r',w*2/3-20,h*2/3-h/20,0)+h/20]
							,[w*2/3-20,h*2/3]])

if __name__ == '__main__':
	width,height = 800,600
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	canvas= pygame.Surface((width,height))
	window =pygame.Surface((width*2/3,height*2/3))
	pygame.display.set_caption("choo-choo")
	seat = seats(width,height,(255,210,170))
	frame = frame(width,height,(255,210,170))
	running = True
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		seat.draw(canvas)
		frame.draw(window)
		pygame.display.flip()
		screen.blit(canvas,(0,0))
		screen.blit(window,(0,0))
	pygame.quit()
