from datetime import datetime
from threading import Timer
import os

x=datetime.today()
print(x)
y=x.replace(day=x.day, hour=10, minute=0, second=1)
delta_t=y-x

secs=delta_t.seconds+1

def run_algo():
  os.system('nohup python /root/HFT/Michigan/michigan.py')

t = Timer(secs, run_algo)
t.start()