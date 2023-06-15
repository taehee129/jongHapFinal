import Model.Translate as tranApi
import Model.CalSim as Cal

class TransService() :
    def __init__(self , sourceLang, targetLang, text, interLang='', interApi='')  :
        self.sourceLang = sourceLang
        self.targetLang = targetLang
        self.text = text
        self.interLang = interLang
        self.interApi = interApi

    def getTranslateList(self) : 

        if (self.interApi != '') :
            interApi = tranApi.TranslateByApi(self.interApi, self.sourceLang, self.interLang, self.text)
            interResult = interApi.translate() 
            if interResult != '' :  self.text = interResult
        else :  
            self.interLang = self.sourceLang

       # print('-------------------------------------')
        #print(self.interLang, self.text, self.targetLang)
        print( self.interLang, self.targetLang)
        googleApi = tranApi.TranslateByApi('google', self.interLang, self.targetLang, self.text )
        papagoApi = tranApi.TranslateByApi('papago', self.interLang, self.targetLang, self.text )
        kakaoApi = tranApi.TranslateByApi('kakao', self.interLang, self.targetLang, self.text )
        deeplApi = tranApi.TranslateByApi('deepl', self.interLang, self.targetLang, self.text )
        gptApi = tranApi.TranslateByApi('gpt', self.interLang, self.targetLang, self.text )


        result = [googleApi.translate(), papagoApi.translate(), kakaoApi.translate(), deeplApi.translate(), gptApi.translate()]
        
        return result
    
    def getTran(self, api) : 
        if (self.interApi != '') :
            interApi = tranApi.TranslateByApi(self.interApi, self.sourceLang, self.interLang, self.text)
            interResult = interApi.translate() 
            if interResult != '' :  self.text = interResult
        else :  
            self.interLang = self.sourceLang

        return tranApi.TranslateByApi(api, self.interLang, self.targetLang, self.text ).translate()       

    def getSimilarPoint(self, api, userText) : 

        apiResult = self.getTran(api)
        result = [apiResult , int(round( Cal.CalSim().sentenceSimilarity(userText, apiResult) , 2)*100)]
        return result



    def getDetectLang(self) : 
        return tranApi.TranslateByApi('google', self.sourceLang, self.targetLang, self.text ).detectLang()


