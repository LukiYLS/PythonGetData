import urllib.request
import gzip 
import json
import os
import threading
import ssl

def makeDir(path):
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def getAbsolutePath(dir, name):
    return os.path.abspath(os.path.join(dir, name))

def requestUrl(url):
    print(url)
    header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"}    
    request=urllib.request.Request(url,headers=header)    
    response=urllib.request.urlopen(request)  
    html = response.read()
    content = gzip.decompress(html).decode("utf-8")
    return content
def requestBinary(url):
    print(url)
    header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"}    
    request=urllib.request.Request(url,headers=header)    
    response=urllib.request.urlopen(request)  
    html = response.read()
    #content = gzip.decompress(html).decode("utf-8")
    return html
def saveFile(content, path, name):
    makeDir(path)
    filePath = getAbsolutePath(path, name)
    fp = open(filePath, "w")
    fp.write(content)
    fp.close()

def saveFileB(content, absPath):
    makeDir(getAbsolutePath(absPath, "../")) 
    fp = open(absPath, "wb+")
    fp.write(content)
    fp.close()
def downloadTileJson(url, NodeList):
    #下载tileset.json文件
    content = requestUrl(url + token)
    info = json.loads(content)
    saveFile(content, rootPath, "tileset.json")    
    #解析根节点所有子节点信息,并得到所有子节点url
    root = info["root"]
    rootUrl = root["content"]["url"]
    NodeList.append(rootUrl)  
    stack = [root]
    while stack:
        node = stack.pop()
        children = node["children"]
        if children is not None:
            for child in children:
                childUrl = child["content"]["url"]
                NodeList.append(childUrl) 
                stack.append(child)   
            
def downloadB3DM(relativeUrl):
    completeUrl = urllib.parse.urljoin(url, relativeUrl)
    content = requestBinary(completeUrl + token)    
    absPath = getAbsolutePath(rootPath, relativeUrl)
    saveFileB(content,absPath)



#存储位置
rootPath = "F:\model\\"
#模型url地址
url = "https://beta.cesium.com/api/assets/1458/"
#进行身份验证时需要
token = "?access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxYmJiNTAxOC1lOTg5LTQzN2EtODg1OC0zMWJjM2IxNGNlYmMiLCJpZCI6NDQsImFzc2V0cyI6WzE0NThdLCJpYXQiOjE0OTkyNjM4MjB9.1WKijRa-ILkmG6utrhDWX6rDgasjD7dZv-G5ZyCmkKg"

NodeList = []
downloadTileJson(urllib.parse.urljoin(url,"tileset.json"), NodeList)



class downloadThreadManager (threading.Thread):
    def __init__(self, threadNum):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
    def run(self):
        print ("开始线程")
        while bFlag == True:
            if len(NodeList)>0 and  threading.active_count()<self.threadNum+1:
                mutex.acquire()
                nodeUrl = NodeList.pop()
                mutex.release()
                tdID = threading.Thread(target=downloadB3DM,args=(nodeUrl,))
                tdID.start()

mutex = threading.Lock()

th = downloadThreadManager(2)
th.start()
while len(NodeList)>0:
    bFlag = True

bFlag = False
