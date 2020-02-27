import asyncio
import websockets
import numpy as np
import time

startTime = time.time()

async def hello(websocket, path):
    while True:
        
        dataFile = open("./data.txt",'r')
        dataRaw = dataFile.readline()
        dataRaw = str(dataRaw)
        dataStream = dataRaw.split(":")

        if(len(dataStream) > 0):
            firstData = dataStream[0][1:-1]
            firstData = firstData.split(",")
            displacement = int(firstData[1]) 

        inpStream = ""
        for data in dataStream:
            data = data[1:-1]
            data = data.split(",")
            inp = data[0]
            timestep = int(data[1]) 

            curTime = 3000000*(time.time() - startTime) + displacement

            if(curTime > timestep):
                inpStream += inp

        print(inpStream + " | " + str(curTime))
        await websocket.send(inpStream)
        time.sleep(0.2)

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()