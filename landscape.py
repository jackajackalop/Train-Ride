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
		self.timeDelay = 0

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

	def draw(self,surf):
		w,h = self.width,self.height
		pygame.draw.rect(surf,self.sky,(0,0,w,h*3/4))
		pygame.draw.rect(surf,self.grass,(0,h*3/4,w,h/4))

	def shift(self,pts,space,time):
		for index in range(0,len(pts)-1):
			pts[index][0]-=space/time
		return pts

	def animate(self,surf,pts,color,space,time):
		self.timeDelay+=1
		w,h = self.width,self.height
		pts = self.shift(pts,space,time)
		pygame.draw.polygon(surf,color,pts)
		return pts
		

class plain(land):
	def __init__(self,width,height,temp,weather):
		super().__init__(width,height,temp,weather)
		self.far = []
		self.farTreesColor = self.atmosphericPersp(self.grass,3)
		self.farPts=50
		self.farSpace = self.width/self.farPts
		self.farTreesPoints(0,self.farPts+2)
		self.farTime = 30
		self.mid = []

		
	def farTreesPoints(self,start,times):
		w,h = self.width,self.height
		for bump in range(times):
			self.far.append([start+self.farSpace*bump,
							random.randint(h*3/4-h/30,h*3/4-h/50)])
		self.far.append([w+1*self.farSpace,h*3/4])
		self.far.append([0,h*3/4])

	def draw(self,surf):
		self.far=super().animate(surf,
						self.far,self.farTreesColor,self.farSpace,self.farTime)
		if(self.timeDelay%self.farTime==0):
			self.far.pop(0)
			del self.far[-2:]
			self.farTreesPoints(self.width+self.farSpace,1)

class river(land):
	def __init__(self,width,height,temp,weather,distance):
		super().__init__(width,height,temp,weather)
		self.distance = distance
		self.river= []
		self.riverPts = 6
		self.riverSpace = self.width/self.riverPts
		self.riverTime = 10*(distance+1)
		self.riverColor = (100,100,150)
		self.riverPoints(0,self.riverPts+2)

	def riverPoints(self,start,times):
		w,h = self.width,self.height
		h1 =h-h*self.distance//12
		h2 = h1 + h/self.distance//12
		split = len(self.river)//2
		upper,lower = self.river[:split],self.river[split:]
		lower.reverse()
		for point in range(times):
			upper.append([start+self.riverSpace*point,
								random.randint(h1,h1+(h2-h1)//4)])

			lower.append([start+self.riverSpace*point,
								random.randint((h1+h2)//2,h2)])
		lower.reverse()
		self.river=upper+lower

	def draw(self,surf):
		self.river=super().animate(surf,self.river,self.riverColor
									,self.riverSpace,self.riverTime)
		if(self.timeDelay%self.riverTime==0):
			self.river.pop(0)
			self.river.pop(-2)
			self.riverPoints(self.width+self.riverSpace,1)
			
class hills(land):
	def __init__(self,width,height,temp,weather):
		super().__init__(width,height,temp,weather)
		self.hills=[]

	def hillPoints(self,start,times):
		

class mountains(land):
	pass

# class forest(land):
# 	pass

if __name__ == '__main__':
	width,height = 800,600
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("land")
	base = land(width,height,0,"clear")
	testPlain = plain(width,height,0,"clear")
	testRiver = river(width,height,0,"clear",2)
	testHills = hills(width,height,0,"clear")
	running = True
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		base.draw(screen)
		testPlain.draw(screen)
		testRiver.draw(screen)
		pygame.display.flip()
		# screen.blit(canvas,(0,0))
	pygame.quit()