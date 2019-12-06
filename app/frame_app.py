from flask import Flask, render_template, request

import sys
sys.path.append('src/')
import ControlManager

app = Flask(__name__)

ctrlMng = ControlManager.ControlManager()

@app.route('/')
def FrameSet(id = None):
    return render_template('FrameSet.html')

@app.route('/Top.html', methods = ['GET', 'POST'])
def Top(id = None):
    receivedTxt = ""
    if request.method == 'POST' :
        result = request.form
        receivedTxt = str(result["url_post_text"])
        if ctrlMng.IsNumeric(receivedTxt) == True :
            exist = ctrlMng.IsAlreadyInDB(int(receivedTxt))
            if exist == False :
                stickerID = receivedTxt
                vaild = ctrlMng.CookYummySoup(stickerID)
        else :
            receivedTxt = "<font color=\"red\"><b>%s</b> is invalid. Allow only numeric.</font>" % (receivedTxt)

    return render_template('Top.html', responseMessage=receivedTxt)

@app.route('/ListMenu.html')
def ListMenu(nameTxt = None):
    sticker_infos = ctrlMng.GetParentIDs()
    sticker_infos = ctrlMng.InsertAccordionLine(sticker_infos)
    return render_template('ListMenu.html', menuList=sticker_infos)

@app.route('/IconList_<int:id>.html')
def IdSet(id = None):
    parentID = int(id)
    titleTxt = int(id)

    sticker_details = ctrlMng.GetLocalIDs(parentID)
    print(sticker_details)

    return render_template('ListBase.html', title=titleTxt, iconList=sticker_details)

if __name__ == "__main__":  # 実行されたら
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
