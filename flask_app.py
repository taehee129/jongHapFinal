from flask import Flask , render_template , url_for, flash, redirect, json , jsonify, request, session
import Model.Translate as Translate
import Service.TranslateSer as TranSer
import Service.BoardSer  as bs
import Model.Crawler as cw
from Model import Dac as dac
app = Flask(__name__)

app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'
app.secret_key = 'My_key'

@app.route('/')
def home():   
    return render_template('jonghap/wordTest.html')


@app.route('/doEnquiry', methods=["GET", "POST"])
def doEnquiry() :

    cate = request.form['cate']
    text = request.form['text']
    memNo= 0
    if 'id' in session :
        memNo = session['memNo']

    dac.Dac().insertEnquiry(memNo, cate, text)

    return redirect(url_for('enquiryPage'))


@app.route('/doCoachLog', methods=["GET", "POST"])
def doCoachLog() :
    data = json.loads(request.data)
    quizNo = data.get('quizNo')
    isTrue = data.get('isTrue')

    if 'id' in session :
        memNo = session['memNo']

        dac.Dac().insertQuizLog(quizNo, memNo, isTrue)

    return []

@app.route('/doTestLog', methods=["GET", "POST"])
def doTestLog() :
    data = json.loads(request.data)
    testNo = data.get('testNo')
    isTrue = data.get('isTrue')

    if 'id' in session :
        memNo = session['memNo']

        dac.Dac().insertTestLog(testNo, memNo, isTrue)

    return []



@app.route('/doWordTest', methods=["GET", "POST"])
def doWordTest() :
    data = json.loads(request.data)
    testId = data.get('testId')
    memNo =0
    if 'id' in session :
        memNo = session['memNo']   
    return jsonify(dac.Dac().selectWordTest(testId,memNo))


@app.route('/wordTestPage', methods=["GET", "POST"])
def wordTestPage() :
    testId = request.args.get('testId')

    if testId is None or testId == '' :
        testId = 0
    return render_template('jonghap/wordTest.html', testId=testId)


@app.route('/wordCoachPage', methods=["GET", "POST"])
def wordCaochPage() :
    quizNo = request.args.get('quizNo')
    if quizNo is None or quizNo == '' :
        quizNo = 0
    return render_template('jonghap/wordCoach.html', firstQuizNo= quizNo)

@app.route('/doWordCoach', methods=["GET", "POST"])
def doWordCoach() :
    data = json.loads(request.data)
    quizNo = data.get('quizNo')
    memNo =0
    if 'id' in session :
        memNo = session['memNo']   
    return jsonify(dac.Dac().selectWordCoach(quizNo, memNo))


@app.route('/dictPage', methods=["GET", "POST"])
def dictPage() :
    
    text = request.args.get('text')
    targetLang = request.args.get('targetLang')
    
    if text == None :
        text = ''
        targetLang =''

    return render_template('jonghap/dict.html', text = text, targetLang=targetLang)

@app.route('/loginPage', methods=["GET", "POST"])
def loginPage() :
    return render_template('jonghap/login.html')


@app.route('/logout', methods=["GET", "POST"])
def logout() :
    if session['id'] :
        session.pop('memNo', None)
        session.pop('id', None)
        session.pop('nickName', None)
        session.pop('email', None)
        session.pop('lang', None)
        session.pop('insertDate', None)
    return redirect(url_for('board'))


@app.route('/login', methods=["GET", "POST"])
def login() : 
    id = request.form['id']
    password = request.form['password']
    member = dac.Dac().login(id,password )
    if not member : 
        'alter("아이디 혹인 비밀번호가 틀렸습니다.")'

    session['memNo'] = member.memNo   
    session['id'] = member.id 
    session['nickName'] = member.nickName
    session['name'] = member.name
    session['email'] = member.email
    session['lang'] = member.lang
    session['insertDate']= member.insertDate

    return redirect(url_for('board'))


@app.route('/mypage', methods=["GET", "POST"])
def mypage() : 
    data = dac.Dac()
    memNo = session['memNo']
    searchList = data.selectSearchLog(session['memNo'])
    wordTestList = data.seleteTestLog(memNo)
    wordCoachList = data.selectCoachLog(memNo)
    enquiryList = data.selectEnquiry(memNo)
    tranList = data.selectTranLog(memNo)
    
    return render_template('jonghap/mypage.html', session=session, searchList=searchList, wordTestList=wordTestList, enquiryList= enquiryList, wordCoachList = wordCoachList, tranList=tranList)

@app.route('/plusRecommend', methods=["GET", "POST"])
def plusRecommend() : 
    data = json.loads(request.data)
    no= data.get('no')
    print('no : '+ no)
    dac.Dac().addRecommend(no)
    return jsonify([])

@app.route('/commenting', methods=["GET", "POST"])
def commenting() :

    text = request.form['text']
    borderNo = request.form['boardNo']
    nickName= 'taehee'

    dac.Dac().addComment(text=text , no=borderNo, nickName=nickName)

    return redirect(url_for('boardDetail', no=borderNo))

