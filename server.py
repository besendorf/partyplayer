import asyncio
import websockets
import json
import vlc
from Queue import PriorityQueue
from __future__ import unicode_literals
import youtube_dl

class Server(object):

    # Logger class for youtube-dl module
    class YtLogger(object):
        def debug(self, msg):
            pass
        
        def warning(self, msg):
            pass
        
        def error(self, msg):
            print(msg)
    
    def ___init__(self):    
        self.songs = PriorityQueue()
        self.database = {}
        self.current_id = 0
        self.ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',}],
                'logger': YtLogger(),
                'progress_hooks': [Yt_hook],}
        
    '''
    Define asyncio coroutines
    '''
    
    # handles failed resquest
    async def bad_request(self, websocket):
        dataOut = {'msg': 'bad-request'}
        await websocket.send(dataOut)
    
    # processes client requests to server
    async def process_request(self, websocket, path):
        print("new connection")
        while True:
            # wait for client data
            try:
                data = await websocket.recv()
            except:
                print("closed connection")
                return
        
            # parse data
            try:
                i = json.loads(data) # parsed input data
            except:
                return self.bad_request(websocket)
        
            # handle parsed data
            if not 'msg' in i:
                return self.bad_request(websocket)
        
            print("received request: {}".format(i))
        
            o = {'msg': i['msg']} # output data
        
            # invoke coroutines
            if i['msg'] == 'login':
                o['data'] = self.login()
            elif i['msg'] == 'add':
                o['valid'] = self.add(i['url'])
            elif i['msg'] == 'list':
                o['songs'] = self.list()
            
            # compose return data
            dataOut = json.dumps(o)
            # return data to client
            await websocket.send(dataOut)
        
    '''
    Define client callbacks invoked by process_request
    '''
    
    # add new url
    def add(self, url):
        # check if song is already downloaded
        if url not in self.database:
            self.database[url] = Song(url)
            # download song
            self.database[url].path = await self.download(url)
        
    async def download(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])
        
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
