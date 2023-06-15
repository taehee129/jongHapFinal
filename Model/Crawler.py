import requests
from bs4 import BeautifulSoup
class dictCrawler :
    def __init__(self, lang, text) :
        self.lang =lang 
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        self.text = text
    def swahili(self) :
        resultList =[]
        url = "https://glosbe.com/en/sw/"+ self.text
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        response.raise_for_status()
        words = soup.select('.pl-1 .pr-1 h3')
        result = ''   
        name = 'glosbe'
        for i ,word in enumerate(words)  : 
            result += '<p class="fs-30 mb-2"> '+ str(i+1)+'. '+ word.text+'</p>'
        resultList.append([url, result, name])

        url = 'https://en.bab.la/dictionary/english-swahili/'+ self.text
        response = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        selectList = soup.select('.quick-results')[0]
        selectList = selectList.select('.quick-result-entry')

        result =''
        name='bab.la'
        for i,val in enumerate(selectList) : 

            strResult = ''  

            if val.select('.babQuickResult') :
                strResult += val.select('.babQuickResult')[0].text + ' - '
            for word in val.select('.quick-result-overview li a') :
                strResult += word.text  +' , '
            
            strResult= strResult[0 :len(strResult)-3]
            result += '<p class="fs-30 mb-2"> '+ str(i+1)+'. '+ strResult+'</p>'

        resultList.append([url, result, name]) 

        url ='https://small.dic.daum.net/search.do?q=안녕&dic=sw'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        result = ''
        name = 'daum'
        selectList = soup.select('.card_word[data-target="mean"] .txt_searchword')  
        selectList2 = soup.select('.card_word[data-target="mean"] .txt_search')
        for i in range(len(selectList)) : 
            result +='<p class="fs-30 mb-2"> '+ str(i+1)+'. '+ selectList[i].text+'</p>'
            result +='<p class="fs-30 mb-2">  '+ selectList2[i].text+'</p>'

        resultList.append([url,result, name])
        return resultList
    

    def dictService(self) : 
        if self.lang =='sw' : 
            return self.swahili()
    

    