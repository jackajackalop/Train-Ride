import pygame
import random

class land(object):
	def __init__(self,width,height,temp,weather):
		self.width =width
		self.height = height
		self.scrollX = 0
		self.temp = temp
		self.weather = weather
		self.grass=	(110,140,30)
		self.sky = (190,210,200)

	def temperature(self):
		self.hueShift = (0,0,0)

	def atmosphericPersp(self,color,distance): 
	#things in distance are lighter and less saturated
		newColor = list(color)
		for color in range(3):
			newColor[color]+=25*distance
		averageColor = sum(newColor)//3
		for color in range(3):
			difference = averageColor-newColor[color]
			newColor[color]+=difference*(distance-1)/3
		return (newColor)

class plain(land):
	def __init__(self,width,height,temp,weather):
		super().__init__(width,height,temp,weather)
		self.far = []
		self.farTreesColor = self.atmosphericPersp(self.grass,3)
		self.farSpacing =50
		self.farSpace = self.width/self.farSpacing
		self.farTrees(0,self.farSpacing+2)
		self.farTime = 30
		self.mid = []
		self.timeDelay = 0
	def shift(self):
		for index in range(0,len(self.far)-1):
			self.far[index][0]-=self.farSpace/self.farTime
		
	def farTrees(self,start,times):
		w,h = self.width,self.height
		for bump in range(times):
			self.far.append([start+self.farSpace*bump,random.randint(h*3/4-h/30,h*3/4-h/50)])
		self.far.append([w+1*self.farSpace,h*3/4])
		self.far.append([0,h*3/4])

	def farBG(self,surf):
		w,h = self.width,self.height
		pygame.draw.polygon(surf,self.farTreesColor,self.far)
		if(self.timeDelay%self.farTime==0):
			self.far.pop(0)
			del self.far[-2:]
			self.farTrees(w+self.farSpace,1)

	def draw(self,surf):
		self.timeDelay+=1
		w,h = self.width,self.height
		pygame.draw.rect(surf,self.sky,(0,0,w,h*3/4))
		pygame.draw.rect(surf,self.grass,(0,h*3/4,w,h/4))
		self.shift()
		self.farBG(surf)


if __name__ == '__main__':
	width,height = 800,600
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("land")
	test = plain(width,height,20,"clear")
	running = True
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		test.draw(screen)
		pygame.display.flip()
		# screen.blit(canvas,(0,0))
	pygame.quit()