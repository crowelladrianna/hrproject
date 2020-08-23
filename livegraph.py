# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 23:33:34 2020

@author: crowe

Created using Bleak. For more information on installing and using Bleak, see:
https://bleak.readthedocs.io/en/latest/#
"""
from bleak import BleakClient
import asyncio

import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread

xs = []
ys = []
       
fig = plt.figure()
ax = fig.add_subplot(1,1,1) 

plt.ylim(60, 130)

'''
This is the specific address of our heart rate monitor. 
For the code used to find nearby bluetooth devices, see:
https://bleak.readthedocs.io/en/latest/scanning.html
'''
address = "C0:FE:D0:65:49:40"

recentPoint = 0

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    firstBit = data[0] & 0x01
    if(firstBit == 0):
        global recentPoint
        recentPoint = data[1]
        print(data[1])
        
def animate(i):
    global xs
    global ys
    
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(recentPoint)
    
    xs = xs[-20:]
    ys = ys[-20:]

    ax.clear()
    plt.ylim(60, 130)
    ax.plot(xs, ys)

async def gather_hrs(loop):
    async with BleakClient(address, loop=loop) as client:
        print(await client.is_connected())

        id = "00002a37-0000-1000-8000-00805f9b34fb"
        
        #services = await client.get_services()
        #char = services.get_characteristic(id)
        
        await client.start_notify(id, notification_handler)
        while True:
            time.sleep(1)
        await client.stop_notify(id)

  
def thr():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gather_hrs(loop))

def main():
    loop = asyncio.get_event_loop()
    t1=Thread(target=loop_in_thread, args=(loop,))
    t1.start()
    
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
    

main()
