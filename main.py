import pygame
import scene, landscape
import webscrape,webscrape2


#framework referenced from blog.lukasperaza.com and hermit 
#code for command console and taking commands based on hermit

def trainStart(width=1200,height=900):
	def draw():
		screen.fill((255,255,255))
		canvas.fill((255,255,255))
		seats.draw(canvas)
		if(start and end):
			if("desert" in currentInfo):
				desert.draw(window)
			else:
				sceneryBase.draw(window)
				if("plains" in currentInfo):
					plains.draw(window)
			if("mountain" in currentInfo):
				mountains.draw(window)
			if("hills" in currentInfo):
				hills.draw(window)
			if("river" in currentInfo):
				river.draw(window)
			if("forest" in currentInfo or "wood" in currentInfo 
				or "woods" in currentInfo):
				forest.draw(window)
		else:
			sceneryBase.draw(window)
			plains.draw(window)
		# print(currentInfo)
		windowFrame.draw(window)
		screen.blit(canvas,(0,0))
		screen.blit(window,(0,0))

	def daylightChange():
		sceneryBase.daylight(hour)
		plains.daylight(hour)
		river.daylight(hour)
		mountains.daylight(hour)
		desert.daylight(hour)
		hills.daylight(hour)
		forest.daylight(hour)

	def drawConsole():
		font =pygame.font.SysFont(pygame.font.get_default_font(),width//35)
		if(showConsole):
			screen.blit(console,[width*.01,height*.9])
			#TODO show available commands
			input = "".join(inputs)
			text = font.render(":"+input,False,(150,150,150))
			screen.blit(text,[width*.02,height*.91])

	# def statusUpdate():
	# 	nonlocal step,currentInfo,times
	# 	if(start and end):
	# 		distance = mph*(pygame.time.get_ticks()-times[-1])/1000/60
	# 		if(distance>=travelInfo['legs']['steps'][step]['distance']['value']):
	# 			currentInfo = webscrape2.surroundings(travelInfo['legs']['steps'][step]['end_location'])
	# 			times.append(pygame.time.get_ticks())
	# 			step+=1
	# 			print(step,currentInfo,travelInfo['legs']['steps'][step]['end_location'])
			# print(distance)

	def exeCommand(command):
		failed = "Not Executed! :("
		noSpace = command.split()
		try:
			commandType = noSpace[0]+" "+noSpace[1]
			if(commandType not in commandlist):
				return failed
			return "hahahahaaaaa :'D"
		except:
			return failed

	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("choo-choo")

	clock = pygame.time.Clock()
	running = True
	showConsole = False
	commandlist = {"set time","set month","set speed"}

	color = (120,130,130)
	inputs = ""
	executed = False
	step = 0
	speed = 0
	hour = 1
	mph = 500
	start,end=False,False
	startLoc,endLoc = "",""
	travelInfo={}
	currentInfo={}
	
	canvas= pygame.Surface((width,height))
	window = pygame.Surface((width*2/3,height*2/3))
	console = pygame.Surface((width/3,height/20))
	console.fill([0,0,0])
	console.set_alpha(50,pygame.RLEACCEL)

	seats = scene.seats(width,height,color)
	windowFrame = scene.frame(width,height,color)
	sceneryBase = landscape.land(width*2/3,height*2/3, 0,"clear")
	plains = landscape.plain(width*2/3,height*2/3,0,"clear")
	river = landscape.river(width*2/3,height*2/3,0,"clear",2)
	mountains = landscape.mountains(width*2/3,height*2/3,0,"clear",1)
	desert = landscape.desert(width*2/3,height*2/3,0,'clear')
	hills = landscape.hills(width*2/3,height*2/3,0,'clear')
	forest = landscape.forest(width*2/3,height*2/3,0,'clear')

	while(running):
		if(not start or not end): showConsole=True
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
			elif(event.type == pygame.KEYDOWN):
				key = pygame.key.name(event.key)
				if(executed):
					executed=False
					inputs = ""
				elif(not showConsole and key == "r"):
					inputs = ""
					executed = False
					speed = 0
					start,end=False,False
					startLoc,endLoc = "",""
					currentInfo = {}
					geoKW =[]
					tempKW = []
					climateKW=[]
				elif((key == "right" or key== "up") and abs(speed+10)<=50):
					speed+=10
					mph+=1000
					plains.changeSpeed(10)
					river.changeSpeed(10)
					mountains.changeSpeed(10)
					forest.changeSpeed(10)
				elif((key == "left" or key == "down")and (speed-10)>=0):
					speed-=10
					mph-=1000
					plains.changeSpeed(-10)
					river.changeSpeed(-10)
					mountains.changeSpeed(-10)
					forest.changeSpeed(-10)
				elif(key == "/"):
					showConsole = not showConsole
					inputs = ""
				elif(showConsole):
					if(len(inputs)<=30):
						if(key == "space"):
							inputs +=" "
						elif(key == "-"):
							inputs+="-"
						elif(len(key)==1):
							inputs+=key
						elif(key == "backspace" and len(inputs)>0):
							inputs=inputs[:-1]
					if(key == "return" and len(inputs)>0):
						if(not start):
							startLoc = inputs
							# check = webscrape2.checkLocation(startLoc)
							# if(check==None):
							# 	inputs = "Not available location :("
							# 	startLoc=""
							# else:
							start=True
							end=True#testing
							inputs = "Start location saved! :D"
						# elif(not end):
						# 	endLoc = inputs
							# check = webscrape2.checkLocation(endLoc)
							# travelInfo,currentInfo=webscrape2.infoGet(startLoc,
																		# endLoc)
							currentInfo = webscrape.infoGrab(startLoc) #testing
							print(currentInfo)
							# if(check==None or travelInfo==None):
							# 	inputs = "Not available location :("
							# 	start=False
							# 	endLoc=""
							# else:
							# 	times = [pygame.time.get_ticks()]
							# 	end = True
							# 	inputs = "End location saved! :D"
						else:
							inputs = str(exeCommand(str(inputs)))
						executed = True
		hour = (pygame.time.get_ticks()/(2000-speed*10))%24
		daylightChange()
		draw()
		drawConsole()
		pygame.display.flip()
		clock.tick()
		# statusUpdate()
	pygame.quit()


trainStart()