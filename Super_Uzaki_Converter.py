import shogi.Ayane as ayane
import time
from concurrent import futures
import os
import math


class Gen_teacher:
    def __init__(self,address,SendComTuple,exeFile,go_depth):

        self.usi=ayane.UsiEngine()

        self.address=address

        self.exeFile=exeFile

        self.settings_of_engine=SendComTuple

        self.go_depth=go_depth
        
        self.read_print=(address,"を開きます")

        self.position=[]

        self.score=0

        self.ThinkResult=""

        self.send_sfen="startpos moves"

        #独自設定用

    
    def read(self):
        print("".join(self.read_print))
        with open(self.address,mode="r") as pos:
            self.read_sfen=tuple([i for i in pos])
            #1行ごとに読み取り
    
    def None_Lambda(self):
        #引き分けの棋譜とかはこれで。
        #例えば、序盤16手目までを集中的に学習させたいけど、棋譜が短すぎなときなんかに使うとよい
        self.result="0"
        fname="".join([self.address[:-5],"_teacher.txt"])
        with open(fname,mode="w") as f:pass
        #ファイル生成

        self.usi.debug_print=False

        self.usi.connect(self.exeFile)
        #YaneuraOuの接続
        send="".join(self.settings_of_engine)
        self.usi.send_command(send)
        time.sleep(1)
        self.usi.send_command("isready\n")
        time.sleep(1)
        self.usi.send_command("usinewgame\n")
        #YaneuraOuの設定

        print("generating start")
        length=len(self.read_sfen)

        Finish=0

        for i in self.read_sfen:
            

            self.position = i.split()

            self.position_length=len(self.position)-1
            
            self.sente_unique=""

            self.gote_unique=""
            
            self.send_sfen="startpos moves"
            
            self.tesuu=0
        
            self.teban="b"

            self.output=""

            self.output_sfen=""
            
            self.tegoma_sfen="-"

            self.tegoma_dict={"R":0,"B":0,"G":0,"S":0,"N":0,"L":0,"P":0,
                          "r":0,"b":0,"g":0,"s":0,"n":0,"l":0,"p":0}
            
            self.board=[
            #将棋のsfenの数字が逆転するので、処理を変える必要がある
            # 0   1   2   3   4   5   6   7   8  ...配列
            # 9   8   7   6   5   4   3   2   1  ...将棋
            ["l","n","s","g","k","g","s","n","l"],#0
            ["o","r","o","o","o","o","o","b","o"],#1
            ["p","p","p","p","p","p","p","p","p"],#2
            ["o","o","o","o","o","o","o","o","o"],#3
            ["o","o","o","o","o","o","o","o","o"],#4
            ["o","o","o","o","o","o","o","o","o"],#5
            ["P","P","P","P","P","P","P","P","P"],#6
            ["o","B","o","o","o","o","o","R","o"],#7
            ["L","N","S","G","K","G","S","N","L"]]#8

            for j in self.position:

                if "startpos" not in j and "moves" not in j:
                    #局面をsfenに変換
                    self.changing_sfen()
                    #self.output_sfenに現在のboardのsfenを格納

                    self.renew(j,self.teban) #renew(self,str,str)
                    #局面を更新
                    #評価値の関係上この順番
                    
                    self.get_score()
                    #次の一手を打った局面の相手の最善手の評価値を反転させたものを出す。
                    #処理して評価値をself.scoreに代入
                    
                    self.output="".join([
                        "sfen ",self.output_sfen,
                        " ",self.teban,
                        " ",self.tegoma_sfen,
                        " 0\nmove ",j,
                        "\nscore ",str(self.score),
                        "\nply ",str(self.tesuu),
                        "\nresult ",self.result,
                        "\ne\n"
                    ])
                    #sfen変換終了
                    #print(".",end="",flush=True)
                    #点を打つ
                    
                    with open(fname,mode="a") as f:
                        f.write(self.output)
                    
                    
                    self.tesuu+=1

                    if self.teban=="b":
                        self.teban="w"
                    else:
                        self.teban="b"
            Finish+=1
            print("".join([str(Finish)," / ",str(length)," Finish"]))
        print("all done")


    def PonaMethod(self):#マルチスレッドでないタイプ
        fname="".join([self.address[:-5],"_teacher.txt"])
        with open(fname,mode="w") as f:pass
        #ファイル生成

        self.usi.debug_print=False

        self.usi.connect(self.exeFile)
        #YaneuraOuの接続
        send="".join(self.settings_of_engine)
        self.usi.send_command(send)
        time.sleep(2)
        self.usi.send_command("isready\n")
        time.sleep(2)
        self.usi.send_command("usinewgame\n")
        #YaneuraOuの設定

        print("generating start")

        
        length=len(self.read_sfen)

        Finish=0

        for i in self.read_sfen:
            self.result="1"

            self.position = i.split()

            if len(self.position)%2==0:#偶数なら後手勝利
                self.result="-1"
            else:#奇数なら先手勝利
                self.result="1"
                
            self.sente_unique=""

            self.gote_unique=""
            
            self.send_sfen="startpos moves"
            
            self.tesuu=0
        
            self.teban="b"

            self.output=""

            self.output_sfen=""
            
            self.tegoma_sfen="-"

            self.tegoma_dict={"R":0,"B":0,"G":0,"S":0,"N":0,"L":0,"P":0,
                          "r":0,"b":0,"g":0,"s":0,"n":0,"l":0,"p":0}
            
            self.board=[
            #将棋のsfenの数字が逆転するので、処理を変える必要がある
            # 0   1   2   3   4   5   6   7   8  ...配列
            # 9   8   7   6   5   4   3   2   1  ...将棋
            ["l","n","s","g","k","g","s","n","l"],#0
            ["o","r","o","o","o","o","o","b","o"],#1
            ["p","p","p","p","p","p","p","p","p"],#2
            ["o","o","o","o","o","o","o","o","o"],#3
            ["o","o","o","o","o","o","o","o","o"],#4
            ["o","o","o","o","o","o","o","o","o"],#5
            ["P","P","P","P","P","P","P","P","P"],#6
            ["o","B","o","o","o","o","o","R","o"],#7
            ["L","N","S","G","K","G","S","N","L"]]#8

            for j in self.position:
                if "startpos" not in j and "moves" not in j:
                    #局面をsfenに変換
                    self.changing_sfen()
                    #self.output_sfenに現在のboardのsfenを格納

                    self.renew(j,self.teban) #renew(self,str,str)
                    #局面を更新
                    #評価値の関係上この順番
                    
                    self.get_score()
                    #次の一手を打った局面の相手の最善手の評価値を反転させたものを出す。
                    #処理して評価値をself.scoreに代入
                    
                    self.output="".join([
                        "sfen ",self.output_sfen,
                        " ",self.teban,
                        " ",self.tegoma_sfen,
                        " 0\nmove ",j,
                        "\nscore ",str(self.score),
                        "\nply ",str(self.tesuu),
                        "\nresult ",self.result,
                        "\ne\n"
                    ])
                    #sfen変換終了
                    
                    with open(fname,mode="a") as f:
                        f.write(self.output)
                    
                    
                    self.tesuu+=1
                    if self.result=="1":
                        self.result="-1"
                    
                    else:
                        self.result="1"
                    if self.teban=="b":
                        self.teban="w"
                    else:
                        self.teban="b"
            Finish+=1
            print("".join([str(Finish)," / ",str(length)," Finish"]))
        print("all done")


    def renew(self,next,color):
        self.send_sfen="".join(tuple([self.send_sfen," ",next]))
        #エンジンに送る用
        #連続したものなので初期化不要
        #board[y][x]となる点に注意
        
        self.x1=next[:1].translate(str.maketrans({"9":"0","8":"1","7":"2","6":"3","5":"4","4":"5","3":"6","2":"7","1":"8"}))
        self.y1=next[1:2].translate(str.maketrans({"a":"0","b":"1","c":"2","d":"3","e":"4","f":"5","g":"6","h":"7","i":"8"}))
        #1文字目と2文字目

        self.x2=next[2:3].translate(str.maketrans({"9":"0","8":"1","7":"2","6":"3","5":"4","4":"5","3":"6","2":"7","1":"8"}))
        self.y2=next[3:4].translate(str.maketrans({"a":"0","b":"1","c":"2","d":"3","e":"4","f":"5","g":"6","h":"7","i":"8"}))
        #3文字目と4文字目
        
        if "*" in next:
            #1文字目に打った手駒
            self.renew_koma=self.tegoma(self.x1,1,color)
            self.board[int(self.y2)][int(self.x2)]=self.renew_koma
        else:
            self.x1=int(self.x1)
            self.x2=int(self.x2)
            self.y1=int(self.y1)
            self.y2=int(self.y2)

            if "o" not in self.board[self.y2][self.x2]:
                self.tegoma(self.board[self.y2][self.x2],0,color)
                self.board[self.y2][self.x2]=self.board[self.y1][self.x1]
                self.board[self.y1][self.x1]="o"

            else:
                self.board[self.y2][self.x2]=self.board[self.y1][self.x1]
                self.board[self.y1][self.x1]="o"


            if "+" in next:#成り
                self.board[self.y2][self.x2]="".join(["+",self.board[self.y2][self.x2]])


    def tegoma(self,koma,option,color):
        self.tegoma_sfen="" #"-"が入ってるのであらかじめ初期化
        if "+" in koma:
            koma=koma[1:]
        #colorはtebanのこと
        #komaには、self.board[y][x]で取得したものが代入される
        #option=0...komaの手駒取得(color不使用)
        #option=1...komaの手駒使用(colorでどちらの手駒を使ったか区別)
        #           blackなら大文字、whiteなら小文字を減らす
        if option==0:
            self.true_koma=koma.swapcase()
            self.tegoma_dict[self.true_koma]+=1
        elif option==1:
            if color == "b":
                self.true_koma=koma
            else:
                self.true_koma=koma.lower()

            self.tegoma_dict[self.true_koma]-=1
        for z in self.tegoma_dict.keys():
            if self.tegoma_dict[z]>0:
                if self.tegoma_dict[z]>1:
                    self.tegoma_sfen="".join([self.tegoma_sfen,str(self.tegoma_dict[z]),z])
                else:
                    self.tegoma_sfen="".join(tuple([self.tegoma_sfen,z]))
        return self.true_koma


    def get_score(self):
        self.usi.usi_position(self.send_sfen)
        # 先にrenewを実行することで、次の一手を打った後に
        # 相手が指す最善手の評価値を反転させて、高めの精度の評価値反映が可能
        self.usi.usi_go_and_wait_bestmove("".join(["depth ",self.go_depth,"\n"]))
        #ここでAyaneはUsiThinkResultクラスをthink_resultに代入。
        self.ThinkResult=self.usi.think_result.to_string().split()
        self.cp_admission=0
        self.mate_admission=0
        self.bestmove=0
        for k in self.ThinkResult:
            if self.cp_admission==0 and "cp" in k:
                self.cp_admission=1
            elif self.mate_admission==0 and "mate" in k:
                self.mate_admission=1
            elif self.cp_admission==1:
                self.score=int(k)
                self.cp_admission=2
            elif self.mate_admission==1:
                if k=="-0" or "0":
                    self.score=-100000
                    self.mate_admission=2
                # 詰みは0で投了のため、0なら問答無用で-100000
                # 後でしっかり100000に変換されるため、指し手は正しく評価される
                if int(k) < 0:
                    self.score=-100000-int(k)
                    self.mate_admission=2
                elif int(k) > 0:
                    self.score=100000-int(k)
                    self.mate_admission=2
        
        # 評価値をここで反転させる
        self.score= -1*self.score
            
        """
        独自設定
        """
        if int(self.tesuu) <10 and self.board[7][2]=="R" and self.teban=="b":
            self.sente_unique="True"
            self.score += 10
        if self.sente_unique=="True" and self.teban=="b":
            if int(self.tesuu) <17 and self.board[7][3]=="S":
                self.score+=3
            if int(self.tesuu) <25 and self.board[7][6]=="S" and self.board[7][4]=="G" and self.board[8][5]=="G" and self.board[7][7]=="K":
                self.score+=3 #美濃
            if int(self.tesuu) <32 and self.board[6][5]=="G" and self.board[7][6]=="S" and self.board[8][5]=="G" and self.board[7][7]=="K":
                self.score+=5 #高美濃
            if int(self.tesuu) <35 and self.board[8][8]=="K" and self.board[7][7]=="S" and self.board[7][8]=="L" and self.board[8][7]=="N" and self.board[6][8]=="G":
                self.score+=3 #振り穴
            if int(self.tesuu) <41 and self.board[7][7]=="K" and self.board[6][7]=="S" and self.board[7][6]=="G":
                self.score+=7 #銀冠
        
        if int(self.tesuu) <10 and self.board[1][6]=="r" and self.teban=="w":
            self.gote_unique="True"
            self.score += 10
        if self.gote_unique=="True" and self.teban=="w":
            if int(self.tesuu) <17 and self.board[1][5]=="s":
                self.score+=3
            if int(self.tesuu) <21 and self.board[1][2]=="s" and self.board[1][4]=="g" and self.board[0][3]=="g" and self.board[7][7]=="k":
                self.score+=3 #美濃
            if int(self.tesuu) <32 and self.board[2][3]=="g" and self.board[1][2]=="s" and self.board[0][3]=="g":
                self.score+=5 #高美濃
            if int(self.tesuu) <35 and self.board[0][0]=="k" and self.board[1][1]=="s" and self.board[1][0]=="l" and self.board[0][1]=="n" and self.board[0][2]=="g":
                self.score+=3 #振り穴
            if int(self.tesuu) <41 and self.board[1][1]=="k" and self.board[2][1]=="s" and self.board[1][2]=="g":
                self.score+=7 #銀冠




    def changing_sfen(self):
        self.count=0 #sfen変換に使うパラメータ
        self.output_sfen="" #初期化しないと前の局面と混ざる。
        for k in range(9):#縦
            if self.count>0:
                self.output_sfen="".join(tuple([self.output_sfen,str(self.count)]))
                self.count=0
            if k>0:
                self.output_sfen="".join(tuple([self.output_sfen,"/"]))

            for l in range(9):#横
                if  "o" in self.board[k][l]:
                    self.count+=1
                
                else:
                    if self.count>0:
                        self.output_sfen="".join(tuple([self.output_sfen,str(self.count),self.board[k][l]]))
                        self.count=0
                    else:
                        self.output_sfen="".join(tuple([self.output_sfen,self.board[k][l]]))



