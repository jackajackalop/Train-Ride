import pygame
import random, math

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
		for index in range(0,len(pts)):
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
		self.farTreesColor = super().atmosphericPersp(self.grass,2)
		self.farPts=50
		self.farSpace = self.width/self.farPts
		self.farTreesPts(0,self.farPts+2)
		self.farTime = 30
		self.mid = []

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
		if(self.far[0][0]<0-self.farSpace):
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
		if(self.river[0][0]<0-self.riverSpace):
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
		self.mountainSpaceB = self.width//self.BNumber
		self.mountainTime = 1500
		self.BSplits = []
		self.FSplits = []
		self.mountainsB,self.BSplits=self.mountainPts(self.mountainsB,
			self.BSplits,self.BNumber,self.mountainSpaceB,0,self.BNumber+2)
		self.mountainsF,self.FSplits = self.mountainPts(self.mountainsF,
			self.FSplits,self.mtNumber,self.mountainSpaceF,0,self.mtNumber+2)
		self.color = (100,130,140)
		self.farColor = super().atmosphericPersp(self.color,2)

	#TODO fix ratchet mountains :'(		
	def mountainPts(self,pts,splits,number,space,start,times):
		widthMargin = self.width//(2*number)
		y = (self.height*3/4)//(self.size+.5)
		heightMargin = ((self.height*3/4)-y)//5
		previousHeight = y 
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

	def draw(self,surf):
		self.mountainsB=super().animate(surf,self.mountainsB,
			self.farColor,self.mountainSpaceB,self.mountainTime*3)
		self.timeDelay-=1
		self.mountainsF=super().animate(surf,self.mountainsF,
			self.color,self.mountainSpaceF,self.mountainTime)
		if(self.mountainsF[self.mtNumber+1][0]<0-self.mountainSpaceF):
			self.FSplits.pop(0)
			del self.mountainsF[-2:]
			del self.mountainsF[:self.FSplits[0]]
			self.mountainPts(self.mountainsF,self.FSplits,self.mtNumber,
						self.mountainSpaceF,self.width+self.mountainSpaceF,1)
		if(self.mountainsB[self.BNumber+1][0]<0-self.mountainSpaceB):
			del self.mountainsB[:self.BSplits[0]]
			self.BSplits.pop(0)
			del self.mountainsB[-2:]
			self.mountainPts(self.mountainsB,self.BSplits,self.BNumber,
						self.mountainSpaceB,self.width+self.mountainSpaceB,1)

class desert(land):
	def __init__(self,width,height,temp,weather):
		super().__init__(width,height,temp,weather)
		self.grass = (180,150,90)

