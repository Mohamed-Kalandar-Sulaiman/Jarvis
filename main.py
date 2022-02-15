from my_imports import *
from my_variables import *

bot_name = None
user_name = None
user_location = None
part = None



#................................functions.....................................................
def fetch_details():
	def get_part():
		#To greet according to part of the day.....
		time = datetime.datetime.now().strftime('%I:%M %p')
		hr = time[0:2]
		m = time[6:]
		if(hr < "12"  and hr >="06" and m == "AM"):
			return "morning"
		elif(hr >="12"  and m == "PM"):
			return "afternoon"
		elif(hr>= "04" and hr <= "06" and m =="PM"):
			return "evening"
		else:
			return "day"

	try:
		#Extracting data such as bot name , username
		with open("jarvis_data.txt" ,"r") as f :
			global bot_name , user_name , user_location , part
			user_name = f.readline().rstrip("\n")
			bot_name = f.readline().rstrip("\n")	
			user_location = f.readline().rstrip("\n")
			f.close()
			part = get_part()
			return
	except : 
			create_user()
			fetch_details()
			return
#....................................................................................
def create_user():
	#Setup process of the bot
	with open("jarvis_data.txt" , "w") as f:
		debug("Welcome to the setup pocess...")
		debug("Whats your name ")
		un = get_input()
		un = un.upper()
		f.write(un +"\n")

		debug("Hi {0} ,  how would you like to call me".format(un))
		bn = get_input()
		bn = bn.upper()
		f.write(bn+"\n")

		debug("Which city do you live in ?")
		lc = get_input()
		lc.upper()
		lc = lc.upper()
		f.write(lc+"\n")
		debug("Now you are good to go ....")
		time.sleep(5)
		f.close()
		return

#................................................................................................
def kill_yourself():
	#To kill the bot.............. it can respawn :)
	debug("Never though you will kill me , bye forever {0}".format(user_name))
	os.remove("jarvis_data.txt")
	time.sleep(5)
	create_user()
	return

#........................................................................
def display(inp):
    main_label.config(text=inp)
    return
#................................................................................................
def take_command():
	c = input("speak : ")
	c.lower()
	if bot_name.lower() in c:
		c = c.replace(bot_name.lower(), '')
	return c
#................................................................................................
def get_input():
	c = input("speak : ")
	c.lower()
	return c
#................................................................................................	
def debug(text):
	#replace print with talk ...
	display(text)
	print(text)
#................................................................................................

def create_note():
	debug("What would you like to name the file ?")
	fname = get_input()
	with open("jarvis_data.txt" , "a") as f:
		f.write(fname +"\n")

	with open(fname , "w") as f:
		debug("The contents tell ")
		contents = get_input()
		f.write(contents)
		debug("done")
		return
#........................................................................................
def help():	
	debug("Im {0} ,your personal assistant bot ,  i can do the following things......".format(bot_name))
	debug("Let me give you some commands to tryout...")
	for item in things_i_can_do:
		text = "I can {0}...".format(item)
		debug(text)
		time.sleep(3)
	debug("For extensive guide,  you can read the creators blog...")
	webbrowser.open("https://google.com")
	return
#........................................................................................
def make_reminder():
	
	try:
		with open("reminders.txt" ,"at") as f:
			debug("What do you want me remind of ?")
			reminder = get_input()
			f.write(reminder+"\n")
			f.close()
			return
	except:
		print("failed")
	return
#..........................................
def tell_reminders():
	def fetch_reminders():
		try:
			with open("reminders.txt" ,"r") as f:
				contents = f.readlines()
				data = list()
				for line in contents:
					d = line.split(",")
					data.append(d)
				f.close()
			return data
		
		except:
			debug("Failed ...")
	reminders = fetch_reminders()
	for r in reminders:
		r = r[0].replace("\n","")
		debug(r)
		
	debug("Thats all you have on your reminders .")
	return



def tell_weather():
	global user_location
	base_url = "http://api.openweathermap.org/data/2.5/weather?"
	api_key = "134a451988d0aa8311697d08a193490c"
	#complete_url = base_url + "appid=" + api_key + "&q=" + user_location
	complete_url = base_url + "q=" + user_location +"&appid=" + api_key
	#api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
	response = requests.get(complete_url)
	weather_data = response.json()
	print(weather_data)
	return

