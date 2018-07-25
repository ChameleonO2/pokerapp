import random
import re
import itertools
from tqdm import tqdm
class PokerCard():
    MARK_LIST = ['Spade','Club','Heart','Dia']
    MAX_CARDS = 6
    regex = r'[1-9,t,T,j,J,q,Q,k,K][s,S,c,C,h,H,d,D]'
    pattern = ""
    usecardlist=[]
    playercardlist = []
    communitycardlist = []

    def __init__(self, ):
        self.pattern = re.compile(self.regex)
        for i in range(52):
            self.usecardlist.append(False)

    def init_cardlist(self):
        usecardlist=[]
        playercardlist = []
        communitycardlist = []
        for i in range(52):
            self.usecardlist.append(False)

    def add_cardlsit(self,num):
        self.usecardlist[num] = True
        return num

    def set_communitycardlist(self,num):
        if (len(self.communitycardlist) <= 5):
            self.communitycardlist.append(self.disern_card(num))
            self.add_cardlsit(num)
            return
        else:
            print("規定値以上です")
            return 
    
    def get_communitycardlist(self,):
        return self.communitycardlist[:]
        
    def set_playercardlist(self,num):
        if (len(self.playercardlist) <= 2):
            self.playercardlist.append(self.disern_card(num))
            self.add_cardlsit(num)
            return
        else:
            print("規定値以上です")
            return 
    
    def get_playercardlist(self,):
        return self.playercardlist[:]
        
    def put_2cardlist(self,):
        """
        現在使用していないカード2枚の組み合わせを出力する．
        """
        tmp = []
        cnt = 0
        for i,val in enumerate(self.usecardlist):
            if val == False:
                tmp.append(self.disern_card(i))
            else:
                cnt+=1
        return list(itertools.combinations(tmp,2))

    def get_hand(self,cards):
        tmp = list(self.get_communitycardlist())
        tmp.extend(cards)
        handval,hand = self.strength_hand(self.select_cards(tmp))
        kicker = self.output_kicker(hand,handval)
        return hand,handval,kicker

    def get_playerhand(self,):
        return self.get_hand(self.get_playercardlist())
    



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
    
    def  show_handname(self,handval):
        if handval == 0:
            return "High Cards"
        elif handval == 1:
            return "One Pair"
        elif handval == 2:
            return "Two Pair"
        elif handval == 3:
            return "Three of a Kind"
        elif handval == 4:
            return "Straight"
        elif handval == 5:
            return "Flush"
        elif handval == 6:
            return "Full House"
        elif handval == 7:
            return "Four of a Kind"
        elif handval == 8:
            return "Straight Flush"
        return "error"


    def output_kicker(self,cards,handval):
        tmp = []
        for val in cards:
            tmp.append(val[0])
        tmp.sort()
        tmp.reverse()
        cards_tmp = tmp[:]
        if handval in [8,5,4]:
            return tmp
        elif handval in [7,6,3]:
            if handval == 7:
                tmp_d = [x for x in set(tmp) if tmp.count(x) > 3]
            if handval in [6,3]:
                tmp_d = [x for x in set(tmp) if tmp.count(x) > 2]
            cards_tmp = list(set(tmp))
            cards_tmp.remove(tmp_d[0])
            cards_tmp.sort()
            cards_tmp.reverse()
            tmp_d.extend(cards_tmp)
            return tmp_d
        elif handval == 2:
            tmp_d = [x for x in set(tmp) if tmp.count(x) > 1]
            tmp_d.sort()
            tmp_d.reverse()
            cards_tmp = list(set(tmp))
            for val in tmp_d:
                cards_tmp.remove(val)
            cards_tmp.sort()
            cards_tmp.reverse()
            tmp_d.extend(cards_tmp)
            return tmp_d
        elif handval == 1:
            tmp_d = [x for x in set(tmp) if tmp.count(x) > 1]
            cards_tmp = list(set(tmp))
            cards_tmp.remove(tmp_d[0])
            cards_tmp.sort()
            cards_tmp.reverse()
            tmp_d.extend(cards_tmp)
            return tmp_d
        else:
            return tmp


    def compare_strength(self,handval1,handval2):
        for i in range(len(handval1)):
            if handval1[i] > handval2[i]:
                return 0
            elif handval1[i] < handval2[i]:
                return 1
        return 2

    
    def select_cards(self,cards):
        return  list(itertools.combinations(cards,5))

    def strength_hand(self,cardsarray):
        maxhandval = 0
        maxhandlist=[]
        for cards in cardsarray:
            handval = self.determine_hand(cards)
            if(maxhandval < handval):
                maxhandval = handval
                maxhandlist = []
                maxhandlist.append(cards)
            elif(maxhandval == handval):
                maxhandlist.append(cards)
        kickerlist=[]
        for val in maxhandlist:
            kickerlist.append(self.output_kicker(val,maxhandval))
        maxtmp = []
        memkicklist = [] 
        for i in range(len(kickerlist)):
            memkicklist.append(True)
        for num in range(len(kickerlist[0])):
            maxnum=0
            for i,val in enumerate(kickerlist):
                if memkicklist[i] and maxnum < val[num]:
                    maxnum = val[num]
            for i,val in enumerate(kickerlist):
                if memkicklist[i] and val[num] < maxnum:
                    memkicklist[i] = False
        maxtmp = memkicklist.index(True)
        return maxhandval,maxhandlist[maxtmp]
 
    

if __name__ == '__main__':
    hoge = PokerCard()
    print("debug handdicison")
    tmp = []
    card = [] 
    print("あなたのハンドを入力してください")
    playdata = []
    while(len(playdata) != 2):
        playdata = input().split()
    
    for val in playdata:
        hoge.set_playercardlist(hoge.convert_cardinfo(val))
        
    print("コミュニティカードを入力してください")
    while(len(playdata) != 5):
        playdata = input().split()
    for val in playdata:
        hoge.set_communitycardlist(hoge.convert_cardinfo(val))

    print(hoge.get_communitycardlist())
    print(hoge.get_playercardlist())
    print("------------")
    phand,phandval,pkicker = hoge.get_playerhand()
    tmpcard = hoge.put_2cardlist()
    wincnt = 0
    losecnt = 0
    samecnt = 0
    print("あなたの役")
    print(phand)
    print(hoge.show_handname(phandval))

    pbar = tqdm(total = 990)
    for val in tmpcard: 
        ehand,ehandval,ekicker = hoge.get_hand(val)
        if phandval > ehandval:
            wincnt += 1
        elif phandval < ehandval:
            losecnt += 1
        else:
            st = hoge.compare_strength(pkicker,ekicker)
            if st == 0:
                wincnt += 1
            elif st == 1:
                losecnt += 1
            else:
                samecnt += 1
        pbar.update(1)
    pbar.close()
    
    # print((wincnt,losecnt,samecnt))
    print("勝率")
    print(wincnt/(wincnt+losecnt+samecnt)*100)
    

