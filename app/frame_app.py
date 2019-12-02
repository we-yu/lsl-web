from flask import Flask, render_template
import sqlite3
import pprint

app = Flask(__name__)

@app.route('/')
def FrameSet(id = None):
    return render_template('FrameSet.html')

@app.route('/ListMenu.html')
def ListMenu(nameTxt = None):
    sticker_infos =  [
                {"id":"1206683", "title":"Poputepipick"},
                {"id":"1252985", "title":"Poputepipick 2"},
                {"id":"1412535", "title":"Poputepipick 3"}
            ]
    return render_template('ListMenu.html', menuList=sticker_infos)

@app.route('/ListBase.html')
def ListBase(nameTxt = None):
    titleTxt="Lorem"
    sticker_details =  [
                (8395708, 8395709, 8395710, 8395711),
                (8395712, 8395713, 8395714, 8395715),
                (8395716, 8395717, 8395718, 8395719)
            ]
    return render_template('ListBase.html', title=titleTxt, iconList=sticker_details)

@app.route('/<int:id>')
def IdSet(id = None):
    titleTxt="Lorem"
    startID = int(id)
    sticker_details = []
    child_list = []

    cnt = startID
    for i in range(4) :
        for j in range(3) :
            child_list.append(cnt)
            cnt+=1
        sticker_details.append(child_list)
        child_list = []
    print(sticker_details)

    return render_template('ListBase.html', title=titleTxt, iconList=sticker_details)


if __name__ == "__main__":  # 実行されたら
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)


