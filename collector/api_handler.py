import requests, time

class API:
    def __init__(self, url, freq, name):
        self.url = url
        self.freq = freq
        self.name = name

class APIHandler:
    def __init__(self):
        self.api_list = []
        self.api_data = []
        
        f = open('api_config', 'r')
        lines = f.readlines()
        
        for i in range(len(lines)):
            url = lines[i].split(',')[0]
            freq = int(lines[i].split(',')[1])
            name = lines[i].split(',')[2]

            self.api_list.append(API(url, freq, name))
            self.api_data.append('')

    def handle_apis(self):
        start = time.time()
        while True:
            for i in range(len(self.api_list)):
                api = self.api_list[i]
                if int(time.time() - start) % api.freq == 0:
                    res = requests.get(api.url)
                    self.api_data[i] = res.text

    #TODO Define api parsers