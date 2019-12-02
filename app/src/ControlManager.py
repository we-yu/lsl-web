class ControlManager:

    def __init__(self):
        print('Call ' + self.__class__.__name__ + ' Constructor')

    def GetLocalIDs(self, parentID):

        if (parentID == 1206683) :
            cnt = 8395708
            localid_list = []
            child_list = []
            for i in range(10):
                for j in range(4):
                    child_list.append(cnt)
                    cnt += 1
                localid_list.append(child_list)
                child_list = []
        elif (parentID == 1252985) :
            cnt = 10260256
            localid_list = []
            child_list = []
            for i in range(10):
                for j in range(4):
                    child_list.append(cnt)
                    cnt += 1
                localid_list.append(child_list)
                child_list = []
        elif (parentID == 1412535) :
            cnt = 15879266
            localid_list = []
            child_list = []
            for i in range(10):
                for j in range(4):
                    child_list.append(cnt)
                    cnt += 1
                localid_list.append(child_list)
                child_list = []
        else :
            cnt = parentID
            localid_list = []
            child_list = []
            for i in range(4):
                for j in range(4):
                    child_list.append(cnt)
                    cnt += 1
                localid_list.append(child_list)
                child_list = []

        return localid_list

