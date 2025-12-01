import threading
from datetime import datetime,timedelta

class Defense:
    def __init__(self):
        t1 = threading.Thread(target=self.keep)
        t1.start()
    def keep(self):
        time = datetime.now()
        while True:
            if datetime.now() > time + timedelta(seconds=20):
                print("Passou 20 s")
                time = datetime.now()

defs = Defense()