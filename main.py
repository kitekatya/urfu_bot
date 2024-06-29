from bot import start
from server import keep_alive
import threading

server = threading.Thread(target=keep_alive)
bot = threading.Thread(target=start)

server.start()
bot.start()
