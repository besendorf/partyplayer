import asyncio
import websockets
import json
import vlc
from Queue import PriorityQueue
from __future__ import unicode_literals
import youtube_dl

songs = PriorityQueue()

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': YtLogger(),
    'progress_hooks': [Yt_hook],
}

class YtLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
        
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

        if i['msg'] == 'login':
            o['data'] = login()
            
        elif i['msg'] == 'add':
            o['valid'] = add(i['url'])
        
        dataOut = json.dumps(o)
        await websocket.send(dataOut)
        
def add(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    songs.put({
        'url' : url
        'votes' : 0
            })
    
def Yt_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')    

if __name__ == "__main__":
    try:
        start_server = websockets.serve(process_request, 'localhost', 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
