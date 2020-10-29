import time
import telepot

f=open("/home/pi/autodoorbell/token.txt", "r")
contents =f.read()
contents = contents.strip()
#print(contents)

bot = telepot.Bot(contents)

print('Starting handler thread')
print('AutoHomePiBot is up')


def send():
	print('sending pic via def send')
	bot.sendPhoto(<put id here>, open('/home/pi/motion/lastsnap.jpg', 'rb'))
