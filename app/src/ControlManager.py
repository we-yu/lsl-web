import DBController
import IconScraper
import re # 正規表現

from pprint import pprint

class ControlManager:
    STICKER_FIXED_URL = 'https://store.line.me/stickershop/product/%s/en'

    @property
    def instances(self):
        return self.__instances
    @instances.setter
    def instances(self, value):
        key = value[0]
        val = value[1]
        self.__instances[key] = val

    @property
    def objects(self):
        return self.__objects
    @objects.setter
    def objects(self, value):
        key = value[0]
        val = value[1]
        self.__objects[key] = val

    def __init__(self):
        print('Call ' + self.__class__.__name__ + ' Constructor')
        self.__instances    = {}
        self.__objects      = {}

        self.instances  = ('dbCtrl',    DBController.DBCtrl)
        self.instances  = ('scrp',      IconScraper.IconScraper)

        self.objects    = ('dbCtrl', self.instances['dbCtrl']())

    def GetParentIDs(self):
        parentIDs = []

        # Execute query, Get all parentIDs from table
        query = 'SELECT id, title FROM sticker_list'
        result = self.objects['dbCtrl'].Read(query)

        # Loop executed result. Make list of {id, title} dictionaries.
        for sticker in result :
            stinfo = {}
            stinfo["id"] = sticker[0]
            stinfo["title"] = sticker[1]
            parentIDs.append(stinfo)

        return parentIDs

    def GetLocalIDs(self, parentID):
        # Execute query. Get all of "local id" from "detail" table.
        query = 'SELECT local_id FROM sticker_detail WHERE parent_id=%s' % (parentID)
        result = self.objects['dbCtrl'].Read(query)

        # Make list in list. Every 4 times change line.
        # [[1, 2, 3, 4], [5, 6, 7, 8] ...]
        localid_list = []
        child_list = []
        cnt = 0
        for local_id in result :
            cnt += 1
            child_list.append(local_id[0])
            if (cnt % 4) == 0 :
                localid_list.append(child_list)
                child_list = []

        return localid_list

    # To new register, Input sticker-ID.
    # https://store.line.me/stickershop/product/1206683/en => 1206683 is sticker-ID
    def IsNumeric(self, val):
        return re.match(r"^\d+$", val) is not None

    # Check that Sticker already downloaded and registered in DB
    def IsAlreadyInDB(self, parentID):
        query = 'SELECT count(id) FROM sticker_list WHERE id=%s' % parentID
        result = self.objects['dbCtrl'].Read(query, 'count')
        return True if result == 1 else False

    def CookYummySoup(self, parentID):
        # Make target url from fixed url + input parent ID
        tgtStiUrl = self.STICKER_FIXED_URL % parentID
        # Make scraper object. Same time, Do scraping. This is only 1 time per object.
        self.objects = ('scrp', self.instances['scrp'](tgtStiUrl))
        scraper = self.objects['scrp']

        # Check this URL is available or not.
        isValid = scraper.IsVaild()

        # iconInfos =
        # LocalID   {'id': '121193446',
        # L size     'staticUrl': 'https://stickershop.line-scdn.net/stickershop/v1/sticker/121193446/iPhone/sticker@2x.png',
        # M size     'fbStaticUrl': 'https://stickershop.line-scdn.net/stickershop/v1/sticker/121193446/android/sticker.png',
        # S size     'backGroundUrl': 'https://stickershop.line-scdn.net/stickershop/v1/sticker/121193446/iPhone/sticker_key@2x.png'},
        if (isValid == True) :

            vals4list = [parentID, tgtStiUrl, scraper.GetStickerTitle(), ""]
            vals4detail = []
            print("vals4list = ", vals4list)

            iconInfos = scraper.GetAllIconURL()

            for iconInfo in iconInfos :
                val4detail = (parentID, iconInfo['id'], iconInfo['staticUrl'], iconInfo['fbStaticUrl'], iconInfo['backGroundUrl'])
                vals4detail.append(val4detail)
            pprint(vals4detail[0])
            pprint(vals4detail[1])
            pprint(vals4detail[2])

            query = 'INSERT INTO sticker_list VALUES(%s, \'%s\', \'%s\', \'%s\')' % (vals4list[0], vals4list[1], vals4list[2], vals4list[3])
            self.objects['dbCtrl'].Create(query)
            query = 'INSERT INTO sticker_detail VALUES (?, ?, ?, ?, ?)'
            self.objects['dbCtrl'].Create(query, vals4detail, 'many')


            # print(iconInfos)

        return parentID

    # Check that sticker URL is available one.
    def IsAvailableSticker(self, parentID):
        return parentID
    # If all fine, Target sticker register to DBs.
    def RegisterNewSticker2DB(self, parentID):
        return parentID