class hills(land):
	def __init__(self,width,height,temp,weather):
		super().__init__(width,height,temp,weather)
		self.hillsF,self.hillsB=[],[]
		self.hillNumber = 3
		self.BNumber = 2
		self.smoothness=10
		self.hillSpaceF = self.width//self.hillNumber
		self.hillSpaceB = self.width//self.BNumber
		self.hillTime = 200
		self.hillsB=self.hillPts(self.hillsB,self.hillSpaceB,0,self.BNumber+2)
		self.hillsF = self.hillPts(self.hillsF,self.hillSpaceF,0,self.hillNumber+2)
		self.grass = super().atmosphericPersp(self.grass,1)
		self.farColor = super().atmosphericPersp(self.grass,1)

	def changeSpeed(self,x):
		self.speed +=10*x

	def parabola(self,maxY,space, x):
		y = (x-space/2)**2/(space)+maxY
		if(y>self.height*3/4):
			y = self.height*3/4
		return y

	def hillPts(self,ptsList,space,start,times):
		base = self.height*3/4
		xIncr = space/self.smoothness
		for hill in range(times):
			maxY= base - random.randint(base//20,base//10)
			for pt in range(self.smoothness):
				x = xIncr*pt+space*hill+start
				y = self.parabola(maxY,space,xIncr*pt)
				ptsList.append([x,y])
		ptsList.append([self.width+2*space,self.height*3/4])
		ptsList.append([0,self.height*3/4])
		return ptsList

	def draw(self,surf):
		self.hillsB=super().animate(surf,self.hillsB,
			self.farColor,self.hillSpaceB,self.hillTime*3)
		self.timeDelay-=1
		self.hillsF=super().animate(surf,self.hillsF,
			self.grass,self.hillSpaceF,self.hillTime)
		if(self.hillsF[0][0]<0-self.hillSpaceF):
			del self.hillsF[-2:]
			del self.hillsF[:self.smoothness]
			self.hillPts(self.hillsF,
						self.hillSpaceF,self.width+2*self.hillSpaceF,1)
		if(self.hillsB[0][0]<0-self.hillSpaceB):
			del self.hillsB[-2:]
			del self.hillsB[:self.smoothness]
			self.hillPts(self.hillsB,
						self.hillSpaceB,self.width+2*self.hillSpaceB,1)

class lake(land): 
	def __init__(self,width,height,temp,weather):
		super().__init__(width,height,temp,weather)
		self.lake = []
		self.lakeColor = (110,170,200)
		self.lakeSpace = 2*width
		self.lakePtsNumber=5
		self.lakeTime = 30
		self.lakePts()

	def lakePts(self):
		w,h = self.width,self.height
		yIncr = h/4/self.lakePtsNumber
		xMargin = w//2
		for pt in range(self.lakePtsNumber+1):
			x = random.randint(0,xMargin)
			self.lake.append([x,h-yIncr*pt])
		for pt in range(self.lakePtsNumber+1):
			x = random.randint(0,xMargin)
			self.lake.append([9*w+x,h*3/4+yIncr*pt])

	def draw(self,surf):
		speedIncr = (self.lakeSpace/self.lakeTime)/6
		speed = self.lakeSpace/self.lakeTime/10+self.speed*speedIncr
		pygame.draw.polygon(surf,self.lakeColor,self.lake)
		self.lake=super().shift(self.lake,speed)

class forest(land):
	def __init__(self,width,height,temp,weather):
		super().__init__(width,height,temp,weather)
		self.forest = []
		self.color = self.atmosphericPersp(self.grass,-2)
		self.trees = 6
		self.treePts = 20
		self.forestTime = 30
		self.forestSpace = self.width//self.trees
		self.forestPts()

	def forestPts(self,start,times):
		w,h = self.width,self.height
		yIncr = h/4/self.treePts
		xIncr = w/self.trees/self.treePts
		for tree in range(self.trees+1):
			for pt in range(self.treePts+1):

		for pt in range(self.lakePtsNumber+1):
			x = random.randint(0,xMargin)
			self.lake.append([x,h-yIncr*pt])
		for pt in range(self.lakePtsNumber+1):
			x = random.randint(0,xMargin)
			self.lake.append([9*w+x,h*3/4+yIncr*pt])

	def draw(self,surf):
		speedIncr = (self.lakeSpace/self.lakeTime)/6
		speed = self.lakeSpace/self.lakeTime/10+self.speed*speedIncr
		pygame.draw.polygon(surf,self.lakeColor,self.lake)
		self.lake=super().shift(self.lake,speed)
if __name__ == '__main__':
	width,height = 800,600
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("land")
	base = land(width,height,0,"clear")
	testPlain = plain(width,height,0,"clear")
	testDesert = desert(width,height,0,"clear")
	testRiver = river(width,height,0,"clear",3)
	testmountains = mountains(width,height,0,"clear",1)
	testHills = hills(width,height,0,"clear")
	testLakes = lake(width,height,0,"clear")
	testForest = forest(width,height,0,"clear")
	running = True
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
		base.draw(screen)
		testPlain.draw(screen)
		# testDesert.draw(screen)
		# testmountains.draw(screen)
		# testHills.draw(screen)
		# testRiver.draw(screen)
		testLakes.draw(screen)
		testForest.draw(screen)
		pygame.display.flip()
	pygame.quit()