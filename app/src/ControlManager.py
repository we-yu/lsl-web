import DBController
import IconScraper
import re # 正規表現

class ControlManager:

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

    # Check that sticker URL is available one.
    def IsAvailableSticker(self, parentID):
        return parentID
    # If all fine, Target sticker register to DBs.
    def RegisterNewSticker2DB(self, parentID):
        return parentID