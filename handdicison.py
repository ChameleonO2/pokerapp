import random
import re
class PokerCard():
    MARK_LIST = ['Spade','Club','Heart','Dia']
    MAX_CARDS = 6
    regex = r'[1-9,t,T,j,J,q,Q,k,K][s,S,c,C,h,H,d,D]'
    pattern = ""
    usecardlist=[]

    def __init__(self, ):
        self.pattern = re.compile(self.regex)
        for i in range(52):
            self.usecardlist.append(0)

    def init_cardlist(self):
        usecardlist=[]
        for i in range(52):
            self.usecardlist.append(False)

    def add_cardlsit(self,num):
        self.usecardlist[num] = True

    def disern_card(self, num):
        """
            与えられた数字を元にカードの値とマークを返す.
        """
        return (num % 13 + 1,self.MARK_LIST[num // 13])

    def inverse_card(self, card):
        """
            与えられたカードの値とマークを元にカードに割り当てた数字を返す.
        """
        for i in range(4):
            if card[1] == self.MARK_LIST[i]:
                return (card[0] - 1) + i * 13

    def convert_cardinfo(self,str1):
        """
        [数字，マーク]のフォーマットで与えられた情報を数値として返す．
        """
        markstr1 = [['s','S'],['c','C'],['h','H'],['d','D']]

        if str1[0] in ['t','T']:
            tmp = 9
        elif str1[0] in ['j','J']:
            tmp = 10
        elif str1[0] in ['q','Q']:
            tmp = 11
        elif str1[0] in ['k','K']:
            tmp = 12
        else:
            tmp = int(str1[0]) - 1

        for i , val in enumerate(markstr1):
            if str1[1] in val:
                tmp += i*13
        return tmp

    def is_flash(self, cards):
        """
            カードがフラッシュなTrueを返す．
        """
        for i in range(1,len(cards)):
            if not(cards[i-1][1] == cards[i][1]):
                return False
        return True

    def is_straight(self, cards):
        """
            カードがストレートならTrueを返す．
        """
        tmp = []
        for val in cards:
            tmp.append(val[0])
        tmp.sort()
        for i in range(1,len(tmp)):
            if not(tmp[i-1]+1 == tmp[i]):
                return False
        return True
    
    def is_straightflash(self, cards):
        """
            カードがストフラならTrueを返す．
        """
        if(self.is_straight(cards) and self.is_flash(cards)):
            return True
        else:
            return False

    def is_4curds(self, cards):
        """
            与えられたカードが4 of a kind ならばTrueを返す．.
        """
        tmp = []
        for val in cards:
            tmp.append(val[0])
        tmp_d = [x for x in set(tmp) if tmp.count(x) > 3]
        if len(tmp_d) == 0:
            return False
        return True

    def is_fullhouce(self,cards):
        """
            フルハウス
        """
        tmp = []
        for val in cards:
            tmp.append(val[0])
        tmp_d = [x for x in set(tmp) if tmp.count(x) > 1]
        if len(tmp_d)>1:
            tmp_d = [x for x in set(tmp) if tmp.count(x) > 2]
            if len(tmp_d)>0:
                return True
        return False


    def is_3curds(self,cards):
        """
            与えられたカードが3 of a kind ならばTrueを返す．.
        """
        if self.is_fullhouce(cards):
            return False
        if self.is_4curds(cards):
            return False
        tmp = []
        for val in cards:
            tmp.append(val[0])
        tmp_d = [x for x in set(tmp) if tmp.count(x) > 2]
        if len(tmp_d)>0:
            return True
        return False

    def is_2pair(self,cards):
        """
            与えられたカードが2pair ならばTrueを返す．.
        """
        if self.is_fullhouce(cards):
            return False
        tmp = []
        for val in cards:
            tmp.append(val[0])
        tmp_d = [x for x in set(tmp) if tmp.count(x) > 1]
        if len(tmp_d)>1:
            return True
        return False
    
    def is_1pair(self,cards):
        """
            与えられたカードが1pair ならばTrueを返す．.
        """
        if self.is_fullhouce(cards):
            return False
        if self.is_4curds(cards):
            return False
        if self.is_3curds(cards):
            return False
        tmp = []
        for val in cards:
            tmp.append(val[0])
        tmp_d = [x for x in set(tmp) if tmp.count(x) > 1]
        if len(tmp_d)>0:
            return True
        return False

    def determine_hand(self,cards):
        """
        役の判定
        """
        if self.is_straightflash(cards):
            return 8
        if self.is_4curds(cards):
            return 7
        if self.is_fullhouce(cards):
            return 6
        if self.is_flash(cards):
            return 5
        if self.is_straight(cards):
            return 4
        if self.is_3curds(cards):
            return 3
        if self.is_2pair(cards):
            return 2
        if self.is_1pair(cards):
            return 1
        return 0

    def compare_strength(self,cardsarray,handval):
        tmp = []
        tmp2 = []
        for val in cardsarray[0]:
            tmp.append(val[0])
        tmp.sort()
        for val in cardsarray[0]:
            tmp2.append(val[0])
        tmp2.sort()
        
        if handval in [8,5,4]:
            if tmp[0] > tmp2[0]:
                return (0,tmp)
            elif tmp[0] < tmp2[0]:
                return (1,tmp2)
            return (-1,None)

        elif handval in [7,6,3]:
            if handval == 7:
                tmp_d = [x for x in set(tmp) if tmp.count(x) > 3]
                tmp2_d = [x for x in set(tmp2) if tmp2.count(x) > 3]
            if handval in [6,3]:
                tmp_d = [x for x in set(tmp) if tmp.count(x) > 2]
                tmp2_d = [x for x in set(tmp2) if tmp2.count(x) > 2]
                
            if tmp_d[0] > tmp2_d[0]:
                return (0,tmp_d[0])
            else :
                return (1,tmp2_d[0])
        elif handval == 2:
            return 0
        elif handval == 1:
            return 0
        else:
            return 0

    
    def select_cards(self,cards):
        i = self.MAX_CARDS 
        allpat = []
        while 1 < i :
            for j in range(i):
                tmp = cards[:]
                tmp.pop(self.MAX_CARDS - i)
                tmp.pop(j)
                allpat.append(tmp)
            i -= 1
        return allpat

    def strength_hand(self,cardsarray):
        maxhandval = 0
        maxhandlist=[]
        for cards in cardsarray:
            handval = self.determine_hand(cards)
            if(maxhandval < handval):
                maxhandval = handval
                maxhandlist = []
                maxhandlist.append(cards)
                print("reset!=========================")
                print(cards)
            elif(maxhandval == handval):
                maxhandlist.append(cards)
                print(cards)
        print(maxhandlist)
        return maxhandval
    



if __name__ == '__main__':
    hoge = PokerCard()
    print("debug handdicison")
    tmp = []
    card = [] 
    for i in range(52):
        card.append(False)
    for i in range(7):
        t = random.randrange(52)
        while card[t] != False:
            t = random.randrange(52)
        card[t] = True 
        tmp.append(hoge.disern_card(t))
    print(tmp)
    print(hoge.strength_hand(hoge.select_cards(tmp)))
    # for val in hoge.select_cards(tmp):
    #     print(val)
