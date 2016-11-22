import pygame

class compartment(object):
	def __init__(self,width,height):
		self.width =width
		self.height = height
		self.color = (255,210,170)
		self.lvx,self.lvy = -.25*width,.6*height#left vanishing point for 2pt perspective
		self.rvx,self.rvy = 2.5*width,.6*height#left vanishing point for 2pt perspective

	def shake(self):
		pass
	def colorChange(self,change):
		newColor = list(self.color)
		for color in range(len(self.color)):
			newColor[color]+=change*color/2
		return (newColor )

class seats(compartment):
	def __init__(self,width=1500,height=1000):
		super().__init__(width,height)

	def perspective(self,side,x1,y1,x2):
		if(side=="l"):vy,vx = self.lvy,self.lvx
		else: vy,vx = self.rvy,self.rvx
		slope = (vy-y1)/(vx-x1)
		y2 = y1+(x2-x1)*slope
		return y2

	def draw(self,surf):
		w,h = self.width,self.height
		surf.fill(self.color)
		couchBase = super().colorChange(30)
		pygame.draw.polygon(surf,couchBase,[[w*2/3,h*.4], 
								[w,self.perspective('l',w*2/3,h*.4,w)],
								[w,h*.8], 
								[w*2/3,self.perspective('l',w,h*.8,w*2/3)]])
		couchSeat=super().colorChange(50)
		pygame.draw.polygon(surf,couchSeat, 
							[[w*2/3,self.perspective('l',w,h*3/4,w*2/3)],
							[w,self.perspective('l',w*2/3,
									self.perspective('l',w,h*3/4,w*2/3),w)],
							[w,h*.95], 
							[w/2,self.perspective('r',w*2/3,h*3/4,w/2)]])
		pygame.draw.polygon(surf,couchBase,
							[[w/2,self.perspective('r',w*2/3,h*3/4,w/2)],
							[w/2,self.perspective('r',w*2/3,h*3/4,w/2)+h/15],
							[w*.9,self.perspective('l',w/2,
								self.perspective('r',w*2/3,h*3/4,w/2)+h/10,w*.9)],
							[w,h],[w,h*.95]])