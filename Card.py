

class Card:
    __value = 0
    __rank = 0
    __suit = ''
    __display = ''

    def __init__(self, v, r, s):
        self.setValue(v)
        self.setRank(r)
        self.setSuit(s)
        self.setDisplay()

    def setValue(self, v):
        if v > 0:
            self.__value = v

    def setRank(self, r):
        if r > 0:
            self.__rank = r

    def setSuit(self, s):
        if s == "Spades" or s == "Hearts" or s == "Clubs" or s == "Diamonds":
            self.__suit = s

    def setDisplay(self):
        if self.__rank == 13:
            string_rank = "K"
        elif self.__rank == 12:
            string_rank = "Q"
        elif self.__rank == 11:
            string_rank = "J"
        elif self.__rank == 1:
            string_rank = "A"
        else:
            string_rank = str(self.__rank)
        suit_char = self.__suit[0]
        self.__display = string_rank + suit_char

    def getValue(self):
        return self.__value

    def getRank(self):
        return self.__rank

    def getSuit(self):
        return self.__suit

    def getDisplay(self):
        return self.__display

    def __str__(self):
        self.setDisplay()
        print(self.__display)
