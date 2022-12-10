from CribbageGame.Card import *
import random


class Deck:
    __deck = []
    __suit = ["Hearts", 'Diamonds', 'Spades', 'Clubs']

    def __init__(self):
        self.__deck = []
        for j in range(4):
            for i in range(13):
                r = i + 1
                self.__deck.append(Card(r if r < 10 else 10, r, self.__suit[j]))

    def __str__(self):
        for i in range(len(self.__deck)):
            self.__deck[i].__str__()

    def shuffle(self):
        for i in range(len(self.__deck)):
            shuffler = random.randint(0, len(self.__deck)-1)
            temp = self.__deck[shuffler]
            self.__deck[shuffler] = self.__deck[i]
            self.__deck[i] = temp

    def cut(self, cut):
        if (cut - 1 <= len(self.__deck)) and (cut - 1 >= 0):
            cut_card = self.__deck[cut]
            del(self.__deck[cut])
            return cut_card

    def deal(self):
        hand1 = []
        hand2 = []
        for i in range(6):
            hand1.append(self.__deck.pop(0))
            hand2.append(self.__deck.pop(0))
        hands = [hand1, hand2]
        return hands

    def __getitem__(self, i):
        if i < len(self.__deck):
            return self.__deck[i]

    def get_length(self):
        return len(self.__deck)
