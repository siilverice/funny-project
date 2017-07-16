from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
import requests

URL_KPLAN3 = "https://www.wealthmagik.com/FundInfo/FundProfile-KAsset-MIXBAL-K%20PLAN3-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B9%80%E0%B8%84%20%E0%B9%81%E0%B8%9E%E0%B8%A5%E0%B8%99%203"

ID_NAME_NAV_VALUE = "ctl00_ContentPlaceHolder1_lblNAV"
ID_NAME_NAV_CHANGED = "ctl00_ContentPlaceHolder1_lblNAVChange"

FUND_NAME = "KPLAN3"


class ReceiveDataView(RetrieveAPIView):
    def get(self, *args, **kwargs):
        r = requests.get(URL_KPLAN3)
        result = r.text
        soup = BeautifulSoup(result, 'html.parser')
        nav_value = soup.find(id=ID_NAME_NAV_VALUE).contents[0]
        nav_changed = float(soup.find(id=ID_NAME_NAV_CHANGED).contents[0].contents[0])
        data = {}

        if nav_changed < 0:
            data['value1'] = "Decrease"
        else:
            data['value1'] = "Increase"

        data['value2'] = nav_value
        data['value3'] = nav_changed

        webhook_url = "https://maker.ifttt.com/trigger/{}/with/key/jLXW-pdOf49SN2PvqvtchnD-3ZULlxoCtrY58Uo-lW5".format(FUND_NAME)
        requests.post(webhook_url, data)

        return Response(status=status.HTTP_200_OK, data=data)
