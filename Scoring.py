import copy


class Scoring:

    def score_hand(self, *args):
        score = 0
        hand_values = []
        hand_ranks = []
        hand_suits = []
        if len(args) == 2:
            for i in range(len(args[0])):
                hand_values.append(args[0][i].getValue())
                hand_ranks.append(args[0][i].getRank())
                hand_suits.append(args[0][i].getSuit())
            hand_values.append(args[1].getValue())
            hand_ranks.append(args[1].getRank())
            hand_suits.append(args[1].getSuit())
            score += self.pairs(hand_ranks)
            score += self.flush(hand_suits, args[1])
            score += self.nobs(hand_ranks, hand_suits, args[1])
            score += self.fifteens(hand_values)
            score += self.runs(hand_ranks)
            return score
        elif len(args) == 1:
            for i in range(len(args[0])):
                hand_values.append(args[0][i].getValue())
                hand_ranks.append(args[0][i].getRank())
                hand_suits.append(args[0][i].getSuit())
            score += self.pairs(hand_ranks)
            score += self.flush(hand_suits)
            score += self.fifteens(hand_values)
            score += self.runs(hand_ranks)
            return score

    @staticmethod
    def fifteens(values):
        score = 0
        count = 0
        values.sort()
        if values[0] < 8:
            for i in range(len(values)):
                count += values[i]
            if count == 15:
                score += 2
            if count > 15:
                for n in range(len(values)):
                    for i in range(n + 1, len(values)):
                        count = 0
                        count = values[n] + values[i]
                        if count == 15:
                            score += 2
                    for j in range(n + 1, len(values)):
                        for k in range(j + 1, len(values)):
                            count = 0
                            count = values[n] + values[j] + values[k]
                            if count == 15:
                                score += 2
                    count = 0
                    for m in range(len(values)):
                        count += values[m]
                    if count == 15:
                        score += 2
        return score

    @staticmethod
    def runs(hand_ranks):
        score = 0
        multiplier = 1
        count = 1
        ranks = copy.deepcopy(hand_ranks)
        run = []
        new_run = []
        pairs = []
        ranks.sort()
        for k in range(1, len(ranks)):
            if ranks[0] + k == ranks[k]:
                count += 1
            else:
                count = 1
                break
        if count == 5:
            score = count
            return score
        for i in range(len(ranks) - 1):
            if ranks[i] != ranks[i + 1]:
                run.append(ranks[i])
        run.append(ranks[len(ranks) - 1])
        if len(run) < 3:
            score = 0
            return score
        for j in range(len(run)):
            for n in range(j + 1, len(run)):
                if run[j] + n - j == run[n]:
                    count = n + 1 - j
            if count > 2:
                new_run.append(run[j])
                new_run.append(run[j+1])
                new_run.append(run[j+2])
                if count == 4:
                    new_run.append(run[j+3])
                break
        for k in range(len(new_run)):
            for x in range(len(ranks) - 1):
                if new_run[k] == ranks[x] and new_run[k] == ranks[x + 1]:
                    multiplier += 1
                    pairs.append(new_run[k])
        if len(pairs) == 2:
            if pairs[0] != pairs[1]:
                multiplier += 1
        if count > 2:
            score = count * multiplier
        return score

    @staticmethod
    def play_runs(hand_ranks):
        score = 0
        count = 1
        ranks = copy.deepcopy(hand_ranks)
        run = []
        if len(ranks) < 3:
            return score
        else:
            run.append(ranks[len(ranks)-1])
            run.append(ranks[len(ranks)-2])
            run.append(ranks[len(ranks)-3])
            score = Scoring.runs(run)
            length = len(hand_ranks) - len(run)
            while length > 0 and score >= 3:
                run_max = max(run)
                run_min = min(run)
                if hand_ranks[len(hand_ranks) - 3 - count] == run_max + 1 or \
                        hand_ranks[len(hand_ranks) - 3 - count] == run_min - 1:
                    score += 1
                    count += 1
                    length -= 1
                else:
                    break
            while length > 0 and score == 0:
                run.append(hand_ranks[len(hand_ranks) - 3 - count])
                if Scoring.runs(run) > score:
                    score = Scoring.runs(run)
                    count += 1
                    length -= 1
                else:
                    break
            return score



    @staticmethod
    def pairs(ranks):
        score = 0
        for i in range(len(ranks)):
            for j in range(i + 1, len(ranks)):
                if ranks[i] == ranks[j]:
                    score += 2
        return score

    @staticmethod
    def flush(*args):
        score = 0
        if len(args) == 2:
            if args[0][0] == args[0][1]:
                if args[0][1] == args[0][2]:
                    if args[0][2] == args[0][3]:
                        score = 4
                        if args[0][0] == args[1].getSuit():
                            score += 1
            return score
        if len(args) == 1:
            count = 0
            args[0].sort()
            for i in range(len(args[0])):
                for j in range(i + 1, len(args[0])):
                    if args[0][i] == args[0][j]:
                        count += 1
                    elif count > 3:
                        score = count
                        return score
                    else:
                        count = 0
        return score
    
    @staticmethod
    def nobs(ranks, suits, cut):
        score = 0
        for i in range(len(ranks)):
            if ranks[i] == 11 and suits[i] == cut.getSuit():
                score += 1
                break
        return score
