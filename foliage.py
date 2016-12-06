import pygame
import math,random

#copied hermit's code for tree4 and changed leaves color
def drawTree(**p):
	if p['depth'] < p['maxdepth']:
		if(p['height']<10): p['color']=(100,140,60)
		if p['height'] <1:return

		dep = p['depth']
		p['width'] *= (p['dwidth'](dep))
		p['width'] = int(math.ceil(p['width']))

		x0 = p['x']+math.cos(p['angle'])*p['trunk']
		y0 = p['y']-math.sin(p['angle'])*p['trunk']
		pygame.draw.line(p['surf'],p['color'],[p['x'],p['y']],[x0,y0],p['width'])


		p['width'] *= p['dwidth'](dep)
		p['width'] = int(math.ceil(p['width']))
		a1 = p['angle']-p['opening']*p['dopening'](dep)
		a2 = p['angle']+p['opening']*p['dopening'](dep)

		h1 = p['height'] * p['dheight'](dep)
		x1 = x0+math.cos(a1)*h1
		y1 = y0-math.sin(a1)*h1

		h2 = p['height'] * p['dheight'](dep)
		x2 = x0+math.cos(a2)*h2
		y2 = y0-math.sin(a2)*h2

		pygame.draw.line(p['surf'],p['color'],[x0,y0],[x1,y1],p['width'])
		pygame.draw.line(p['surf'],p['color'],[x0,y0],[x2,y2],p['width'])


		p['trunk'] *= p['dtrunk'](dep)

		p['depth'] += .5
		p['x'],p['y'],p['height'],p['angle'] = x1,y1,h1,a1-p['dangle'](dep)

		drawTree(**p)


		p['depth'] += .5
		p['x'],p['y'],p['height'],p['angle'] = x2,y2,h2,a2+p['dangle'](dep)
		drawTree(**p)
	else:
		return


def tree4(surf,x,y,color):
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: (-math.pi/6)+((random.random()-0.5)*(dep))*2,

			 trunk = 50,
			 dtrunk = lambda dep: 0.8*random.random(),

			 width = 8,
			 dwidth = lambda dep: random.random()*0.2+0.8,

			 height = 50,
			 dheight = lambda dep: random.random()*0.5+0.5,

			 opening = math.pi/5,
			 dopening = lambda dep: 0.8 + random.random()*0.5*dep*2,

			 color = color,
			 depth = 0,
			 maxdepth = 8
			)
# class shrub(trees):
# 	def __init__(self,surf,color,location,size):
# 		super().__init__(surf,color,location,size)

# 	def draw(self):
# 		pass

# class deciduous(trees):
# 	def __init__(self,surf,color,location,size):
# 		super().__init__(surf,color,location,size)

# class pine(trees):
# 	def __init__(self,surf,color,location,size):
# 		super().__init__(surf,color,location,size)

if __name__ == '__main__':
	width,height = 800,600
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("happy little trees :DDDD")
	running = True
	tree4(screen,width//2,height*3//4,(100,80,60))
	while running:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
			if(event.type==pygame.KEYDOWN):
				screen.fill((0,0,0))
				tree4(screen,width//2,height*3//4,(100,80,60))
		pygame.display.flip()
		# screen.blit(canvas,(0,0))
	pygame.quit()
