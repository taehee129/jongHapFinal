import pymssql
from Model.boardObject import Post
from Model.DbConnect import DbConnection
from Model.commentObject import Comment
from Model.memberObject import Member
from Model.searchLogObject import SearchLogObject
from Model.wordCoachObject import wordCaochObject
from Model.enquiryObject import EnquiryObject
from Model.translateLogObject import TranLogObject

class Dac() :
    def __init__(self) -> None:
        self.conn = DbConnection().connect()

    def register(self, name, nick_name, id, password, email, lang) :
        print(name, nick_name, id, password, email, lang)

        query = 'insert into member(name, nick_name, id, password, email, lang, insert_date) values(\''+name+'\', \''+ nick_name+'\', \''+ id+'\', \''+password+'\', \''+email+'\', \''+lang+'\', getdate())'
        # Connection 으로부터 Cursor 생성
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close()      

    def seledtBoardList(self, page, viewCnt , recommendCnt, searchCate='' , searchText='') :
        boardList = []
        searchQuery = ''
        if searchCate =='제목' :
            searchQuery= "AND TITLE LIKE '%"+ str(searchText)+"%'"
        elif searchCate =='내용' : 
            searchQuery= "AND TEXT LIKE '%"+ searchText+"%'"
        else :
            searchQuery =''


        query= '''       
            SELECT * 
              FROM
            (
            SELECT ROW_NUMBER () OVER (ORDER BY INSERT_DATE DESC) AS IDX
                , BOARD_NO 
                , TITLE
                , NICK_NAME
                , TEXT
                , VIEW_CNT
                , RECOMMEND_CNT
                , LANG
                , FORMAT(INSERT_DATE,  'yyyy-MM-dd') AS A
                FROM BOARD
             WHERE VIEW_CNT >= '''+ str(viewCnt)+'''
               AND RECOMMEND_CNT >= '''+ str(recommendCnt)+'''
            ''' + searchQuery+ '''
            ) A 
            WHERE A.IDX>='''+ str(((int(page)-1)*10 + 1))+''' AND A.IDX<='''+ str((int(page)*10))+'''
        '''
        print(query)
        cursor = self.conn.cursor()
        query.encode('utf-8')
        cursor.execute(query)

        row = cursor.fetchone()

        while row :
            # 0 : booard_no , 1 : name m, 2 : text, 3 : view_cnt, 4 : recommend_cnt , 5 : lang, 6 :isert_date  
            post = Post(row[1], row[2] , row[3], row[4] ,row[5], row[6] , row[7],row[8])           
            boardList.append(post)
            row = cursor.fetchone()            
        self.conn.close()

        
        return boardList
    def selectCommentList(self, no) :      
        commentList = [] 
        query = 'select * from board_comment where board_no = ' +no+' order by comment_no desc'
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()

        while row :
    
            comment = Comment(row[0], row[1] , row[2], row[3],row[4])
            commentList.append(comment)
            row = cursor.fetchone() 
         
        self.conn.close()

        return commentList
    
    def selectBoardDetail(self, no) :
        query = 'select * from board where board_no ='+ no
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()

        post = Post(row[0], row[1], row[2], row[3] ,row[4], row[5] , row[6], row[7])
        return post 
    def insertBoard(self,  title, text,lang ) :
        
        query = u"insert into board(title, nick_name,text ,view_cnt, recommend_cnt, lang, insert_date) values('"+title+"','taehee', '"+text+"' , 0 , 0 , '"+lang+"' , getdate())"
         # Connection 으로부터 Cursor 생성
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close()       
    
    def plusViewCnt(self, no) :
        query = 'update board set view_cnt = view_cnt +1 where board_no = '+no
        # Connection 으로부터 Cursor 생성
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close()  
    
    def addComment(self, text,nickName ,no) :
        query = "insert into board_comment(board_no ,nick_name, text, insert_date) values("+no+",'"+ nickName+"', '"+ text+"' , GETDATE())"
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close() 
    def addRecommend(self, boardNo) : 
        query = 'update board set recommend_cnt = recommend_cnt +1 where board_no='+boardNo
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close() 
    
    def login(self, id, password) :
        query = "select * from member where id = '"+ id + "'and password ='" + password+"'"
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()
        member =False

        if row : 
            member = Member(row[0], row[1], row[2], row[3], row[4], row[5] , row[6], row[7])



        return member

    def insertSearchLog(self,memNo, text, targetLang)  :
        query = "insert into search_log(memno, text,target_lang,insert_date) values("+str(memNo)+", '"+ text+"' ,'"+ targetLang+"', GETDATE())"
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close() 
    
    def selectSearchLog(self, memNo) :
        
        query = 'select text , target_lang from search_log where memno ='+ str(memNo) +' group by text, target_lang'
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()
        resultList= []

        while row :
    
            searchLog = SearchLogObject('', '' , row[0], row[1],'')
            resultList.append(searchLog)
            row = cursor.fetchone() 
        
        return resultList

    def insertTranslateLog(self,memNo, text, targetLang, sourceLang)  :
        query = "insert into translate_log(memno, text,target_lang,source_lang,insert_date) values("+str(memNo)+", '"+ text+"' ,'"+ targetLang+"', '"+sourceLang+"',GETDATE())"
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close() 
    def selectTranLog(self, memNo) :
        
        query = 'select text , target_lang, source_lang from translate_log where memno ='+ str(memNo) +' group by text, target_lang, source_lang'
        cursor = self.conn.cursor()
        cursor.execute(query)
        
        row = cursor.fetchone()
        resultList= []

        while row :
    
            searchLog = TranLogObject('', '' , row[0], row[1],row[2] ,'')
            resultList.append(searchLog)
            row = cursor.fetchone() 
        
        return resultList
    def selectWordCoach(self, quizNo, memNo) : 
        if quizNo == 0 :
            query = '''
            
            select top 1 a.quiz_no, question, option1,option2 , answer, explain, newid()
            from word_coach a
            left join word_coach_log b 
                on  a.quiz_no = b.quiz_no 
                and  b.memno ='''+str(memNo)+''' 
            where b.log_no is null
            order by newid()

            '''
        else :
            query ='select * from word_coach where quiz_no='+str(quizNo)
        
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()
        resultList= []

        while row :
    
            quiz = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            resultList.append(quiz)
            row = cursor.fetchone() 
        
        return resultList
    
    def selectWordTest(self, testId, memNo) : 

        if testId == 0 :

            query = '''
            select top 1 
                  a.test_no, question,a.option1, a.option2, a.option3, a.option4, answer, img_path,
                newid() 
                from word_test  a
            left join word_test_log b 
                on a.test_no = b.test_no 
            and b.memno = '''+ str(memNo)+'''
            where b.log_no is null 
            order by newid()        

            '''
            print(query)
        else : 
            query = 'select test_no, question , option1, option2, option3, option4, answer, img_path from word_test where test_no =' + str(testId)
    
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()
        resultList= []

        while row :
    
            test = (row[0], row[1], row[2], row[3], row[4], row[5], row[6],row[7])
            resultList.append(test)
            row = cursor.fetchone() 
        
        return resultList

    def insertTestLog(self, testNo, MemNo, isTrue) :
        query = "delete from word_test_log where test_no="+ str(testNo)+" and memno="+ str(MemNo)+"  insert into word_test_log(test_no, memno, is_true) values("+ str(testNo)+", "+ str(MemNo)+",'"+ str(isTrue)+"' )"
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close() 

    def insertQuizLog(self, quizNo, MemNo, isTrue) :
        query = "delete from word_coach_log where quiz_no="+ str(quizNo)+" and memno="+ str(MemNo)+"  insert into word_coach_log(quiz_no, memno, is_true) values("+ str(quizNo)+", "+ str(MemNo)+",'"+ str(isTrue)+"' )"
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close() 
    
    def seleteTestLog(self, memNo) : 
        query = '''
        select b.answer , b.test_no
          from word_test_log  a
         inner join word_test b 
            on a.test_no = b.test_no
         where a.memno='''+ str(memNo)+'''
         and is_true='f'
        '''
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()
        resultList= []

        while row :
    
            resultList.append([row[0], row[1]])
            row = cursor.fetchone() 
        
        return resultList        
    

    def selectCoachLog(self, memNo) : 
        query = '''
        select b.answer , b.quiz_no
          from word_coach_log  a
         inner join word_coach b 
            on a.quiz_no = b.quiz_no
         where a.memno='''+ str(memNo)+'''
         and is_true='f'
        '''
        print(query)
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()
        resultList= []
       
        while row :
    
            resultList.append([row[0], row[1]])
            row = cursor.fetchone() 
        
        return resultList   


    def insertEnquiry(self,memNo, cate, text) : 

        query = "insert into enquiry(memno,cate, text,insert_date) values("+str(memNo)+", '"+ cate+"' ,'"+ text+"', GETDATE())"
        cursor = self.conn.cursor()
        
        # SQL문 실행
        cursor.execute(query)

        self.conn.commit()

        # 연결 끊기
        self.conn.close()         
    def selectEnquiry(self, memNo) : 
        query = '''
            select * from enquiry where memNo = '''+ str(memNo)+'''
        '''
        cursor = self.conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()
        resultList= []
        code = {'e' : '에러' , 'g' : '개선사항', "s" : '사용법', 't': '기타'}
        while row :
            enquiry = EnquiryObject(row[0],row[1],row[2],row[3], row[4],row[5])
            enquiry.cate = code[enquiry.cate]
            resultList.append(enquiry)
            row = cursor.fetchone() 
        
        return resultList          
