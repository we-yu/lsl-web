import DBController

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
