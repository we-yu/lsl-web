# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import re
import json

STICKER_LIST_CLASS  = 'FnStickerList'
UNVLAID_PAGE_MARK   = 'lyMainError'

class IconScraper :
    #   Setting property -------------------------------
    # bs4 object
    @property
    def soup(self):
        return self.__soup
    @soup.setter
    def soup(self, value):
        self.__soup = value

    # Scraping target URL
    @property
    def tgtUrl(self):
        return self.__tgtUrl
    @tgtUrl.setter
    def tgtUrl(self, value):
        self.__tgtUrl = value

    # Sticker's top ID
    @property
    def topId(self):
        return self.__topId
    @topId.setter
    def topId(self, value):
        self.__topId = value

    # Sticker's detail ID
    @property
    def detailId(self):
        return self.__detailId
    @detailId.setter
    def detailId(self, value):
        self.__detailId = value
    #   ------------------------------------------------

    def __init__(self, url):
        # print('Call ' + self.__class__.__name__ + ' Constructor')

        # Scraping target url
        self.tgtUrl = url

        # Request page and get parser
        sticker_req  = requests.get(self.tgtUrl)
        # HTMLパーサー解析済みデータ
        self.soup = BeautifulSoup(sticker_req.content, 'html.parser')
        # StickerID
        # self.topId = self.GetStickerTopID()

    # If there is text of "UNVALID_PAGE_MARK" in page, You got error page.
    def IsVaild(self):
        contentsStr = str(self.soup)

        # ogContent = self.soup.find('meta', {"property":"og:url"})['content']
        # print("ogContent = ", ogContent)

        return True if UNVLAID_PAGE_MARK not in contentsStr else False

    def GetAllIconURL(self):
        # print('Call ' + sys._getframe().f_code.co_name)

        sticker_title = self.GetStickerTitle()

        # Top of icons <ul> has 2 classes. Always has STICKER_LIST_CLASS
        # <ul class="mdCMN09Ul FnStickerList">
        # Get First class text
        re_condition = r'^.*' + STICKER_LIST_CLASS + '.*$'
        stickerBox = self.soup.find('ul', class_=re.compile(re_condition))
        tgtClass = stickerBox['class'][0]

        # Extract detail-ID from class text
        re_condition = r'^(?P<detailId>.*)Ul$'
        self.detailId = re.search(re_condition, tgtClass)['detailId']

        # Each icons set under <li class="(detail-ID)Li"> tags
        detailId_li = self.detailId + 'Li'
        stickerList = self.soup.find_all('li', class_=detailId_li)

        iconUrls = []
        for iconLi in stickerList :
            # <Li> class has custom attributes. Extract that and convert from JSON text to dictionary type.
            # 'type', 'id', 'staticUrl' ...
            # https://www.lisz-works.com/entry/python-convert-json-dict
            data_preview = iconLi.get('data-preview')
            data_preview = json.loads(data_preview)

            # print(data_preview)

            # Get static/fallback url. Get small-size icon url from static.
            staticUrl = data_preview['staticUrl'].split(';')[0]
            fallbackStaticUrl = data_preview['fallbackStaticUrl'].split(';')[0]
            # Make background-image URL
            backgroundUrl = staticUrl.replace('@', '_key@')
            # Set Id and url into dictionary, Then append to array. This is return value.
            iconInfo = {'id':data_preview['id'], 'staticUrl':staticUrl, 'fbStaticUrl':fallbackStaticUrl, 'backGroundUrl':backgroundUrl}
            iconUrls.append(iconInfo)

        return iconUrls

    def GetStickerTopID(self) :
        # Extract Sticker ID (Might be all stickers manages by this ID)

        # Make ID condition (名前付きキャプチャグループ)
        re_condition = r'^(?P<sticker_id>.*)Item01$'
        sticker_top = self.soup.find('ul', class_=re.compile(re_condition))
        classText = str(sticker_top.ul['class'][0])
        re_condition = r'^(?P<sticker_id>.*)Item01.*'
        id = re.search(re_condition, classText)['sticker_id']

        return id

    def GetStickerDetailId(self) :
        id = ''
        return id

    def GetStickerTitle(self) :
        title = self.soup.select('p.mdCMN38Item01Ttl')
        title = title[0].getText()
        return title



