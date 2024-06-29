from bot import start, auto_update
from server import keep_alive
import threading

server = threading.Thread(target=keep_alive)
bot = threading.Thread(target=start)
update = threading.Thread(target=auto_update)

server.start()
bot.start()
update.start()
