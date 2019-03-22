command = ""
started = False

while True:

  command = input ("> ").lower()
if command =="start":
	if started:
		print ("car is already started!")
	else :
		started = True
		print ("car started.....")
elif command =="stop":
	if not started :
		print ("car is already stoped!")
	else:
		stated = True 
		print ("car stoped ")
elif  command =="help":
	print ("""
			start - to start the car 
			stop - to stop the car 
			quit - to exit the game
		
			""")
elif command == "quit":
	print ("quit")