class Multi_Gen_teacher:
    def __init__(self,SendComTuple,exeFile,depth,at_thread,sfen_list,start,stop):
        self.usi=ayane.UsiEngine()
        # YaneuraOuと接続

        self.exeFile=exeFile
        # YaneuraOuまでのパス

        self.settings_of_engine=SendComTuple
        # YaneuraOuの設定

        self.go_depth=depth
        # YaneuraOuのgoコマンドで送るdepth
        # 設定した方が圧倒的に速い。

        self.score=0
        # 評価値

        self.ThinkResult=""
        # YaneuraOuの思考結果を格納する

        self.send_sfen="startpos moves"
        # 開始局面以降のsfenを記録

        self.at_thread=str(at_thread)
        # Multi処理の行番号

        self.sfen_list=sfen_list

        self.start_line=start
        # 開始行数

        self.stop_line=stop
        # 終了行数

    def Multi_Pona(self):#マルチスレッド
        fname="".join(["tmp_kif/",self.at_thread,"_teacher.txt"])
        with open(fname,mode="w") as f:pass
        #ファイル生成

        self.usi.debug_print=False

        self.usi.connect(self.exeFile)
        #YaneuraOuの接続
        send="".join(self.settings_of_engine)
        self.usi.send_command(send)
        time.sleep(1)
        self.usi.send_command("isready\n")
        time.sleep(1)
        self.usi.send_command("usinewgame\n")
        #YaneuraOuの設定

        
        for i in range(self.start_line,self.stop_line):

            self.read_sfen=self.sfen_list[i].split()

            if len(self.read_sfen)%2==0:#偶数なら後手勝利
                self.result="-1"
            else:#奇数なら先手勝利
                self.result="1"
                
            self.sente_unique=""

            self.gote_unique=""
            
            self.send_sfen="startpos moves"
            
            self.tesuu=0
        
            self.teban="b"

            self.output=""

            self.output_sfen=""

            
            self.tegoma_sfen="-"
            #手駒を出力するための変数

            self.tegoma_dict={"R":0,"B":0,"G":0,"S":0,"N":0,"L":0,"P":0,
                            "r":0,"b":0,"g":0,"s":0,"n":0,"l":0,"p":0}
            #手駒用の辞書型配列
            
            self.board=[
            #盤面の記録用配列(list)
            #将棋のsfenの数字が逆転するので、処理を変える必要がある
            # 0   1   2   3   4   5   6   7   8  ...配列
            # 9   8   7   6   5   4   3   2   1  ...将棋
            ["l","n","s","g","k","g","s","n","l"],#0
            ["o","r","o","o","o","o","o","b","o"],#1
            ["p","p","p","p","p","p","p","p","p"],#2
            ["o","o","o","o","o","o","o","o","o"],#3
            ["o","o","o","o","o","o","o","o","o"],#4
            ["o","o","o","o","o","o","o","o","o"],#5
            ["P","P","P","P","P","P","P","P","P"],#6
            ["o","B","o","o","o","o","o","R","o"],#7
            ["L","N","S","G","K","G","S","N","L"]]#8

            for j in self.read_sfen:
                if "startpos" not in j and "moves" not in j:
                    #局面をsfenに変換
                    self.changing_sfen()
                    #self.output_sfenに現在のboardのsfenを格納

                    self.renew(j,self.teban) #renew(self,str,str)
                    #局面を更新
                    #評価値の関係上この順番
                    
                    self.get_score()
                    #次の一手を打った局面の相手の最善手の評価値を反転させたものを出す。
                    #処理して評価値をself.scoreに代入
                    
                    self.output="".join([
                        "sfen ",self.output_sfen,
                        " ",self.teban,
                        " ",self.tegoma_sfen,
                        " 0\nmove ",j,
                        "\nscore ",str(self.score),
                        "\nply ",str(self.tesuu),
                        "\nresult ",self.result,
                        "\ne\n"
                    ])
                    #sfen変換終了
                    
                    with open(fname,mode="a") as f:
                        f.write(self.output)
                    
                    
                    self.tesuu+=1
                    if self.result=="1":
                        self.result="-1"
                    
                    else:
                        self.result="1"
                    if self.teban=="b":
                        self.teban="w"
                    else:
                        self.teban="b"
            print(end=self.at_thread ,flush=True)
        self.usi.disconnect()
        


    def renew(self,next,color):
        self.send_sfen="".join(tuple([self.send_sfen," ",next]))
        #エンジンに送る用
        #連続したものなので初期化不要
        #board[y][x]となる点に注意
        
        self.x1=next[:1].translate(str.maketrans({"9":"0","8":"1","7":"2","6":"3","5":"4","4":"5","3":"6","2":"7","1":"8"}))
        self.y1=next[1:2].translate(str.maketrans({"a":"0","b":"1","c":"2","d":"3","e":"4","f":"5","g":"6","h":"7","i":"8"}))
        #1文字目と2文字目

        self.x2=next[2:3].translate(str.maketrans({"9":"0","8":"1","7":"2","6":"3","5":"4","4":"5","3":"6","2":"7","1":"8"}))
        self.y2=next[3:4].translate(str.maketrans({"a":"0","b":"1","c":"2","d":"3","e":"4","f":"5","g":"6","h":"7","i":"8"}))
        #3文字目と4文字目
        
        if "*" in next:
            #1文字目に打った手駒
            self.renew_koma=self.tegoma(self.x1,1,color)
            self.board[int(self.y2)][int(self.x2)]=self.renew_koma
        else:
            self.x1=int(self.x1)
            self.x2=int(self.x2)
            self.y1=int(self.y1)
            self.y2=int(self.y2)

            if "o" not in self.board[self.y2][self.x2]:
                self.tegoma(self.board[self.y2][self.x2],0,color)
                self.board[self.y2][self.x2]=self.board[self.y1][self.x1]
                self.board[self.y1][self.x1]="o"

            else:
                self.board[self.y2][self.x2]=self.board[self.y1][self.x1]
                self.board[self.y1][self.x1]="o"


            if "+" in next:#成り
                self.board[self.y2][self.x2]="".join(["+",self.board[self.y2][self.x2]])


    def tegoma(self,koma,option,color):
        self.tegoma_sfen="" #"-"が入ってるのであらかじめ初期化
        if "+" in koma:
            koma=koma[1:]
        #colorはtebanのこと
        #komaには、self.board[y][x]で取得したものが代入される
        #option=0...komaの手駒取得(color不使用)
        #option=1...komaの手駒使用(colorでどちらの手駒を使ったか区別)
        #           blackなら大文字、whiteなら小文字を減らす
        if option==0:
            self.true_koma=koma.swapcase()
            self.tegoma_dict[self.true_koma]+=1
        elif option==1:
            if color == "b":
                self.true_koma=koma
            else:
                self.true_koma=koma.lower()

            self.tegoma_dict[self.true_koma]-=1
        for z in self.tegoma_dict.keys():
            if self.tegoma_dict[z]>0:
                if self.tegoma_dict[z]>1:
                    self.tegoma_sfen="".join([self.tegoma_sfen,str(self.tegoma_dict[z]),z])
                else:
                    self.tegoma_sfen="".join(tuple([self.tegoma_sfen,z]))
        return self.true_koma


    def get_score(self):
        self.usi.usi_position(self.send_sfen)
        # 先にrenewを実行することで、次の一手を打った後に
        # 相手が指す最善手の評価値を反転させて、高めの精度の評価値反映が可能
        self.usi.usi_go_and_wait_bestmove("".join(["depth ",self.go_depth,"\n"]))
        #ここでAyaneはUsiThinkResultクラスをthink_resultに代入。
        self.ThinkResult=self.usi.think_result.to_string().split()
        self.cp_admission=0
        self.mate_admission=0
        self.bestmove=0
        for k in self.ThinkResult:
            if self.cp_admission==0 and "cp" in k:
                self.cp_admission=1
            elif self.mate_admission==0 and "mate" in k:
                self.mate_admission=1
            elif self.cp_admission==1:
                self.score=int(k)
                self.cp_admission=2
            elif self.mate_admission==1:
                if k=="-0" or "0":
                    self.score=-100000
                    self.mate_admission=2
                # 詰みは0で投了のため、0なら問答無用で-100000
                # 後でしっかり100000に変換されるため、指し手は正しく評価される
                if int(k) < 0:
                    self.score=-100000-int(k)
                    self.mate_admission=2
                elif int(k) > 0:
                    self.score=100000-int(k)
                    self.mate_admission=2
        
        # 評価値をここで反転させる
        self.score= -1*self.score
            
        """
        独自設定
        """
        if int(self.tesuu) <10 and self.board[7][2]=="R" and self.teban=="b":
            self.sente_unique="True"
            self.score += 10
        if self.sente_unique=="True" and self.teban=="b":
            if int(self.tesuu) <17 and self.board[7][3]=="S":
                self.score+=3
            if int(self.tesuu) <25 and self.board[7][6]=="S" and self.board[7][4]=="G" and self.board[8][5]=="G" and self.board[7][7]=="K":
                self.score+=3 #美濃
            if int(self.tesuu) <32 and self.board[6][5]=="G" and self.board[7][6]=="S" and self.board[8][5]=="G" and self.board[7][7]=="K":
                self.score+=5 #高美濃
            if int(self.tesuu) <35 and self.board[8][8]=="K" and self.board[7][7]=="S" and self.board[7][8]=="L" and self.board[8][7]=="N" and self.board[6][8]=="G":
                self.score+=3 #振り穴
            if int(self.tesuu) <41 and self.board[7][7]=="K" and self.board[6][7]=="S" and self.board[7][6]=="G":
                self.score+=7 #銀冠
        
        if int(self.tesuu) <10 and self.board[1][6]=="r" and self.teban=="w":
            self.gote_unique="True"
            self.score += 10
        if self.gote_unique=="True" and self.teban=="w":
            if int(self.tesuu) <17 and self.board[1][5]=="s":
                self.score+=3
            if int(self.tesuu) <21 and self.board[1][2]=="s" and self.board[1][4]=="g" and self.board[0][3]=="g" and self.board[7][7]=="k":
                self.score+=3 #美濃
            if int(self.tesuu) <32 and self.board[2][3]=="g" and self.board[1][2]=="s" and self.board[0][3]=="g":
                self.score+=5 #高美濃
            if int(self.tesuu) <35 and self.board[0][0]=="k" and self.board[1][1]=="s" and self.board[1][0]=="l" and self.board[0][1]=="n" and self.board[0][2]=="g":
                self.score+=3 #振り穴
            if int(self.tesuu) <41 and self.board[1][1]=="k" and self.board[2][1]=="s" and self.board[1][2]=="g":
                self.score+=7 #銀冠




    def changing_sfen(self):
        self.count=0 #sfen変換に使うパラメータ
        self.output_sfen="" #初期化しないと前の局面と混ざる。
        for k in range(9):#縦
            if self.count>0:
                self.output_sfen="".join(tuple([self.output_sfen,str(self.count)]))
                self.count=0
            if k>0:
                self.output_sfen="".join(tuple([self.output_sfen,"/"]))

            for l in range(9):#横
                if  "o" in self.board[k][l]:
                    self.count+=1
                
                else:
                    if self.count>0:
                        self.output_sfen="".join(tuple([self.output_sfen,str(self.count),self.board[k][l]]))
                        self.count=0
                    else:
                        self.output_sfen="".join(tuple([self.output_sfen,self.board[k][l]]))






