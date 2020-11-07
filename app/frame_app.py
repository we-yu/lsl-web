from flask import Flask, render_template, request

import sys
sys.path.append('src/')
import ControlManager

import pprint as pp

app = Flask(__name__)

ctrlMng = ControlManager.ControlManager()

@app.route('/')
def FrameSet(id = None):
    return render_template('FrameSet.html')

@app.route('/Top.html', methods = ['GET', 'POST'])
def Top(id = None):
    isValid, receivedTxt = ctrlMng.StickerFetching(request)

    return render_template('Top.html', responseMessage=receivedTxt, fetchResult=isValid)

@app.route('/ListMenu.html')
def ListMenu(nameTxt = None):
    sticker_infos = ctrlMng.GetParentIDs()
    sticker_infos = ctrlMng.InsertAccordionLine(sticker_infos)
    return render_template('ListMenu.html', menuList=sticker_infos)

@app.route('/IconList_<int:id>.html')
def IdSet(id = None):
    parentID = int(id)
    titleTxt = ctrlMng.GetStickerTitle(parentID)

    sticker_details = ctrlMng.GetLocalIDs(parentID)

    # pp.pprint(sticker_details)

    return render_template('ListBase.html', title=titleTxt, iconList=sticker_details)

if __name__ == "__main__":  # 実行されたら
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
