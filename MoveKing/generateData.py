"""import pandas as pd"""

def rMoves(x=0, y=0, path=[], xMax=7, yMax=7):  #csv string
    retString=""
    if x==xMax and y==yMax:
        retString = str(path).replace("[", "").replace("]", "").replace(" ", "").replace("\'", "\"")
        for a in range(14-len(path)):
            retString+=",\"NA\""
        retString += ",\"" + str(len(path))+"\","+("\"Player 1\"" if len(path)%2==0 else "\"Player 2\"")
        return retString+"\n"
    if x<xMax: #move right
        tempPath = path.copy()
        tempPath.append("Right")
        retString+=rMoves(x+1,y,tempPath)
    if y<yMax: #move down
        tempPath=path.copy()
        tempPath.append("Down")
        retString+=rMoves(x,y+1,tempPath)
    if x<xMax and y<yMax: #move diagonal
        tempPath=path.copy()
        tempPath.append("Diagonal")
        retString+=rMoves(x+1,y+1,tempPath)
    return retString

"""def pMoves(x=0, y=0, path=[], xMax=7, yMax=7):  #pandas dataframe
    retData=pd.DataFrame()
    if x==xMax and y==yMax:
        retData.append(pd.DataFrame([path]))
        #print(pd.DataFrame([path]))
        return retData
    if x<xMax: #move right
        tempPath = path.copy()
        tempPath.append("Right")
        retData.append(pMoves(x+1,y,tempPath))
    if y<yMax: #move down
        tempPath=path.copy()
        tempPath.append("Down")
        retData.append(pMoves(x,y+1,tempPath))
    if x<xMax and y<yMax: #move diagonal
        tempPath=path.copy()
        tempPath.append("Diagonal")
        retData.append(pMoves(x+1,y+1,tempPath))
    return retData
"""

with open("kingMoves.csv","w+") as f:
    moves=rMoves()
    print(moves)
    f.write("\"P1M1\",\"P2M1\",\"P1M2\",\"P2M2\",\"P1M3\",\"P2M3\",\"P1M4\","
            "\"P2M4\",\"P1M5\",\"P2M5\",\"P1M6\",\"P2M6\",\"P1M7\",\"P2M7\","
            "\"Moves\",\"Winner\""
            "\n")
    f.write(moves)