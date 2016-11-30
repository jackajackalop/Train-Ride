import pygame
import random

class land(object):
	def __init__(self,width,height,temp,weather):
		self.width =width
		self.height = height
		self.temp = temp
		self.weather = weather
		self.grass=	(120,130,40)
		self.sky = (190,210,200)
		self.timeDelay = 0
		self.speed = 0

	def temperature(self):
		self.hueShift = (0,0,0)

	def changeSpeed(self,x):
		self.speed+=x


	@staticmethod
	def atmosphericPersp(color,distance): 
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

	def shift(self,pts,speed):
		for index in range(0,len(pts)-1):
			pts[index][0]-=speed
		return pts

	def animate(self,surf,pts,color,space,time):
		self.timeDelay+=1
		w,h = self.width,self.height
		speedIncr = (space/time)/6
		speed = space/time+self.speed*speedIncr
		pts = self.shift(pts,speed)
		pygame.draw.polygon(surf,color,pts)
		return pts
		

class plain(land):
	def __init__(self,width,height,temp,weather):
		super().__init__(width,height,temp,weather)
		self.far = []
		self.farTreesColor = super().atmosphericPersp(self.grass,3)
		self.farPts=50
		self.farSpace = self.width/self.farPts
		self.farTreesPts(0,self.farPts+2)
		self.farTime = 30
		self.mid = []
	#TODO draw more ahead of train
	def farTreesPts(self,start,times):
		w,h = self.width,self.height
		for bump in range(times):
			self.far.append([start+self.farSpace*bump,
							random.randint(h*3//4-h//30,h*3//4-h//50)])
		self.far.append([w+1*self.farSpace,h*3/4])
		self.far.append([0,h*3/4])

	def draw(self,surf):
		self.far=super().animate(surf,
						self.far,self.farTreesColor,self.farSpace,self.farTime)
		if(self.timeDelay%self.farTime==0):
			self.far.pop(0)
			del self.far[-2:]
			self.farTreesPts(self.width+self.farSpace,1)

class river(land):
	def __init__(self,width,height,temp,weather,distance):
		super().__init__(width,height,temp,weather)
		self.distance = distance
		self.river= []
		self.riverPts = 6
		self.riverSpace = self.width/(self.riverPts)
		self.riverTime = 10*(distance+1)
		self.riverColor = (100,100,150)
		self.riverPoints(0,self.riverPts+2)
	#TODO draw more ahead
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
			
class mountains(land):
	def __init__(self,width,height,temp,weather,size):
		super().__init__(width,height,temp,weather)
		self.size = size
		self.mountainsB=[]
		self.mountainsF = []
		self.mtNumber = random.randint(3,5)
		self.BNumber = self.mtNumber-2
		self.mountainSpaceF = self.width//self.mtNumber
		self.mountainSpaceB = self.width//(self.mtNumber-2)
		self.mountainTime = 800
		self.BSplits = []
		self.FSplits = []
		self.mountainsB,self.BSplits=self.mountainPts(self.mountainsB,
			self.BSplits,self.BNumber,self.mountainSpaceB,0,self.BNumber+2)
		self.mountainsF,self.FSplits = self.mountainPts(self.mountainsF,
			self.FSplits,self.mtNumber,self.mountainSpaceF,0,self.mtNumber+2)
		self.color = (100,130,140)
		self.farColor = super().atmosphericPersp(self.color,2)

	def mountainPts(self,pts,splits,number,space,start,times):
		widthMargin = self.width//(2*number)
		y = (self.height*3/4)//(self.size+.5)
		heightMargin = ((self.height*3/4)-y)//5
		previousHeight = y #TODO generate by angle instead of height
		for mountains in range(times):
			h = int(start+space*mountains)
			h1 = random.randint(h,h+widthMargin)
			h2= h+space
			pts.append([h1,self.height*3/4])
			mountainBumps = random.randint(8,12)
			splits.append(mountainBumps+1)
			ptDist = (h2-h1)//mountainBumps
			ptMargin = ptDist//2
			for bumps in range(mountainBumps):
				ptX = random.randint(h1+ptDist*bumps,h1+ptDist*bumps+ptMargin)
				if(previousHeight+heightMargin)>=(self.height*3/4):
					previousHeight=self.height*3/4 - heightMargin 
				ptY = random.randint(previousHeight-heightMargin,
									previousHeight+heightMargin)
				previousHeight = ptY
				pts.append([ptX,ptY])
		pts.append([h2,self.height*3/4])
		pts.append([0,self.height*3/4])
		return pts,splits
	#TODO removes mountain based on h1, but should be based on h2
	def draw(self,surf):
		self.mountainsB=super().animate(surf,self.mountainsB,
			self.farColor,self.mountainSpaceB,self.mountainTime*3)
		self.timeDelay-=1
		self.mountainsF=super().animate(surf,self.mountainsF,
			self.color,self.mountainSpaceF,self.mountainTime)
		if(self.timeDelay%(self.mountainTime*3)==0):
			del self.mountainsB[:self.BSplits[0]]
			self.BSplits.pop(0)
			del self.mountainsB[-2:]
			self.mountainPts(self.mountainsB,self.BSplits,self.BNumber,
						self.mountainSpaceB,self.width+self.mountainSpaceB,1)
		if(self.timeDelay%self.mountainTime==0):
			self.FSplits.pop(0)
			del self.mountainsF[-2:]
			del self.mountainsF[:self.FSplits[0]]
			self.mountainPts(self.mountainsF,self.FSplits,self.mtNumber,
						self.mountainSpaceF,self.width+self.mountainSpaceF,1)


class hills(land):
	pass

class forest(land):
	pass

if __name__ == '__main__':
	width,height = 800,600
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("land")
	base = land(width,height,0,"clear")
	testPlain = plain(width,height,0,"clear")
	testRiver = river(width,height,0,"clear",2)
	testmountains = mountains(width,height,0,"clear",1)
	running = True
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		base.draw(screen)
		testmountains.draw(screen)
		testPlain.draw(screen)
		testRiver.draw(screen)
		pygame.display.flip()
	pygame.quit()