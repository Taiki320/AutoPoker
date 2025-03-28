import random
import copy
import time

class Player:#プレイヤーのクラス
    def __init__(self,name):
        self.name = name

class Cards:#トランプの数字とマークを保持するクラス(52個)
    def __init__(self):
        self.nums = [1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.marks = ["♡","♡","♡","♡","♡","♡","♡","♡","♡","♡","♡","♡","♡","♢","♢","♢","♢","♢","♢","♢","♢","♢","♢","♢","♢","♢","♤","♤","♤","♤","♤","♤","♤","♤","♤","♤","♤","♤","♤","♧","♧","♧","♧","♧","♧","♧","♧","♧","♧","♧","♧","♧"]

class Deck:#stackを使ったデッキ表現
    def __init__(self):
        self.deck = list(range(52))#class Cardsで保持しているトランプのインデックスとして使用。山札を表現する。

    def pop(self):#山札のリストをシャッフルし、返す
        random.shuffle(self.deck)#山札をシャッフル
        return self.deck.pop()#山札のカードを一枚ごとに返す、それと同時に山札からは削除される

class Game:
    def __init__(self):#初期設定、classとつなげる
        name1 = "cpu1"
        name2 = "cpu2"
        self.p1 = Player(name1)
        self.p2 = Player(name2)
        self.deck = Deck()
        self.cards = Cards()

    def num_check(self,card_nums):#数字の重複の数を確認
        nums_multi = 0 #数字の重複
        for s in set(card_nums):
            if nums_multi < card_nums.count(s):
                nums_multi = card_nums.count(s)
        return nums_multi

    def mark_check(self,cards_marks):#マークの重複の数を確認
        marks_multi = 0#マークの重複
        for s in set(cards_marks):
            if marks_multi < cards_marks.count(s):
                marks_multi = cards_marks.count(s)
        return marks_multi

    def straight_check(self,num):#ストレートかどうかの判定のための関数
        card_nums = num
        if 1 in card_nums and 10 in card_nums:#ストレート時の[10,11,12,13,1]のための表現
            card_nums.remove(1)#カードの数字のリストの「1」を削除
            card_nums.append(14)#カードの数字のリストの最後に14を追加

        max_num = max(card_nums)#リストの最大値
        min_num = min(card_nums)#リストの最小値
        ave_num = (max_num + min_num)/2#リストの平均値

        if max_num - min_num == 4 and ave_num in card_nums and ave_num - 1 in card_nums and ave_num + 1 in card_nums:#大きいー小さい＝４の時に平均値とそれの＋－1の値が存在するときに連続しているといえる
            return True

    def roll_check(self,hand):#どの役かを確認し、値を返す
        hand_nums = []
        hand_marks = []
        i = 0
        lengh = len(hand)#カードの枚数分
        while lengh != 0:
            hand_nums.append(self.cards.nums[hand[i]])
            hand_marks.append(self.cards.marks[hand[i]])
            lengh = lengh - 1
            i = i + 1
        
        if len(hand) == 1:#カードの枚数分で分けている
            return "ぶた",1
        if len(hand) == 2:
            if len(set(hand_nums)) == 1 and self.num_check(hand_nums) == 2:
                return "ワンペア",3
            else:return "ぶた",1
        if len(hand) == 3:
            if len(set(hand_nums)) == 2 and self.num_check(hand_nums) == 2:
                return "ワンペア",3
            elif len(set(hand_nums)) == 1 and self.num_check(hand_nums) == 3:
                return "スリーカード",5
            else:return "ぶた",1
        if len(hand) == 4:
            if len(set(hand_nums)) == 3 and self.num_check(hand_nums) == 2:
                return "ワンペア",3
            elif len(set(hand_nums)) == 2 and self.num_check(hand_nums) == 2:
                return "ツーペア",5
            elif len(set(hand_nums)) == 2 and self.num_check(hand_nums) == 3:
                return "スリーカード",5
            elif len(set(hand_nums)) == 1 and self.num_check(hand_nums) == 4:
                return "フォーカード",30
            else:return "ぶた",1
        if len(hand) == 5:
            if len(set(hand_nums)) == 4 and self.num_check(hand_nums) == 2:
                return "ワンペア",3
            elif len(set(hand_nums)) == 3 and self.num_check(hand_nums) == 2:
                return "ツーペア",5
            elif len(set(hand_nums)) == 3 and self.num_check(hand_nums) == 3:
                return "スリーカード",5
            elif self.straight_check(hand_nums) and self.mark_check(hand_marks) != 5:
                return "ストレート",12
            elif self.mark_check(hand_marks) == 5 and self.straight_check(hand_nums) != True:
                return "フラッシュ",15
            elif len(set(hand_nums)) == 2 and self.num_check(hand_nums) == 3:
                return "フルハウス",20
            elif len(set(hand_nums)) == 2 and self.num_check(hand_nums) == 4:
                return "フォーカード",30
            elif self.straight_check(hand_nums) and self.mark_check(hand_marks) == 5:
                if 1 in hand_nums and 10 in hand_nums:
                    return "ロイヤルストレートフラッシュ",100
                else:
                    return "ストレートフラッシュ",40
            else:
                return "ぶた",1
        return "ぶた",1
 
    def first(self,name,draw):
        card_nums = []
        card_marks = []
        cards = []
        count = 0
        print("__"+name+"_____")
        while draw != 0:
            cards.append(self.deck.pop())
            card_nums.append(self.cards.nums[cards[count]])
            card_marks.append(self.cards.marks[cards[count]])
            print(card_marks[count]+str(card_nums[count]),end = " ")
            draw = draw - 1
            count = count + 1
        print(" ")
        return cards

    def alloutput(self,name1,hand1,count1,name2,hand2,name3,hand3,count3,name4,hand4,name5,hand5,name6,hand6):#出力をしないといけないすべての処理を出力
        deck_count = len(self.deck.deck)
        print("山札:残りの枚数="+str(deck_count))
        self.output(name1,hand1,count1)
        self.output2(name2,hand2)
        self.output(name3,hand3,count3)
        self.output2(name4,hand4)
        self.output2(name5,hand5)
        self.output2(name6,hand6)

    def output(self,name,hand,count):
        card_nums = []
        card_marks = []
        i = 0
        print("__"+name+"_____")
        while count != 0:
            card_nums.append(self.cards.nums[hand[i]])
            card_marks.append(self.cards.marks[hand[i]])
            print(card_marks[i]+str(card_nums[i]),end = " ")
            count = count - 1
            i = i + 1
        print(" ")

    def output2(self,name,hand):
        card_nums = []
        card_marks = []
        lengh = len(hand)
        i = 0
        print("__"+name+"_____")
        while lengh != 0:
            card_nums.append(self.cards.nums[hand[i]])
            card_marks.append(self.cards.marks[hand[i]])
            print(card_marks[i]+str(card_nums[i]),end = " ")
            lengh = lengh - 1
            i = i + 1
        print(" ")

    def choice2(self,hand,count,conf_card,conf_result,conf_resultN):
        w,num = self.roll_check(hand)
        conf_result += num
        lengh = len(hand)
        i = 0
        while lengh != 0:
            conf_card.append(hand[i])
            lengh = lengh - 1
            i = i + 1
        conf_resultN.append(w)
        hand = []
        count = 0
        return hand,count,conf_card,conf_result,conf_resultN

    def pattern(self,hand,field): #仮想手札に場からカードを代入、一番優先順位が高いものの手札を調べる
        high_choice = 0 
        high_dust = 0
        high_rank = 100#優先順位の初期値
        high_hand = []#一番優先順位が高い手札
        count = 0 
        rank = 0
        choice = 0
        for i in range(1,8,1):#1~7までを回す
            dust = 0#仮の捨て札のはこ
            temp = copy.copy(hand)#仮想手札の代入とリセット
            pig = 0#豚かどうかの判定
            rank = 100
            if len(hand) >= 2:
                if i==1:#一枚を場の左からとる
                    print("pattern1")
                    Incard = 0
                    temp.append(field[Incard])#場から入れるカードを手札に代入
                    print("temp_count=",len(temp))
                    if len(temp) == 5 :
                        rank,choice,pig = self.priority_check5(temp) 
                    if pig == 1 or len(temp) <= 4:
                        rank,temp,dust,choice = self.priority_check4U(temp,high_rank)
                if i==2:#一枚を場の真ん中からとる
                    print("pattern2")
                    Incard = 1
                    temp.append(field[Incard])#場から入れるカードを手札に代入
                    print("temp_count=",len(temp))
                    if len(temp) == 5 :
                        rank,choice,pig = self.priority_check5(temp) 
                    if pig == 1 or len(temp) <= 4:
                        rank,temp,dust,choice = self.priority_check4U(temp,high_rank)
                if i==3:#一枚を場の右からとる
                    print("pattern3")
                    Incard = 2
                    temp.append(field[Incard])#場から入れるカードを手札に代入
                    print("temp_count=",len(temp))
                    if len(temp) == 5 :
                        rank,choice,pig = self.priority_check5(temp) 
                    if pig == 1 or len(temp) <= 4:
                        rank,temp,dust,choice= self.priority_check4U(temp,high_rank)
                if len(hand)<=3:
                    if i==4:#二枚を場の左と右からとる
                        print("pattern4")
                        Incard = 0
                        temp.append(field[Incard])#場から入れるカードを手札に代入 
                        Incard = 2
                        temp.append(field[Incard])#場から入れるカードを手札に代入
                        print("temp_count=",len(temp))
                        if len(temp) == 5 :
                            rank,choice,pig = self.priority_check5(temp) 
                        if pig == 1 or len(temp) <= 4:
                            rank,temp,dust,choice= self.priority_check4U(temp,high_rank)
                    if i==5:#二枚を場の真ん中と右からとる
                        print("pattern5")
                        Incard = 0
                        temp.append(field[Incard])#場から入れるカードを手札に代入
                        Incard = 1
                        temp.append(field[Incard])#場から入れるカードを手札に代入
                        print("temp_count=",len(temp))
                        if len(temp) == 5 :
                            rank,choice,pig = self.priority_check5(temp) 
                        if pig == 1 or len(temp) <= 4:
                            rank,temp,dust,choice= self.priority_check4U(temp,high_rank)
                    if i==6:#二枚を場の真ん中と左からとる
                        print("pattern6")
                        Incard = 1
                        temp.append(field[Incard])#場から入れるカードを手札に代入
                        Incard = 2
                        temp.append(field[Incard])#場から入れるカードを手札に代入
                        print("temp_count=",len(temp))
                        if len(temp) == 5 :
                            rank,choice,pig = self.priority_check5(temp) 
                        if pig == 1 or len(temp) <= 4:
                            rank,temp,dust,choice= self.priority_check4U(temp,high_rank)
            elif len(hand)==1 or len(hand)==0 :
                if i==7:#三枚を場の右と真ん中と左からとる
                    print("pattern7")
                    Incard = 0
                    temp.append(field[Incard])
                    Incard = 1
                    temp.append(field[Incard])
                    Incard = 2
                    temp.append(field[Incard])
                    if len(temp) == 5 :
                        rank,choice,pig = self.priority_check5(temp) 
                    if pig == 1 or len(temp) <= 4:
                        rank,temp,dust,choice= self.priority_check4U(temp,high_rank)

            if high_rank > rank:#一番優先順位が高いものを決定する(値が低いものほど優先順位が高い)
                high_i = i#パターンの数
                high_rank = rank#一番高い優先順位の記録
                high_hand = temp#一番高い優先順位の手札
                high_choice = choice#STEP3で1,2どちらを選ぶか
                high_dust = dust 
                count = len(high_hand)
            print("\n")

        if high_i == 1:
            if len(self.deck.deck) != 0:
                field[0] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
        elif high_i == 2:
            if len(self.deck.deck) != 0:
                field[1] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
        elif high_i == 3:
            if len(self.deck.deck) != 0:
                field[2] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
        elif high_i == 4:
            if len(self.deck.deck) > 1:
                field[0] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
                field[2] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
        elif high_i == 5:
            if len(self.deck.deck) > 1:
                field[0] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
                field[1] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
        elif high_i == 6:
            if len(self.deck.deck)  > 1:
                field[1] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
                field[2] = self.deck.pop()#山札から場のカードへ追加及び、手札に入れる場のカードを削除
        elif high_i == 7:
            if len(self.deck.deck) != 0:
                field[0] = self.deck.pop()
            if len(self.deck.deck) != 0:
                field[1] = self.deck.pop()
            if len(self.deck.deck) != 0:
                field[2] = self.deck.pop()

        return high_hand,high_choice,count,field,high_dust

    def priority_check5(self,hand):#手札が５枚の時には豚以外は即確定へ、豚は4枚以下の場合と同じところで処理する
        i = 0
        hand_num = []
        hand_mark = []
        lengh = len(hand)
        while lengh != 0:#手札をマークと数字で保存
            hand_num.append(self.cards.nums[hand[i]])
            hand_mark.append(self.cards.marks[hand[i]])
            lengh = lengh - 1
            i = i + 1
        #check
        print(hand_num,hand_mark)
        if self.straight_check(hand_num) and self.mark_check(hand_mark) == 5:#return rank,choice,豚かの判断
            if 1 in hand_num and 10 in hand_num:
                return 1,2,0#ロイヤルストレートフラッシュ(揃う)
            else:
                return 2,2,0#ストレートフラッシュ(揃う)
        elif len(set(hand_num)) == 2 and self.num_check(hand_num) == 4:
            return 3,2,0#フォーカード(揃う)
        elif len(set(hand_num)) == 2 and self.num_check(hand_num) == 3:
            return 4,2,0#フルハウス(揃う)
        elif self.mark_check(hand_mark) == 5 and self.straight_check(hand_num) != True:
            return 5,2,0#フラッシュ(揃う)
        elif self.straight_check(hand_num) and self.mark_check(hand_mark) != 5:
            return 6,2,0#ストレート(揃う)
        elif len(set(hand_num)) == 2 and self.num_check(hand_num) == 2:
	        return 7,2,0#スリーカード(揃う)
        elif len(set(hand_num)) == 3 and self.num_check(hand_num) == 2:
            return 8,2,0#ツーペア(揃う)
        elif len(set(hand_num)) == 4 and self.num_check(hand_num) == 2:
            return 9,2,0#ワンペア(揃う)
        else:
            return 0,1,1#豚(priority_check4Uに移動)

    def priority_check4U(self,hand,high_rank):#手札が4以下の場合と豚の時には一枚引かないといけないそのための処理
        i = 0
        high_hand = 0
        high_dust = 0
        high_choice = 0
        lengh = len(hand)
        for i in range(lengh):
            temp = copy.copy(hand)
            hand_num = []
            hand_mark = []
            dust = 0
            rank = 0

            print("捨て札=",str(i))
            dust = temp[i]
            print("dust=",dust)
            del temp[i]
            print("dust以外=",temp)
            lengh = len(temp)
            j = 0
            while lengh != 0:#手札をマークと数字で保存
                hand_num.append(self.cards.nums[temp[j]])
                hand_mark.append(self.cards.marks[temp[j]])
                lengh = lengh - 1
                j = j + 1
            #check
            print("hand=",hand_num,hand_mark)
            rank,choice = self.priority_check4(temp,hand_num,hand_mark)
            print("rank=",rank)

            if high_rank > rank:#一番優先順位が高いものを決定する(値が低いものほど優先順位が高い)
                high_rank = rank
                high_hand = temp
                high_dust = dust
                high_choice = choice 

        return high_rank,high_hand,high_dust,high_choice

    def priority_check4(self,hand,hand_num,hand_mark):
        hand.sort()
        max_num_continue = 0
        num_continue = 0
        i = 0
        j = 1
        max_num_continue = 1
        lengh = len(hand)
        while i != (lengh-1):
            i2 = i
            num_continue = 1
            j = i + 1
            while j != lengh:
                if (hand_num[j] - hand_num[i2]) == 1:
                    num_continue = num_continue + 1
                    i2 = i2 + 1
                    j = j + 1
                else:
                    break
            if max_num_continue < num_continue:
                max_num_continue = num_continue
            i = i + 1
        if len(hand) == 4:
            if self.mark_check(hand_mark) == 4:
                return 13,1#フラッシュ(揃うかも)
            elif self.mark_check(hand_mark) == 3:
                return 14,1#フラッシュ(もしかしたら揃うかも)
            else: return 32,1#豚
        elif len(hand) == 3:
            if self.num_check(hand_mark) == 3:
                return 10,1#スリーカード(揃う)
            elif len(set(hand_num)) == 2 and self.num_check(hand_num) == 2:
	            return 11,1#ワンペア(揃う)
            elif self.mark_check(hand_mark) == 3:
                return 15,1#フラッシュ(揃うかも)
            elif max_num_continue == 4:
                return 16,1#ストレート(もしかしたら揃うかも)
            else:return 31,1#豚
        elif len(hand) == 2:
            if len(set(hand_num)) == 1 and self.num_check(hand_num) == 2:
                return 12,1#ワンペア(揃う)
            else : return 30,1#豚

    def win(self,name1,hand1,name2,hand2,conf_result1,conf_resultN1,conf_result2,conf_resultN2):
        print("__結果発表_____")
        if len(hand1) != 0: 
            w1,num1 = self.roll_check(hand1)
            conf_result1 +=num1
            conf_resultN1.append(w1)
        print(name1+"の合計点="+str(conf_result1))
        print("出た役="+str(conf_resultN1))
        if len(hand2) != 0: 
            w2,num2 = self.roll_check(hand2) 
            conf_result2 +=num2
            conf_resultN2.append(w2)
        print(name2+"の合計点="+str(conf_result2))
        print("出た役="+str(conf_resultN2) )
        if conf_result1 > conf_result2:
            print("********"+name1+"の勝利!!***************")
        elif conf_result1 < conf_result2:
            print("********"+name2+"の勝利!!***************")
        else:
            print("________引き分け_________________")

    def play_game(self):
        print("「Quot」START!!")
        turn = 1
        #初期手札&確定(cpu1)
        draw = 3
        p1n = self.p1.name
        p1h = self.first(p1n,draw)
        count1_card = 3
        conf_card1 = []
        conf_result1 = 0
        conf_name1 = "確定"
        conf_resultN1 = []

        #初期手札&確定(cpu2)
        draw = 3
        p2n = self.p2.name
        p2h = self.first(p2n,draw)
        count2_card = 3
        conf_card2 = []
        conf_result2 = 0
        conf_name2 = "確定"
        conf_resultN2 = []

        #初期場
        draw = 3
        field_name = "場"
        field_card = self.first(field_name,draw)
        print(field_card)

        #捨て場
        dust_name="捨て場"
        dust_card = []

        print("\n")
        while len(self.deck.deck) != 0:
            print("\n")
            print("ターン"+str(turn))
            turn = turn + 1
        #cpu1
            #対戦手順1、対戦手順2
            print("cpu1>>場から好きなカードを手札が5枚を超えないように選んでください")
            p1h,choice,count1_card,field_card,dust = self.pattern(p1h,field_card)

            print(p1h,choice,count1_card,field_card,dust)
            time.sleep(1)
            #対戦手順3
            print("cpu1>>次の二つの選択肢から必要な動作を選択肢の最後の数字で選択してください")
            print(choice)
            if choice==1:
                dust_card.append(dust)
                print("choice = ",1)
            elif choice == 2 and count1_card == 5:
                p1h,count1_card,conf_card1,conf_result1,conf_resultN1 = self.choice2(p1h,count1_card,conf_card1,conf_result1,conf_resultN1)
                print("choice = ",2)

            self.alloutput(p1n,p1h,count1_card,conf_name1,conf_card1,p2n,p2h,count2_card,conf_name2,conf_card2,field_name,field_card,dust_name,dust_card)
            time.sleep(1)
            if len(self.deck.deck) == 0:
                break
            print("\n")

        #cpu2
            #対戦手順1、対戦手順2
            print("cpu2>>場から好きなカードを手札が5枚を超えないように選んでください")
            p2h,choice,count2_card,field_card,dust = self.pattern(p2h,field_card)
 
            print(p2h,choice,count2_card,field_card,dust)
            time.sleep(1)
            #対戦手順3
            print("cpu2>>次の二つの選択肢から必要な動作を選択肢の最後の数字で選択してください")
            print(choice)
            if choice==1:
                dust_card.append(dust)
                print("choice = ",1)
            elif choice == 2 and count2_card == 5:
                p2h,count2_card,conf_card2,conf_result2,conf_resultN2 = self.choice2(p2h,count2_card,conf_card2,conf_result2,conf_resultN2)
                print("choice = ",2)
            self.alloutput(p1n,p1h,count1_card,conf_name1,conf_card1,p2n,p2h,count2_card,conf_name2,conf_card2,field_name,field_card,dust_name,dust_card)
            time.sleep(1)
        self.win(p1n,p1h,p2n,p2h,conf_result1,conf_resultN1,conf_result2,conf_resultN2)
        print("「Quot」finish!!")
        while True:
            s = "q で終了 : "
            response = input(s)
            if response == 'q':
                break



game = Game()
game.play_game()




