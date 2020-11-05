# import DBController
import DBStateController
import IconScraper

import string
import re # 正規表現

from pprint import pprint
from Logger import Logger
from Logger import ListLogger

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

        self.instances  = ('scrp',      IconScraper.IconScraper)
        # self.instances  = ('dbCtrl',    DBController.DBCtrl)
        #
        # self.objects    = ('dbCtrl', self.instances['dbCtrl']())

        # # DB State Select
        self.instances  = ('DBState', DBStateController.DBContext)
        self.objects    = ('DBState', self.instances['DBState']())
        self.objects['DBState'].change_state("mongodb")

    def GetParentIDs(self):
        parentIDs = []

        inquery = {
            "collection": "sticker_list",
            "projection": {
                "id": 1,
                "title": 1
            },
            "selection": {},
            "sort": {
                "key": "title",
                "direction": 1
            },
            "limit": 0
        }

        mongoRet = self.objects['DBState'].Read(inquery)
        result = []
        for find in mongoRet:
            result.append((find["id"], find["title"]))

        # for r in result:
        #     Logger(r)
        
        # Execute query, Get all parentIDs from table
        # query = 'SELECT id, title FROM sticker_list ORDER BY title'
        # result = self.objects['dbCtrl'].Read(query)

        # Loop executed result. Make list of {id, title} dictionaries.
        for sticker in result :
            # Logger(sticker)
            stinfo = {}
            stinfo["id"] = sticker[0]
            stinfo["title"] = sticker[1]
            stinfo["class"] = ""
            parentIDs.append(stinfo)

        Logger("parentIDs =")
        ListLogger(parentIDs)

        return parentIDs

    # メニュー用辞書リストの適切な位置にアコーディオン用の列を挿入する。
    # リスト自体はORDER BY titleで取得しているため、英数字→a-zの順番にはすでになっている。
    def InsertAccordionLine(self, stlist):

        menuIdx = 0         # メニューリストをたどるIndex
        numMarkList = []    # 頭文字英数字のものはこちらへ移動
        newStList = []      # 適当にAccordionを入れた新メニューリスト

        # 頭文字英数字のものはいったん別リストへ退避
        alphaReg = re.compile(r'^[a-zA-Z]+$')
        while not alphaReg.match(stlist[0]['title'][0]) :
            numMarkList.append(stlist.pop(0))

        # a-zの文字列を基準にループを回す
        for alp in string.ascii_lowercase :
            # まずは現在のアルファベットでaccordion用要素を作る
            accLine = {'id': -1, 'title': alp, 'class': 'accordion-start'}
            newStList.append(accLine)

            lastIdx = menuIdx
            # メニュー用Indexがメニュー配列を超えていない・かつ現在参照しているメニュー要素の文字列が現在アルファベットと同じ限りループを回す
            while ((menuIdx < len(stlist)) and (alp == stlist[menuIdx]['title'][0].lower())) :
                # 当該要素を新メニューリストへ挿入し、参照用Indexを一つすすめる。
                newStList.append(stlist[menuIdx])
                menuIdx += 1

            accLine = {'id': -1, 'title': alp, 'class': 'accordion-end'}
            newStList.append(accLine)

            # If nothing any menu read, delete accordion start/end line.
            if(lastIdx == menuIdx) :
                newStList.pop(len(newStList) - 1)
                newStList.pop(len(newStList) - 1)

        # 新メニューリストの後ろへ英数字用のAccordionと要素を連結する。
        if (len(numMarkList) != 0) :
            accLine = {'id': -1, 'title': "Numbers & Other", 'class': 'accordion-start'}
            newStList.append(accLine)

            newStList.extend(numMarkList)

            accLine = {'id': -1, 'title': "", 'class': 'accordion-end'}
            newStList.append(accLine)

        ListLogger(newStList)
        return newStList

    def GetLocalIDs(self, parentID):

        inquery = {
            "collection": "sticker_detail",
            "selection": {
                "id.parent": parentID
            },
            "projection": {
                "id.child":1
            },
            "sort": {
                "key": "id.child",
                "direction": 1
            },
            "limit": 0
        }

        mongoRet = self.objects['DBState'].Read(inquery)
        # Logger("MongoDB Result ↓")
        result = []
        for find in mongoRet:
            result.append((find["id"]["child"],))
            # Logger("Mongo Find :", find)

        # Execute query. Get all of "local id" from "detail" table.
        query = 'SELECT local_id FROM sticker_detail WHERE parent_id=%s ORDER BY local_id' % (parentID)
        # result = self.objects['dbCtrl'].Read(query)
        # for find in result:
        #     Logger("SQL Find :", find)

        # Logger("SQL Result =", result)

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

    def StickerFetching(self, req):
        Logger("Req = ", req, req.method)

        validate = True
        # Method check, If it is "POST". Allowed.
        validate = (req.method == "POST") if (validate == True) else False
        if (validate == True) :
            stickerID = str(req.form["url_post_text"])
            isValid, msg = self.ValidationID(stickerID)
        else :
            isValid = False
            msg = ""

        if (isValid) :
            # Valid page check
            isValid, msg = self.CookYummySoup(stickerID) if (validate == True) else (False, msg)
            Logger("Cook soup", isValid, msg)

        return isValid, msg

    def ValidationID(self, stickerID):

        validate = True

        # Numeric check
        validate, msg = self.IsNumeric(stickerID) if (validate == True) else (False, False)
        Logger("Numeric check", validate, msg)

        stickerID = int(stickerID)

        # Duplicate check
        validate, msg = self.IsDuplicate(stickerID) if (validate == True) else (False, msg)

        Logger("Duplicate check", validate, type(validate), msg)

        return validate, msg

    # To new register, Input sticker-ID.
    # https://store.line.me/stickershop/product/1206683/en => 1206683 is sticker-ID
    def IsNumeric(self, val):
        isValid = re.match(r"^\d+$", val) is not None
        msg = "<font color=\"red\"><b>%s</b> is invalid. Allow only numeric.</font>" % (val)
        return (isValid, msg)

    def IsDuplicate(self, parentID):
        inquery = {
            "collection": "sticker_list",
            "selection": {
                "id": parentID
            },
            "count": 1
        }

        listCount = self.objects['DBState'].Read(inquery)
        Logger("ListCount = ", listCount, type(listCount), bool(listCount))
        msg = "<font color=\"red\"><b>%s</b> is already in DB.</font>" % (parentID)

        return (not bool(listCount), msg)

    # def IsAlreadyInDB(self, parentID):
    #     query = 'SELECT count(id) FROM sticker_list WHERE id=%s' % parentID
    #     result = self.objects['dbCtrl'].Read(query, 'count')
    #     return True if result == 1 else False

    def CookYummySoup(self, parentID):
        # Make target url from fixed url + input parent ID
        tgtStiUrl = self.STICKER_FIXED_URL % parentID
        # Make scraper object. Same time, Do scraping. This is only 1 time per object.
        self.objects = ('scrp', self.instances['scrp'](tgtStiUrl))
        scraper = self.objects['scrp']

        # Check this URL is available or not.
        isValid, errMsg = scraper.IsValid()

        # Optional messages to return
        optMsg = ""

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

            inserts = []

            for iconInfo in iconInfos :
                # Create list for SQL
                val4detail = (parentID, iconInfo['id'], iconInfo['staticUrl'], iconInfo['fbStaticUrl'], iconInfo['backGroundUrl'])
                vals4detail.append(val4detail)

                # Create list for MongoDB
                detail_dic = {
                    "id": {
                        "parent": int(parentID),
                        "child": int(iconInfo['id'])
                    },
                    "iconUrl": {
                        "L": iconInfo['staticUrl'],
                        "M": iconInfo['fbStaticUrl'],
                        "S": iconInfo['backGroundUrl']
                    }
                }

                inserts.append(detail_dic)

            # pprint(vals4detail[0])
            # pprint(vals4detail[1])
            # pprint(vals4detail[2])

            inquery_list = {
                "collection": "sticker_list",
                "insert": [
                    {
                        "id":       int(vals4list[0]),
                        "url":      vals4list[1],
                        "title":    vals4list[2],
                        "comment":  vals4list[3]
                    }
                ]
            }

            Logger("List Inquery =", inquery_list)
            # Logger("type", type(inquery_list["insert"][0]["id"]))

            inquery_detail = {
                "collection": "sticker_detail",
                "insert": inserts
            }

            Logger("Detail Inquery =", inquery_detail)
            # Logger("type 0", type(inquery_detail["insert"][0]["id"]["parent"]), type(inquery_detail["insert"][0]["id"]["child"]))

            result = self.objects['DBState'].Create(inquery_list)
            Logger("Insert List Count =", len(result))
            result = self.objects['DBState'].Create(inquery_detail)
            Logger("Insert Detail Count =", len(result))

            # query = 'INSERT INTO sticker_list VALUES(%s, \'%s\', \'%s\', \'%s\')' % (vals4list[0], vals4list[1], vals4list[2], vals4list[3])
            # self.objects['dbCtrl'].Create(query)
            # query = 'INSERT INTO sticker_detail VALUES (?, ?, ?, ?, ?)'
            # self.objects['dbCtrl'].Create(query, vals4detail, 'many')

            fetchedTitle = vals4list[2]
            optMsg = "<font color=\"blue\">Sticker [<b>%s</b>] succeeded to fetching</font>" % (fetchedTitle)
        else:
            optMsg = "<font color=\"red\">Sticker <b>%s</b> could not found.</font>" % (parentID)
            errMsg_Formatted = "<pre>" + errMsg + "</pre>"
            optMsg = optMsg + errMsg_Formatted + "<hr>"

        return isValid, optMsg

    def GetStickerTitle(self, parentID):

        inquery = {
            "collection": "sticker_list",
            "selection": {
                "id": parentID
            },
            "projection": {
                "title":1
            }
        }

        mongoRet = self.objects['DBState'].Read(inquery)
        return mongoRet[0]["title"]

        # query = 'SELECT title FROM sticker_list WHERE id = %s' % parentID
        # titleTxt = self.objects['dbCtrl'].Read(query)
        # return titleTxt[0][0]
