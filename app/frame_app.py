from flask import Flask, render_template
import sys
sys.path.append('src/')
import ControlManager

app = Flask(__name__)

ctrlMng = ControlManager.ControlManager()

@app.route('/')
def FrameSet(id = None):
    return render_template('FrameSet.html')

@app.route('/Top.html')
def Top(id = None):
    return render_template('Top.html')

@app.route('/ListMenu.html')
def ListMenu(nameTxt = None):
    sticker_infos =  [
                {"id":"1206683", "title":"Poputepipick"},
                {"id":"1252985", "title":"Poputepipick 2"},
                {"id":"1412535", "title":"Poputepipick 3"}
            ]
    return render_template('ListMenu.html', menuList=sticker_infos)

@app.route('/IconList_<int:id>.html')
def IdSet(id = None):
    titleTxt="Lorem"
    parentID = int(id)

    sticker_details = ctrlMng.GetLocalIDs(parentID)
    print(sticker_details)

    return render_template('ListBase.html', title=titleTxt, iconList=sticker_details)

if __name__ == "__main__":  # 実行されたら
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)


