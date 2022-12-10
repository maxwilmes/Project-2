

class Hand:
    __hand = []

    def __init__(self, *args):
        if len(args) > 1:
            if isinstance(args[1],int):
                self.__hand = args[0][args[1]]
            elif isinstance(args[1],list):
                self.__hand = args[0] + args[1]

    def __str__(self):
        for i in range(len(self.__hand)):
            self.__hand[i].__str__()

    def __getitem__(self, i):
        if i < len(self.__hand):
            card = self.__hand[i]
            return card

    def pop(self, i):
        if i < len(self.__hand):
            card = self.__hand[i]
            del(self.__hand[i])
            return card

    def __setitem__(self, key, value):
        if key < len(self.__hand):
            self.__hand[key] = value

    def __len__(self):
        return len(self.__hand)

    def discard(self, i, n):
        crib = []
        if i < len(self.__hand) and n < len(self.__hand) and i != n:
            if i > n:
                crib = [self.__hand.pop(i), self.__hand.pop(n)]
            elif i < n:
                crib = [self.__hand.pop(n), self.__hand.pop(i)]
            return crib
