import asyncio
import websockets
import json
import vlc

conn = psycopg2.connect("dbname=Election user=postgres host='localhost' password=UBahn-Takustraße")
cur = conn.cursor()

async def bad_request(websocket):
    dataOut = {'msg': 'bad-request'}
    await websocket.send(dataOut)
    
async def process_request(websocket, path):
    print("new connection")
    while True:
        try:
            data = await websocket.recv()
        except:
            print("closed connection")
            return

        try:
            i = json.loads(data) # parsed input data
        except:
            return bad_request(websocket)

        if not 'msg' in i:
            return bad_request(websocket)

        if i['msg'] == 'ping':
            continue

        print("received request: {}".format(i))

        o = {'msg': i['msg']} # output data

        if i['msg'] == 'blub':
            o['data'] = blub()
        
        dataOut = json.dumps(o)
        await websocket.send(dataOut)
        
if __name__ == "__main__":
    try:
        start_server = websockets.serve(process_request, 'localhost', 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