def search_wiki():
	debug("What you wanna search about ?")
	text = get_input()
	info = wikipedia.summary(text, 1)
	debug(info)

def tell_joke():
	joke = pyjokes.get_joke()
	debug(joke)

def send_mail():
	#fetching mail details........
	global user_name
	def fetch_mail_details():
		try:
			with open("mail_data.txt" , "r") as f:
				contents = f.readlines()
				data = list()
				for line in contents:
					d = line.split(",")
					data.append(d)
				
				f.close()
				return data
		except:
			debug("failed")
	
	data = fetch_mail_details()
	Sender_mail = data[0][0]
	Sender_password = data[0][1].replace("\n" , "")
	del data[0]
	recievers_list = dict()

	for line in data:
		nickname = line[0]
		mail_id = line[1].replace("\n", "")
		recievers_list[nickname] = mail_id
	debug("Do you wanna view the address book ?")
	wish = get_input()
	for item in yes_words:
		if(item in wish):
			for name in recievers_list.keys():
				debug(name)
	#data has been fetched now
	debug("To whom do wanna send mail ?")
	sender = get_input().lower()
	if(sender not in recievers_list.keys()):
		debug("That person is not in your address book ! Sorry try again")
		return
	Reciever_mail = recievers_list[sender]

	debug("Whats the subject line {0} ?".format(user_name))
	sub = get_input()

	debug("Whats the content ?")
	content = get_input()
	msg = MIMEMultipart()
	msg["Subject"] = sub
	text = content
	msg.attach(MIMEText(text))
	debug("Alright sending mail to {0}".format(sender))
	try:
		server = smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login(Sender_mail,Sender_password)
		server.sendmail(Sender_mail , Reciever_mail , msg.as_string())
	except:
		debug("Some error has happend ")
	else:
		debug("Mail sent successfully !")

	return
#.............end..of.....sendmail....................

def morning_routine():
	debug("Good {0} {1} !".format(part , user_name))
	debug("You have the following things on your reminders ")
	tell_reminders()
	#tell_weather()
	debug("Have a great day ahead")
	return



#........................end of functions.....................................


#....................................TKINTER..SETUP.....................................
canvas = tk.Tk()
canvas.title("JARVIS")
canvas.geometry("500x300")

main_label = tk.Label(text="command ")
main_label.config(bg= "white" ,fg="black",width = 80,height = 50,font=("arial",20))
main_label.pack()

data_label = tk.Label()
data_label.config(bg= "white" ,fg="black",width = 80,height = 50,font=("arial",20))
data_label.config(text="test")
data_label.pack()
#...........END OF TKNTER SETP.........................................................

#..........SPEECH RECOG SETUP........................................................
#insert here

#................END..........................................................................




#.......................||| Main function ||...............................................
run = True
fetch_details()
if(part =="morning"):
	morning_routine()
else:
	debug("Good {0} {1} , what can i do for you ?".format(part , user_name))

while(run):
	command = take_command()
	#.....closing the bot......................
	for item in exit_words :
		def quit():
				global run
				run = False
				m ="See you later {0} ".format(user_name)
				debug(m)
				time.sleep(5)
				exit()
				return
		if(item in command):
			quit()
			continue
	#...........................................
	for item in greeting_words:
		if(item in command):
			debug("Hi im {0}".format(bot_name))
			break	

	for item in help_words :
		if(item in command):
			help() 
	
	for item in take_note_words:
		if(item in command):
			create_note()

	for item in make_reminder_words:
		if(item in command):
			make_reminder()
	
	for item in tell_reminder_words:
		if(item in command):
			tell_reminders()
	
	for item in tell_weather_words :
		if(item in command):
			tell_weather()
	
	for item in search_wiki_words :
		if(item in command):
			search_wiki()
	
	for item in tell_joke_words :
		if(item in command):
			tell_joke()



	if("time" in command):
		time = datetime.datetime.now().strftime('%I:%M %p')
		debug('Current time is ' + time) 

	elif("kill" in command):
		kill_yourself()

	elif("send mail" in command):
		send_mail()

