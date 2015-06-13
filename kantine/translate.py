# coding=utf-8

import requests

class Translator(object):
    def __init__(self, ip=None, email=None, key=None, api_url='http://api.mymemory.translated.net/get'):
        self.ip = ip
        self.email = email
        self.key = key
        self.api_url = api_url

    def translate(self, term, lang_from="de", lang_to="en"):
        req = requests.get(self.api_url, params={
            "q": term,
            "langpair": "{0}|{1}".format(lang_from, lang_to),
            "key": self.key,
            "ip": self.ip,
            "de": self.email
        })

        if not req.ok:
            raise req.text

        return req.json()[u'responseData'][u'translatedText']


if __name__ == '__main__':
    t = Translator()
    print(t.translate("Bohnensuppe mit Linsen und Wűrstchen"))
