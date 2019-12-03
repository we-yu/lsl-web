
import DBController
from pprint import pprint

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

        self.instances  = ('dbCtrl', DBController.DBCtrl)
        self.objects    = ('dbCtrl', self.instances['dbCtrl']())

    def GetParentIDs(self):
        parentIDs = []
        query = 'SELECT id, title FROM sticker_list'
        result = self.objects['dbCtrl'].Read(query)


        for sticker in result :
            print(sticker[0], sticker[1])
            stinfo = {}
            stinfo["id"] = sticker[0]
            stinfo["title"] = sticker[1]
            parentIDs.append(stinfo)

        return parentIDs

    def GetLocalIDs(self, parentID):
        query = 'SELECT local_id FROM sticker_detail WHERE parent_id=%s' % (parentID)
        print('query = ', query)

        result = self.objects['dbCtrl'].Read(query)

        localid_list = []
        child_list = []
        cnt = 0
        for local_id in result :
            cnt += 1
            child_list.append(local_id[0])
            if (cnt % 4) == 0 :
                localid_list.append(child_list)
                child_list = []

        # print("===================== : ")
        # print('query, result = ', query, '¥n', result)
        # print(" : =====================")


        return localid_list