class Conduct_Converter:
    def __init__(self):
        """
        ここの数値は設定に合わせて変更してほしい
        変数名がそのままやねうらおう側のオプション名となっている。
        \nは改行のこと。
        これがないと処理がうまくいかないので注意
        Ayaneruもダウンロードすること
        """


        self.exeFile="exe/YaneuraOuV489_NNUE-HalfKPE9.exe"
        #YaneuraOuの実行ファイル名を記述
        #拡張子まで入力


        """
        --------------------------
        SendComTuple
        やねうらおうにコマンド送信
        --------------------------
        """

        self.multipv = "multipv 1\n"
        #候補手の数
        #1のままで良い。次善手を出力するなら
        #クラス内のbestmoveをいじくってほしい


        self.threads = "threads 1\n"
        #YaneuraOu側に割り当てるスレッド。
        #Depthに応じて調整
        #この時点で使用するスレッド数は
        #4(棋譜処理用:30行後くらいに記述) + 4*2 = 8スレッド
        #4*2はYaneuraOuが棋譜処理それぞれで起動されるため。

        self.usi_hash = "usi_hash 524\n"
        #YaneuraOu側の確保するメモリ


        self.bookfile = "bookfile user_book2\n"
        #定跡ファイル指定。
        #bookfileがわからなければ"no_book"に書き換えてもよい

        self.bookmoves = "\n" #"bookmoves 32\n"
        #定跡を何手目まで読み込むか
        
        self.depth="1"
        self.setoption_name_DepthLimit_value="".join(["setoption_name_DepthLimit_value ",self.depth,"\n"])
        #読みを深さ6で打ち切り。
        #こちらを設定すると、読みすぎることなく早く終わってくれるため。
        #YaneuraOuのgensfen並みの生成速度を目指したい

        """
        =================================
        SendComTuple はここまで
        =================================

        """
        
        self.workers=2
        # 棋譜を何スレッドに分割して処理するか
        # 棋譜処理用のスレッド
        # default = 4 (int)
        # 総使用スレッド数は、
        # (YaneuraOu側)*(max_workers)+(max_workers)
        # となるので注意

        self.opFile=input("読み込むsfenファイルを拡張子まで入力してください：\n")
        #opFileはファイル名
        #openに必要

        self.SendComTuple=[
            self.multipv,
            self.threads,
            self.usi_hash,
            self.bookfile,
            self.bookmoves,
            self.setoption_name_DepthLimit_value
        ]


    def Calling_PonaMethod(self):
        self.gen = Gen_teacher(self.opFile,self.SendComTuple,self.exeFile,self.depth)
        #クラスを短く。
        #__init__に値を渡してクラス生成
        self.gen.read()
        #ファイルを開く
        self.gen.PonaMethod()

    
    def Calling_Non_lambda(self):
        self.gen = Gen_teacher(self.opFile,self.SendComTuple,self.exeFile,self.depth)
        self.gen.read()
        self.gen.None_Lambda()

    
    def Calling_MultiPona(self):
        
        self.Multi_read()
        self.Multi_calc()
        #multi_gen = Multi_Gen_teacher(self.SendComTuple,self.exeFile,self.depth,,self.sfen_tuple[i])
        #multi_gen.Multi_PonaMethod()
        future_result=None

        with futures.ThreadPoolExecutor(max_workers=self.workers) as executor:#落ちるので、恐らく回数分けないとだめ。
            print("start...")
            
            future=[
                executor.submit
                (Calling_MultiPona_Main,[
                    self.SendComTuple,  # 1
                    self.exeFile,       # 2
                    self.depth,         # 3
                    i,                  # 4
                    self.sfen_tuple,    # 5
                    self.arg_lines[i],  # 6
                    self.arg_lines[i+1] # 7
                    ])
                     for i in range(self.workers)]
            # 引数一覧:
            #  1. SendComTuple  : YaneuraOuの設定が入った配列,
            #  2. exeFile       : YaneuraOuのファイルパス,
            #  3. depth         : goコマンドのdepth, 
            #  4. at_thread     : 処理ごとの割り当て番号,
            #  5. sfen_list     : 読み込んだsfen,
            #  6. start         : 開始行,
            #  7. stop          : 終了行
            """
            for i in range(self.workers):
                future_result=futures.Future.done(future[i])
                print(future_result)
            """
            # Python公式: 
            # Futureはsubmitの後で生成されて、.result(executorの代入された変数とか)だと、executor.submitの返り値を取得するらしい
        
        print("merge all files...")
        with open("all_teacher.txt",mode="w")as f:
            for i in range(self.workers):
                fname="".join(["tmp_kif/",str(i),"_teacher.txt"])
                with open(fname,mode="r")as g:
                    data=list(g)
                    for i in data:
                        f.write(i)
                os.remove(fname)
        print("all done")


    def Multi_read(self):
        print("".join([self.opFile," open\n"]))
        
        with open(self.opFile,mode="r") as pos:

            self.sfen_tuple=tuple(pos)
            self.lines=len(self.sfen_tuple)

    def Multi_calc(self):
        each_lines=math.floor(self.lines/self.workers)
        amari=self.lines%self.workers
        if amari>0:
            self.arg_lines=[each_lines*i+amari if i == self.workers else each_lines*i  for i in range(self.workers+1)]
        else:
            self.arg_lines=[each_lines*i for i in range(self.workers+1)]


#並行処理実行用関数
def Calling_MultiPona_Main(args):
    multi_gen = Multi_Gen_teacher(*args)
    multi_gen.Multi_Pona()




class Method_Select:
    def PonaMethod(self):
        conduct=Conduct_Converter()
        # 通常プロセス
        conduct.Calling_PonaMethod()
        

    def None_Lambda(self):

        conduct=Conduct_Converter()
        conduct.Calling_None_Lambda()
        # 全試合を引き分けにする(result=0)
        # 大量の短い棋譜を教師にする場合はおすすめ

    def Multi_Pona(self):
        conduct=Conduct_Converter()
        conduct.Calling_MultiPona()

if __name__ == "__main__":
    text = ""
    while text!="quit":
        text=input("モードを選んで数字を入力してください\n終了するにはquitと入力してください\nPonaMethod:1\nNone_Lambda:2\nMulti_Pona:3\n")
        select=Method_Select()
        if text=="1":
            select.PonaMethod()
        elif text=="2":
            select.None_Lambda()
        elif text=="3":
            select.Multi_Pona()