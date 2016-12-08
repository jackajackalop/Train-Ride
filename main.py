import pygame
import scene, landscape
import webscrape2, webscrape
import os
import random


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

	def monthChange():
		sceneryBase.changeMonth(month)
		plains.changeMonth(month)
		river.changeMonth(month)
		mountains.changeMonth(month)
		desert.changeMonth(month)
		hills.changeMonth(month)
		forest.changeMonth(month)

	def drawConsole():
		font =pygame.font.SysFont(pygame.font.get_default_font(),width//35)
		if(showConsole):
			screen.blit(console,[width*.01,height*.9])
			#TODO show available commands
			input = "".join(inputs)
			text = font.render(":"+input,False,(150,150,150))
			screen.blit(text,[width*.02,height*.91])

	def drawSplash():
		def multiline(instructions):
			lines = len(instructions)//40
			lineNumber =0
			for line in instructions.splitlines():
				textLine = line.strip()
				# textLine.strip()
				text=font.render(textLine,False,(180,180,180))
				screen.blit(text,[margin,margin+height//20*lineNumber])
				lineNumber+=1

		font =pygame.font.SysFont('lettergothicstdopentype',width//30,bold=True)
		margin = splashMargins+20
		if(showSplash):
			splash.fill((0,0,0))
			screen.blit(splash,[splashMargins,splashMargins])
			if(not showHome):
				instructions ="".join(
"""Hello! Welcome to Train Ride Simulator!
Enter two destinations that can be 
traveled between by train (not through
oceans or to fictional places) and 
watch as beautiful computer-generated 
approximations of the actual scenery 
along the route pass you by!

Commands you can use:
-set time x (x is an hour of the day 
			in 24 hour form)
-set month x
-set speed x (x is betweed -5 and 5)
-help 

Press q to quit this instructions screen
""")
				multiline(instructions)
			elif(showHome): 
				font =pygame.font.SysFont('lettergothicstdopentype',width//15,bold=True)
				instructions ="Train Ride Simulator!"
				text=font.render(instructions,False,(180,180,180))
				screen.blit(text,[margin,height//2])
				font =pygame.font.SysFont('lettergothicstdopentype',width//25,bold=True)
				instructions ="Press 'h' for help or 'q' to start"
				text=font.render(instructions,False,(180,180,180))
				screen.blit(text,[margin,height//2+height//10])
			elif(arrived):
				font =pygame.font.SysFont('lettergothicstdopentype',width//15,bold=True)
				instructions ="You have arrived!"
				text=font.render(instructions,False,(180,180,180))
				screen.blit(text,[margin,height//2])
				font =pygame.font.SysFont('lettergothicstdopentype',width//25,bold=True)
				instructions ="Press 'r' to restart!"
				text=font.render(instructions,False,(180,180,180))
				screen.blit(text,[margin,height//2+height//10])

	def statusUpdate():
		nonlocal step,currentInfo,times,skip
		if(start and end):
			try:
				# print(skip)
				distance = mph*(pygame.time.get_ticks()-times[-1])/1000/60
				if(distance>=travelInfo['legs']['steps'][step]['distance']['value'] or skip):
					currentInfo = webscrape2.surroundings(travelInfo['legs']['steps'][step]['end_location'])
					times.append(pygame.time.get_ticks())
					step+=1
					# print(step,currentInfo,travelInfo['legs']['steps'][step]['end_location'])
					skip=False
			except: 
				skip = False
				arrived=True

	def exeCommand(command):
		nonlocal speed, month,showSplash,showConsole
		failed = "Not Executed! :("
		noSpace = command.lower().split()
		months =["january","february","march","april","may","june",
		"july","august","september","october","november","december"]
		try:
			if(command=="help"):
				showConsole=False
				showSplash=True
				showHome=False
			else:
				commandType = noSpace[0]+" "+noSpace[1]
				amount = noSpace[2]
				if(commandType not in commandlist):
					return failed
				else:
					if(commandType == "set speed"):
						speed = int(noSpace[2])
					elif(commandType == "set month"):
						if(not amount.isdigit()):
							amount = months.index(amount)+1
						month = int(amount)
						monthChange()

			return "Executed :D"
		except:
			return failed

	def queueMusic(path):
		music = []
		for file in os.listdir(path):
			if(".mp3" in file):
				music.append(path+"/"+file)
		return shuffle(music)

	def shuffle(songlist):
		playlist=[]
		for songs in range(len(songlist)):
			index = random.randint(0,len(songlist)-1)
			playlist.append(songlist.pop(index))
		return playlist

	pygame.init()
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("Train Ride Simulator")
	playlist = queueMusic("music")
	played = []
	SONGOVER= pygame.USEREVENT
	pygame.mixer.music.set_endevent(SONGOVER)

	clock = pygame.time.Clock()
	running = True
	showConsole = False
	showSplash = True
	showHome=True
	arrived =False
	commandlist = {"set time","set month","set speed","help",}

	color = (120,130,130)
	inputs = ""
	executed = False
	skip = False
	step = 0
	speed = 0
	hour = 0
	month = 6
	mph = 500
	start,end=False,False
	startLoc,endLoc = "",""
	travelInfo={}
	currentInfo={}
	
	canvas= pygame.Surface((width,height))
	window = pygame.Surface((width*2/3,height*2/3))
	splashMargins = 20
	splash = pygame.Surface((width-2*splashMargins,height-2*splashMargins))
	splash.set_alpha(120,pygame.RLEACCEL)

	console = pygame.Surface((width/3,height/20))
	console.fill([0,0,0])
	console.set_alpha(50,pygame.RLEACCEL)

	seats = scene.seats(width,height,color)
	windowFrame = scene.frame(width,height,color)
	sceneryBase = landscape.land(width*2/3,height*2/3, 0,"clear",month)
	plains = landscape.plain(width*2/3,height*2/3,0,"clear",month)
	river = landscape.river(width*2/3,height*2/3,0,"clear",2,month)
	mountains = landscape.mountains(width*2/3,height*2/3,0,"clear",1,month)
	desert = landscape.desert(width*2/3,height*2/3,0,'clear',month)
	hills = landscape.hills(width*2/3,height*2/3,0,'clear',month)
	forest = landscape.forest(width*2/3,height*2/3,0,'clear',month)

	while(running):
		if(not start or not end):
			if(not showSplash): showConsole=True
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
			elif(event.type==SONGOVER):
				played+=playlist.pop(0)
				if(len(playlist)==0):
					playlist = shuffle(played)
				pygame.mixer.music.load(playlist[0])
				pygame.mixer.music.play()
			elif(event.type == pygame.KEYDOWN):
				key = pygame.key.name(event.key)
				if(key == "/"):
					showConsole = not showConsole
					inputs = ""
				elif(executed):
					executed=False
					inputs = ""
				elif(showSplash):
					if(key=='q'):
						showSplash=False
					if(key=='h'):
						showHome = not showHome
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
						if(inputs=="help"):
							inputs =str(exeCommand(str(inputs)))
						elif(not start):
							startLoc = inputs
							check = webscrape2.checkLocation(startLoc)
							if(check==None):
								inputs = "Not available location :("
								startLoc=""
							else:
								start=True
								inputs = "Start location saved! :D"
						elif(not end):
							endLoc = inputs
							check = webscrape2.checkLocation(endLoc)
							travelInfo,currentInfo=webscrape2.infoGet(startLoc,
																		endLoc)
							if(check==None or travelInfo==None):
								inputs = "Not available location :("
								start=False
								endLoc=""
							else:
								times = [pygame.time.get_ticks()]
								end = True
								inputs = "End location saved! :D"
								pygame.mixer.music.load(playlist[0])
								pygame.mixer.music.play()

						else:
							inputs = str(exeCommand(str(inputs)))
						executed = True
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
					#for incrementing speed of the train
				elif(not showConsole and key =="s"):
					skip =True
				if((key == "right" or key== "up") and abs(speed+10)<=50):
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
		hour = (pygame.time.get_ticks()/(2000-speed*10))%24
		daylightChange()
		draw()
		drawSplash()
		drawConsole()
		pygame.display.flip()
		clock.tick()
		statusUpdate()
	pygame.quit()


trainStart()