# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import tkinter as tk
import tkinter.messagebox as msg
import pandas as pd

class App(tk.Frame):
    def __init__(self,master=None):
        super(App, self).__init__()
        self.master.title("Move King")
        tk.Frame.__init__(self,master)
        master.protocol('WM_DELETE_WINDOW',quit)
        self.master.resizable(width=False,height=False)
        self.initContents()
        self.updateBoard()

    def initContents(self):
        self.kingData = pd.read_csv("kingMoves.csv")
        self.moves = []
        self.xMax = 7
        self.yMax = 7

        self.pack(fill="both",expand=True)

        self.canvas=tk.Canvas(self,bg="dark gray")
        self.canvas.pack(side="top")
        self.canvas.update()
        for a in range(self.xMax+1):
            for b in range(self.yMax+1):
                self.canvas.create_rectangle(
                    a/(self.xMax+1)*self.canvas.winfo_width(),
                    b/(self.yMax+1)*self.canvas.winfo_height(),
                    (a+1)/(self.xMax+1)*self.canvas.winfo_width()-1,
                    (b+1)/(self.yMax+1)*self.canvas.winfo_height()-1,
                    fill="light gray" if a%2==b%2 else "dark gray"
                )

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.pack(side="right")
        self.upperButtonFrame=tk.Frame(self.buttonFrame)
        self.upperButtonFrame.pack(side="top")
        self.buttonLabel=tk.Label(self.upperButtonFrame,text="Move:")
        self.buttonLabel.pack(side="left")
        self.rightButton = tk.Button(self.upperButtonFrame, text="Right", command=lambda: self.setDir("Right"))
        self.rightButton.pack(side="right")
        self.lowerButtonFrame = tk.Frame(self.buttonFrame)
        self.lowerButtonFrame.pack(side="bottom")
        self.DownButton = tk.Button(self.lowerButtonFrame, text="Down", command=lambda: self.setDir("Down"))
        self.DownButton.pack(side="left")
        self.DiagButton = tk.Button(self.lowerButtonFrame, text="Diagonal", command=lambda: self.setDir("Diagonal"))
        self.DiagButton.pack(side="right")

        self.playAsMenuVal=tk.StringVar(root)
        self.playAsMenuVal.set("Player 1")
        self.playerOpts=["Player 1", "Player 2"]

        self.resetFrame=tk.Frame(self)
        self.resetFrame.pack(side="left")
        self.optionFrame=tk.Frame(self.resetFrame)
        self.optionFrame.pack(side="top")
        self.playerOptionText=tk.Label(self.optionFrame,text="Play as:")
        self.playerOptionText.pack(side="left")
        self.playerOption = tk.OptionMenu(self.optionFrame, self.playAsMenuVal, *self.playerOpts)
        self.playerOption.pack(side="right")
        self.resetButton=tk.Button(self.resetFrame, text="Reset",command=self.reset)
        self.resetButton.pack(side="bottom")

        self.reset()

    def updateBoard(self):
        if self.playerOpts[self.playerTurn]==self.playAs:
            if self.dir!="":
                if self.move(self.dir):
                    if self.x == 7 and self.y == 7:
                        msg.showinfo("Game over", "You lost.")
                        self.reset()
                    else:
                        self.playerTurn = (self.playerTurn + 1) % 2
                self.dir=""
        else:
            try:
                self.dir = self.pickMove(self.moves, self.playerOpts[self.playerTurn])
            except: #No winning strategy
                if self.x<7 and self.y<7:
                    self.dir="Diagonal"
                elif self.x<7:
                    self.dir="Right"
                elif self.y<7:
                    self.dir="Down"
                else:
                    pass
            self.move(self.dir)
            if self.x == 7 and self.y == 7:
                msg.showinfo("Game over", "You won.")
                self.reset()
            else:
                self.playerTurn = (self.playerTurn + 1) % 2
            self.dir = ""
        self.after(250,self.updateBoard)

    def updateXY(self,x,y):
        return (
            ((x / (self.xMax + 1) * self.canvas.winfo_width()) +
             ((x + 1) / (self.xMax + 1) * self.canvas.winfo_width() - 1)) / 2,
            ((y / (self.yMax + 1) * self.canvas.winfo_height()) +
             ((y + 1) / (self.yMax + 1) * self.canvas.winfo_height() - 1)) / 2
        )

    def setDir(self, dir):
        self.dir=dir

    def pickMove(self, moves,winner="Player 2"):  #computer chooses move
        filteredData=self.kingData.copy()
        filteredData=filteredData[filteredData["Winner"]==winner]
        for a in range(len(moves)):
            filteredData=filteredData[filteredData[filteredData.columns.values[a]]==moves[a]]
        dataFreq=filteredData.groupby(filteredData.columns.values[len(moves)]).count()["Winner"]
        decision=dataFreq[dataFreq==max(dataFreq)].index[0]
        return decision

    def move(self,dir):
        self.moves.append(dir)
        if dir=="Right":
            if self.x<7:
                self.x+=1
                self.canvas.move(self.piece, self.updateXY(1,0)[0]*2/3, 0)
                return True
            else:
                print("Cannot move right.")
                return False
        elif dir=="Down":
            if self.y<7:
                self.y+=1
                self.canvas.move(self.piece, 0, self.updateXY(0,1)[1]*2/3)
                return True
            else:
                print("Cannot move down.")
                return False
        elif dir=="Diagonal":
            if self.x<7 and self.y<7:
                self.x+=1
                self.y+=1
                self.canvas.move(self.piece, self.updateXY(1,1)[0]*2/3, self.updateXY(1,1)[1]*2/3)
                return True
            else:
                print("Cannot move diagonally.")
                return False
        else:
            return False

    def reset(self):
        self.moves.clear()
        self.playAs=self.playAsMenuVal.get()
        self.playerTurn=0
        self.dir=""

        self.x = 0
        self.y = 0

        self.xCoord, self.yCoord = self.updateXY(self.x, self.y)

        try:
            self.canvas.delete(self.piece)
        except:
            pass

        self.piece = self.canvas.create_oval(
            self.xCoord - 10,
            self.yCoord - 10,
            self.xCoord + 10,
            self.yCoord + 10,
            fill="black"
        )

if __name__=="__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
    app.destroy()
