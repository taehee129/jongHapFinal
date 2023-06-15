import Model.Dac as data

class BoardService :
    def __init__(self) -> None:
        pass

    def getBoardDetail(self, no) :
        dac = data.Dac() 
        dac.plusViewCnt(no) # 조회수 증가 
        dac = data.Dac() 
        return [dac.selectBoardDetail(no), dac.selectCommentList(no)]
        