@app.route('/posting', methods=["GET", "POST"])
def posting() :
    if request.method =='GET' :
        return render_template('jonghap/posting.html')
    title = request.form['title']
    text = request.form['text']
    lang = request.form['lang']

    dac.Dac().insertBoard(title, text, lang)

    return redirect(url_for('board'))


@app.route('/board', methods=['GET'])
def board() :
    page = request.args.get('page')
    viewCnt = request.args.get('viewCnt')
    recommendCnt = request.args.get('recommendCnt')
    searchCate = request.args.get('searchCate')
    searchText = request.args.get('searchText')

    if page ==None :
        page =1 
        viewCnt =0
        recommendCnt =0
        searchCate=''
        searchText =''

    boardDac = dac.Dac()
    boardList = boardDac.seledtBoardList(page,viewCnt,recommendCnt, searchCate,searchText)

    return render_template('jonghap/board.html' , boardList=boardList, session= session)


@app.route('/boardDetail')
def boardDetail() :
    no = request.args.get('no')
    service = bs.BoardService()
    result = service.getBoardDetail(no)
    post = result[0]
    commentList = result[1]
    return render_template('jonghap/boardDetail.html', post = post, commentList=commentList)

@app.route('/registerPage', methods=["GET", "POST"])
def registerPage():
    return render_template('jonghap/register.html' )

@app.route('/register', methods=["GET", "POST"])
def register():
    
    name = request.form['name']
    nickName = request.form['nickName']
    id = request.form['id']
    password = request.form['password']
    email = request.form['email']
    lang = request.form['lang']
    
    registerDac = dac.Dac()
    registerDac.register(name,nickName, id, password, email, lang)
    
    return redirect(url_for('board'))

@app.route('/doPracTran', methods = ['POST'])
def doPracTran() : 
    data = json.loads(request.data)
    text = data.get('text')
    pracText = data.get('pracText')
    sourceLang = data.get('sourceLang')
    targetLang = data.get('targetLang')

    
    api = data.get('api')

    tranService = TranSer.TransService(sourceLang=sourceLang 
                                       , targetLang=targetLang
                                       , text = text
                                       )
    
    print(tranService.getSimilarPoint(api,pracText))

    return jsonify(tranService.getSimilarPoint(api,pracText))


@app.route('/translate', methods = ['POST'])
def translate() : 
    data = json.loads(request.data)
    text = data.get('context')
    sourceLang = data.get('sourceLang')
    targetLang = data.get('targetLang')
    interLang = data.get('interLang')
    interApi  = data.get('interApi')

    tranService = TranSer.TransService(sourceLang=sourceLang 
                                       , targetLang=targetLang
                                       , text = text
                                       , interLang = interLang
                                       , interApi= interApi
                                       )
    
    
    if 'id' in session :
        dac.Dac().insertTranslateLog(session['memNo'],text, targetLang , sourceLang)

    return jsonify(tranService.getTranslateList())


@app.route('/translatePage', methods = ['POST','GET'])
def translatePage() : 
    text = request.args.get('text')
    targetLang = request.args.get('targetLang')
    sourceLang = request.args.get('sourceLang')
    
    if text == None :
        text = ''
        targetLang ='' 
        sourceLang = ''  
    return render_template('jonghap/translate.html', text=text, targetLang=targetLang, sourceLang=sourceLang)

@app.route('/practiceTranPage', methods = ['POST','GET']) 
def practiceTranPage() :
    return render_template('jonghap/practiceTran.html')
@app.route('/enquiryPage', methods = ['POST','GET']) 
def enquiryPage() :
    return render_template('jonghap/enquiry.html')


@app.route('/detectLang', methods = ['POST'])
def detectLang() : 
    data = json.loads(request.data)
    text = data.get('context')   
    tranService = TranSer.TransService('' , '',text)
    return jsonify(tranService.getDetectLang())

@app.route('/createSentence', methods = ['POST'])
def createSentence() :
    data = json.loads(request.data)

    sentence = 'This is text Sentence' 

    sourceLang = data.get('sourceLang')
    targetLang = data.get('targetLang')
    interLang = ''
    interApi  = ''
    tranService = TranSer.TransService(sourceLang=sourceLang 
                                       , targetLang=targetLang
                                       , text = sentence
                                       , interLang = interLang
                                       , interApi= interApi
                                       )
    
    return jsonify(tranService.getTranslateList())


#dict

@app.route('/dict', methods = ['POST','GET'])
def doDict() : 
    
    data = json.loads(request.data)
    targetLang = data.get('targetLang')
    text = data.get('text')

    if 'id' in session :
        dac.Dac().insertSearchLog(session['memNo'],text, targetLang )
    
    return jsonify(cw.dictCrawler(targetLang,text).dictService())



if __name__ == '__main__':
    app.run(debug=True)