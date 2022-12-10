from CribbageGame.Scoring import *
from CribbageGame.Hand import *
import copy


class AI:

    @staticmethod
    def ai_discard(hand):
        discard = [0, 0]
        scorer = Scoring()
        score = 0
        top_score = 0
        for i in range(5):
            for j in range(i + 1, 6):
                test_hand = copy.deepcopy(hand)
                test_hand.discard(i, j)
                score = scorer.score_hand(test_hand)
                if score > top_score:
                    top_score = score
                    discard[0] = i
                    discard[1] = j
        return discard
