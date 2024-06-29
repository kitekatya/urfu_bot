from bot import start, start_update
from server import keep_alive
import threading

server = threading.Thread(target=keep_alive)
bot = threading.Thread(target=start)
update = threading.Thread(target=start_update)

server.start()
bot.start()
update.start()
