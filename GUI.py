import copy
from tkinter import *
from CribbageGame.Hand import *
from CribbageGame.Deck import *
from CribbageGame.Scoring import *
from CribbageGame.AI import *
from PIL import Image, ImageTk
import time


class GUI:
    def __init__(self, window):
        self.window = window
        self.dealer = 0
        self.play_total = IntVar()
        self.play_total.set(0)
        self.user_score = IntVar()
        self.user_score.set(0)
        self.com_score = IntVar()
        self.cut_status = True
        self.wait = IntVar()
        self.cut_num = IntVar()
        self.cut_num.set(0)
        self.discard_place = True
        self.cut_card = 0
        self.card_to_play = 0
        self.cards = {}
        self.card_frames = {}
        self.hand = {}
        self.hand_display = {}
        self.com_cards = {}
        self.com_cards_frames = {}
        self.card_image = {}
        self.discard_cards = [-1, -1]
        self.deck = Deck()
        self.user_card_to_play = Card(1,1,"Hearts")
        self.scorer = Scoring()
        self.hands = self.deck.deal()
        self.hand0 = Hand(self.hands, 0)
        self.hand1 = Hand(self.hands, 1)
        self.crib = Hand(self.hands, 0)

        self.user_score_frame = Frame(self.window, bg='green')
        self.user_score_label_1 = Label(self.user_score_frame, text=f'USER: ', bg='green', fg='white', font=40)
        self.user_score_label_2 = Label(self.user_score_frame, textvariable= self.user_score, bg='green', fg='white', font=40)
        self.user_score_label_1.pack(padx=5,pady=2,side='left')
        self.user_score_label_2.pack(padx=5, pady=2, side='right')
        self.user_score_frame.pack(anchor='nw')

        self.com_score_frame = Frame(self.window, bg='green')
        self.com_score_label_1 = Label(self.com_score_frame, text=f'COM: ', bg='green', fg='white', font=40)
        self.com_score_label_2 = Label(self.com_score_frame, textvariable=self.com_score, bg='green', fg='white', font=40)
        self.com_score_label_1.pack(padx=5, pady=2, side='left')
        self.com_score_label_2.pack(padx=5, pady=2, side='right')
        self.com_score_frame.pack(anchor='nw')

        self.start_frame = Frame(self.window)
        self.start_label = Label(self.start_frame, text='Welcome to Cribbage!', font=12)
        self.start_button = Button(self.start_frame, text='Start Game', font=100, command=lambda: self.gameplay())
        self.start_label.pack(side='top', pady=5)
        self.start_button.pack(side='bottom', pady=5)
        self.start_frame.pack(anchor='center')

        self.ready_frame = Frame(self.window)
        self.ready_button = Button(self.ready_frame, text= 'Cut', font=100, command=lambda: self.wait.set(0))
        self.ready_button.pack()

        self.select_card_frame = Frame(self.window)
        self.select_card_label = Label(self.select_card_frame, text='Select Card Then Select Cut', font=100)
        self.cut_won_frame = Frame(self.window)
        self.cut_won_label = Label(self.cut_won_frame, text="Cut Won!\nYour Crib", font=100)
        self.cut_lost_frame = Frame(self.window)
        self.cut_lost_label = Label(self.cut_lost_frame, text="Cut Lost!\nOpponent's Crib", font=100)
        self.cut_tie_frame = Frame(self.window)
        self.cut_tie_label = Label(self.cut_tie_frame, text= "It's a Tie!\nCut Again!", font=100)


        self.select_discard_frame = Frame(self.window)
        self.select_discard_label = Label(self.select_discard_frame, text='Your Hand:\nSelect 2 Cards to Discard',
                                          font=100)
        self.select_discard_button = Button(self.select_discard_frame, text='Discard', font=100,
                                            command=lambda:(self.gui_discard(self.discard_cards), self.wait.set(1)))

        self.play_total_frame = Frame(self.window)
        self.play_total_label_1 = Label(self.play_total_frame, text='Total:', bg='green', fg='white', font=100)
        self.play_total_label_2 = Label(self.play_total_frame, textvariable=self.play_total, bg='green', fg='white', font=100)
        self.play_total_label_1.pack(side='left')
        self.play_total_label_2.pack(side='right')

        self.go_frame = Frame(self.window)
        self.go_button = Button(self.go_frame, text= 'Go',font=100, command=lambda: self.wait.set(0))
        self.user_go_label = Label(self.go_frame, text='You Must Say Go', font = 100)
        self.com_go_label = Label(self.go_frame, text= 'Opponent Says Go', font=100)
        self.too_high_label = Label(self.go_frame, text='Total Exceeds 31\nSelect a Different Card', font= 100)

        self.fifteen_frame = Frame(self.window)
        self.fifteen_label = Label(self.fifteen_frame, text='15!\nPlus 2 Points', font=100)
        self.fifteen_label.pack()

        self.pair_frame = Frame(self.window)
        self.pair_label = Label(self.pair_frame, text='Pair!\nPlus 2 Points', font=100)
        self.pair_label.pack()

        self.three_pair_frame = Frame(self.window)
        self.three_pair_label = Label(self.three_pair_frame, text='Three of a Kind!\nPlus 6 Points', font=100)
        self.three_pair_label.pack()

        self.four_pair_frame = Frame(self.window)
        self.four_pair_label = Label(self.four_pair_frame, text='Three of a Kind!\nPlus 6 Points', font=100)
        self.four_pair_label.pack()

        self.thirty_one_frame = Frame(self.window)
        self.thirty_one_label = Label(self.thirty_one_frame, text='31!\nPlus 2 Points', font=100)
        self.thirty_one_label.pack()

        self.nibs_frame = Frame(self.window)
        self.nibs_label = Label(self.nibs_frame, text='Nibs!\nPlus 2 Points', font=100)
        self.nibs_label.pack()

    def start_cut(self):
        global cut_image
        cut_image = self.resize_card('cards/back_of_card.png')
        self.select_card_label.pack()
        self.select_card_frame.place(x=450, y=50)
        for i in range(52):
            self.card_frames[i] = Frame(self.window)
            self.cards[i] = Button(self.card_frames[i], image=cut_image, command=lambda: self.cut_num.set(20))
            self.cards[i].pack(side='left')
            self.card_frames[i].place(x=i*20, y=100)
        self.ready_frame.place(x=700, y=500)
        self.ready_button.wait_variable(self.wait)
        self.cut_card = self.cut_num.get()
        self.select_card_frame.place_forget()
        self.ready_frame.place_forget()
        for k in range(52):
            self.card_frames[k].place_forget()
        cut0 = self.deck.cut(self.cut_card)
        cut1 = self.deck.cut(random.randint(0, 49))
        if cut0.getRank() == cut1.getRank():
            self.cut_tie_label.pack()
            self.cut_tie_frame.pack(anchor='center')
            self.window.update()
            time.sleep(1)
            self.cut_tie_frame.pack_forget()
            self.start_cut()
        if cut0.getRank() > cut1.getRank():
            self.dealer = 1
            self.cut_won_label.pack()
            self.cut_won_frame.pack(anchor='center')
            self.cut_status = True
        if cut0.getRank() < cut1.getRank():
            self.dealer = 2
            self.cut_lost_label.pack()
            self.cut_lost_frame.pack(anchor='center')
            self.cut_status = False
        self.window.update()
        time.sleep(1)
        self.cut_lost_frame.pack_forget()
        self.cut_won_frame.pack_forget()

    def play_cut(self):
        global play_cut_image
        for i in range(52):
            self.card_frames[i].place(x=i*20, y=100)
        self.ready_frame.place(x=300, y=520)
        self.ready_button.wait_variable(self.wait)
        self.ready_frame.place_forget()
        self.cut_card = self.cut_num.get()
        for k in range(52):
            self.card_frames[k].place_forget()
        play_cut_image = self.resize_card(f'cards/{self.deck.__getitem__(self.cut_card).getDisplay()}.png')
        if self.deck.__getitem__(self.cut_card).getRank() == 11:
            self.nibs_frame.place(x=650, y=320)
            self.window.update()
            time.sleep(1)
            self.nibs_frame.place_forget()
        self.turn_card = self.deck.__getitem__(self.cut_card)
        self.cut_card_frame = Frame(self.window)
        self.cut_card_label = Label(self.cut_card_frame, image=play_cut_image)
        self.cut_card_label_1 = Label(self.cut_card_frame, text='Cut Card', font= 120)
        self.cut_card_label_1.pack(side='top')
        self.cut_card_label.pack(side='bottom')
        self.cut_card_frame.place(x=200, y=270)

    def display_hand(self, hand):
        global card_images
        card_images = {}
        for k in range(len(hand)):
            self.hand_display[k] = hand.__getitem__(k).getDisplay()
            self.card = self.hand_display[k]
            card_images[k] = self.resize_card(f"cards/{self.card}.png")

        self.hand_card_frame_1 = Frame(self.window, background='green')
        self.hand_card_label_1 = Button(self.hand_card_frame_1, image=card_images[0], bg='green',
                                        command=lambda: self.discard_toggle(0))
        self.hand_card_frame_2 = Frame(self.window, background='green')
        self.hand_card_label_2 = Button(self.hand_card_frame_2, image=card_images[1], bg='green',
                                        command=lambda: self.discard_toggle(1))
        self.hand_card_frame_3 = Frame(self.window, background='green')
        self.hand_card_label_3 = Button(self.hand_card_frame_3, image=card_images[2], bg='green',
                                        command=lambda: self.discard_toggle(2))
        self.hand_card_frame_4 = Frame(self.window, background='green')
        self.hand_card_label_4 = Button(self.hand_card_frame_4, image=card_images[3], bg='green',
                                        command=lambda: self.discard_toggle(3))
        self.hand_card_frame_5 = Frame(self.window, background='green')
        self.hand_card_label_5 = Button(self.hand_card_frame_5, image=card_images[4], bg='green',
                                        command=lambda: self.discard_toggle(4))
        self.hand_card_frame_6 = Frame(self.window, background='green')
        self.hand_card_label_6 = Button(self.hand_card_frame_6, image=card_images[5], bg='green',
                                        command=lambda: self.discard_toggle(5))
        self.select_discard_label.pack(side='top')
        self.select_discard_button.pack(side='bottom')
        self.select_discard_frame.pack(anchor='s')
        self.hand_card_label_1.pack(side='left')
        self.hand_card_frame_1.place(x=450, y=500)
        self.hand_card_label_2.pack(side='left')
        self.hand_card_frame_2.place(x=530, y=500)
        self.hand_card_label_3.pack(side='left')
        self.hand_card_frame_3.place(x=610, y=500)
        self.hand_card_label_4.pack(side='left')
        self.hand_card_frame_4.place(x=690, y=500)
        self.hand_card_label_5.pack(side='left')
        self.hand_card_frame_5.place(x=770, y=500)
        self.hand_card_label_6.pack(side='left')
        self.hand_card_frame_6.place(x=850, y=500)

    def display_play_hand(self, hand):
        for k in range(len(hand)):
            self.hand_display[k] = hand.__getitem__(k).getDisplay()
            self.card = self.hand_display[k]
            card_images[k] = self.resize_card(f"cards/{self.card}.png")

        self.hand_card_play_frame_1 = Frame(self.window, background='green')
        self.hand_card_play_label_1 = Button(self.hand_card_play_frame_1, image=card_images[0], bg='green',
                                        command=lambda: (self.get_card_to_play(0), self.wait.set(0)))
        self.hand_card_play_frame_2 = Frame(self.window, background='green')
        self.hand_card_play_label_2 = Button(self.hand_card_play_frame_2, image=card_images[1], bg='green',
                                        command=lambda: (self.get_card_to_play(1), self.wait.set(0)))
        self.hand_card_play_frame_3 = Frame(self.window, background='green')
        self.hand_card_play_label_3 = Button(self.hand_card_play_frame_3, image=card_images[2], bg='green',
                                        command=lambda: (self.get_card_to_play(2), self.wait.set(0)))
        self.hand_card_play_frame_4 = Frame(self.window, background='green')
        self.hand_card_play_label_4 = Button(self.hand_card_play_frame_4, image=card_images[3], bg='green',
                                        command=lambda: (self.get_card_to_play(3), self.wait.set(0)))
        self.hand_card_play_label_1.pack(side='left')
        self.hand_card_play_frame_1.place(x=450, y=500)
        self.hand_card_play_label_2.pack(side='left')
        self.hand_card_play_frame_2.place(x=530, y=500)
        self.hand_card_play_label_3.pack(side='left')
        self.hand_card_play_frame_3.place(x=610, y=500)
        self.hand_card_play_label_4.pack(side='left')
        self.hand_card_play_frame_4.place(x=690, y=500)

    def gui_discard(self, card):
        discard = AI.ai_discard(self.hand1)
        self.crib = Hand(self.hand0.discard(card[0], card[1]), self.hand1.discard(discard[0], discard[1]))
        self.hand_card_frame_1.place_forget()
        self.hand_card_frame_2.place_forget()
        self.hand_card_frame_3.place_forget()
        self.hand_card_frame_4.place_forget()
        self.hand_card_frame_5.place_forget()
        self.hand_card_frame_6.place_forget()
        self.select_discard_frame.pack_forget()
        self.display_play_hand(self.hand0)

    def discard_toggle(self, place):
        if self.discard_place == True:
            self.discard_cards[0] = place
            self.discard_place = False
            return
        if self.discard_place == False:
            self.discard_cards[1] = place
            self.discard_place = True
            return

    def get_card_to_play(self, num):
        self.card_to_play = num

    def the_play(self, user_hand, com_hand):
        temp_total = self.play_total.get()
        values = []
        ranks = []
        go = 0
        go_occurred = False
        last_card_played = 0
        last_played = True
        card_played = 0
        pair_count = 1
        x1 = 0
        x2 = 0
        j = 0
        self.play_total_frame.place(x=900, y=320)
        user_hand_copy = copy.deepcopy(user_hand)
        self.window.update()
        while len(user_hand) > 0 or len(com_hand) > 0:
            if len(com_hand) > 0:
                for k in range(len(com_hand)):
                    self.card_to_play = k
                    card_played = com_hand.__getitem__(self.card_to_play)
                    temp_total = self.play_total.get()
                    temp_total += card_played.getValue()
                    if temp_total <= 31:
                        break
                if temp_total > 31:
                    self.cut_status = False
                    go += 1
                    go_occurred = True
                    if go == 2:
                        self.com_score.set(self.com_score.get() + 1)
                        go = 0
                        self.play_total.set(0)
                        values = []
                        ranks = []
                    else:
                        self.too_high_label.pack_forget()
                        self.go_button.pack_forget()
                        self.com_go_label.pack()
                        self.user_go_label.pack_forget()
                        self.go_frame.place(x=650, y=320)
                        self.window.update()
                        time.sleep(1)
                        self.com_go_label.pack_forget()
                elif temp_total == 31:
                    self.com_score.set(self.com_score.get() + 2)
                    go_occurred = False
                    self.thirty_one_frame.place(x=650, y=320)
                    self.window.update()
                    time.sleep(1)
                    self.thirty_one_frame.place_forget()
                if go_occurred == False:
                    if go == 1:
                        go = 0
                    if self.cut_status:
                        self.play_total.set(temp_total)
                        values.append(card_played.getValue())
                        ranks.append(card_played.getRank())
                        self.card_image[j] = self.resize_card(f'cards/{card_played.getDisplay()}.png')
                        self.com_cards_frames[j] = Frame(self.window)
                        self.com_cards[j] = Label(self.com_cards_frames[j], image=self.card_image[j])
                        self.com_cards[j].pack()
                        self.com_cards_frames[j].place(x=1000+x1, y=80)
                        if self.play_total.get() == 31:
                            self.play_total.set(0)
                            values = []
                            ranks = []
                        if self.play_total.get() == 15:
                            self.com_score.set(self.com_score.get() + 2)
                            self.fifteen_frame.place(x=650, y=320)
                            self.window.update()
                            time.sleep(1)
                            self.fifteen_frame.place_forget()
                        self.com_score.set(self.com_score.get() + Scoring.play_runs(ranks))
                        Scoring.play_runs(ranks)
                        if last_card_played == card_played.getRank():
                            self.com_score.set(self.com_score.get() + 2)
                            pair_count += 1
                            if pair_count ==2:
                                self.pair_frame.place(x=650, y=320)
                                self.window.update()
                                time.sleep(1)
                                self.pair_frame.place_forget()
                            if pair_count == 3:
                                self.com_score.set(self.com_score.get() + 4)
                                self.three_pair_frame.place(x=650, y=320)
                                self.window.update()
                                time.sleep(1)
                                self.three_pair_frame.place_forget()
                            if pair_count == 4:
                                self.com_score.set(self.com_score.get() + 6)
                                self.four_pair_frame.place(x=650, y=320)
                                self.window.update()
                                time.sleep(1)
                                self.four_pair_frame.place_forget()
                        else:
                            pair_count = 1
                        j += 1
                        x1 += 40
                        if x1 > 120:
                            x1 = 0
                        com_hand.pop(self.card_to_play)
                        self.cut_status = False
                        last_played = False
                        last_card_played = card_played.getRank()
                else:
                    go_occurred = False
                    self.cut_status = False
            if len(user_hand) > 0:
                if self.cut_status == False:
                    self.window.update()
                    for m in range(len(user_hand)):
                        card_played = user_hand.__getitem__(m)
                        temp_total = self.play_total.get()
                        temp_total += card_played.getValue()
                        if temp_total <= 31:
                            break
                    if temp_total > 31:
                        self.user_go_label.pack()
                        self.go_button.pack()
                        self.go_frame.place(x=650, y=320)
                        self.go_button.wait_variable(self.wait)
                        self.go_frame.place_forget()
                        go += 1
                        go_occurred = True
                        if go == 2:
                            self.user_score.set(self.user_score.get() + 1)
                            go = 0
                            self.play_total.set(0)
                            values = []
                            ranks = []
                    #exec(f'self.hand_card_play_frame_{self.card_to_play + 1}.wait_variable(self.wait)')
                    if go_occurred == False:
                        if go == 1:
                            go = 0
                        exec(f'self.hand_card_play_frame_{self.card_to_play + 1}.wait_variable(self.wait)')
                        while user_hand_copy[self.card_to_play].getValue() + self.play_total.get() > 31:
                            self.too_high_label.pack()
                            self.go_button.pack_forget()
                            self.com_go_label.pack_forget()
                            self.user_go_label.pack_forget()
                            self.go_frame.place(x=650, y=320)
                            self.window.update()
                            time.sleep(1)
                            self.too_high_label.pack_forget()
                            exec(f'self.hand_card_play_frame_{self.card_to_play + 1}.wait_variable(self.wait)')
                        exec(f'self.hand_card_play_frame_{self.card_to_play + 1}.place(x=1000+x2, y=350)')
                        exec(f'self.hand_card_play_frame_{self.card_to_play + 1}.tkraise()')
                        x2 += 40
                        if x2 > 120:
                            x2 = 0
                        for i in range(len(user_hand)):
                            if user_hand_copy[self.card_to_play].getDisplay() == user_hand[i].getDisplay():
                                card_played = user_hand.__getitem__(i)
                                self.play_total.set(self.play_total.get() + card_played.getValue())
                                values.append(card_played.getValue())
                                ranks.append(card_played.getRank())
                                user_hand.pop(i)
                                break
                        if self.play_total.get() == 31:
                            self.user_score.set(self.user_score.get() + 2)
                            self.play_total.set(0)
                            values = []
                            ranks = []
                            self.thirty_one_frame.place(x=650, y=320)
                            self.window.update()
                            time.sleep(1)
                            self.thirty_one_frame.place_forget()
                        if self.play_total.get() == 15:
                            self.user_score.set(self.user_score.get() + 2)
                            self.fifteen_frame.place(x=650, y=320)
                            self.window.update()
                            time.sleep(1)
                            self.fifteen_frame.place_forget()
                        self.user_score.set(self.user_score.get() + Scoring.play_runs(ranks))
                        if last_card_played == card_played.getRank():
                            self.user_score.set(self.user_score.get() + 2)
                            pair_count += 1
                            if pair_count == 2:
                                self.pair_frame.place(x=650, y=320)
                                self.window.update()
                                time.sleep(1)
                                self.pair_frame.place_forget()
                            if pair_count == 3:
                                self.user_score.set(self.user_score.get() + 4)
                                self.three_pair_frame.place(x=650, y=320)
                                self.window.update()
                                time.sleep(1)
                                self.three_pair_frame.place_forget()
                            if pair_count == 4:
                                self.user_score.set(self.user_score.get() + 6)
                                self.four_pair_frame.place(x=650, y=320)
                                self.window.update()
                                time.sleep(1)
                                self.four_pair_frame.place_forget()
                        else:
                            pair_count = 1
                        self.cut_status = True
                        last_played = True
                        last_card_played = card_played.getRank()
                    else:
                        go_occurred = False
                        self.cut_status = True
                else:
                    self.cut_status = False
            else:
                go_occurred = True
                self.play_total.set(0)
                self.user_score.set(self.user_score.get() + 1)
        if last_played == True:
            self.user_score.set(self.user_score.get() + 1)
        if last_played == False:
            self.com_score.set(self.com_score.get() + 1)

    def the_show(self, user_hand, com_hand, turn_card):
        user_hand_copy = copy.deepcopy(user_hand)
        com_hand_copy = copy.deepcopy(com_hand)
        turn_card_copy = copy.deepcopy(turn_card)
        self.display_play_hand(user_hand)
        for j in range(len(com_hand)):
            self.com_cards_frames[j].place(x=450 + 80 * j, y=40)
        user_hand_score = IntVar()
        com_hand_score = IntVar()
        crib_score = IntVar()
        user_hand_score.set(self.scorer.score_hand(user_hand_copy, turn_card_copy))
        com_hand_score.set(self.scorer.score_hand(com_hand_copy, turn_card_copy))
        crib_score.set(self.scorer.score_hand(self.crib, turn_card_copy))
        if self.dealer == 2:
            self.user_score_frame = Frame(self.window)
            self.user_score_label = Label(self.user_score_frame, text="Your Score:", font=200)
            self.user_score_label_1 = Label(self.user_score_frame, textvariable=user_hand_score, font=200)
            self.user_score_label_1.pack(side='bottom')
            self.user_score_label.pack(side='top')
            self.user_score_frame.place(x=500, y=450)
            self.user_score.set(self.user_score.get() + user_hand_score.get())
            if self.user_score.get() >= 121:
                return

            self.com_score_frame = Frame(self.window)
            self.com_score_label = Label(self.com_score_frame, text="Opponent's Score:", font=200)
            self.com_score_label_1 = Label(self.com_score_frame, textvariable=com_hand_score, font=200)
            self.com_score_label_1.pack(side='bottom')
            self.com_score_label.pack(side='top')
            self.com_score_frame.place(x=500, y=300)
            self.com_score.set(self.com_score.get() + com_hand_score.get() + crib_score.get())

            if self.com_score.get() >= 121:
                return
        elif self.dealer == 1:
            self.com_score_frame = Frame(self.window)
            self.com_score_label = Label(self.com_score_frame, text="Your Score:", font=200)
            self.com_score_label_1 = Label(self.com_score_frame, textvariable=com_hand_score, font=200)
            self.com_score_label_1.pack(side='bottom')
            self.com_score_label.pack(side='top')
            self.com_score_frame.place(x=500, y=300)
            self.com_score.set(self.com_score.get() + com_hand_score.get())
            if self.com_score.get() >= 121:
                return

            self.user_score_frame = Frame(self.window)
            self.user_score_label = Label(self.user_score_frame, text="Your Score:", font=200)
            self.user_score_label_1 = Label(self.user_score_frame, textvariable=user_hand_score, font=200)
            self.user_score_label_1.pack(side='bottom')
            self.user_score_label.pack(side='top')
            self.user_score_frame.place(x=500, y=450)
            self.user_score.set(self.user_score.get() + user_hand_score.get() + crib_score.get())
            if self.user_score.get() >= 121:
                return

    def resize_card(self, card):
        card_img = Image.open(card)
        card_img_resize = card_img.resize((150, 218))
        global final_img
        final_img = ImageTk.PhotoImage(card_img_resize)
        return final_img

    def gameplay(self):
        self.start_frame.pack_forget()
        self.user_score.set(0)
        self.com_score.set(0)
        while self.user_score.get() < 121 and self.com_score.get() < 121:
            if self.dealer == 0:
                self.deck = Deck()
                self.deck.shuffle()
                self.start_cut()
            self.deck = Deck()
            self.deck.shuffle()
            self.hands = self.deck.deal()
            if self.dealer == 1:
                self.hand0 = Hand(self.hands, 0)
                self.hand1 = Hand(self.hands, 1)
            elif self.dealer == 2:
                self.hand0 = Hand(self.hands, 1)
                self.hand1 = Hand(self.hands, 0)
            self.display_hand(self.hand0)
            self.select_discard_button.wait_variable(self.wait)
            self.play_cut()
            hand0_play = copy.deepcopy(self.hand0)
            hand1_play = copy.deepcopy(self.hand1)
            self.the_play(hand0_play, hand1_play)
            self.window.update()
            self.the_show(self.hand0, self.hand1, self.turn_card)
            self.window.update()
            time.sleep(3)
            self.user_score_frame.place_forget()
            self.com_score_frame.place_forget()
            self.keep_playing_frame = Frame(self.window)
            self.keep_playing_button = Button(self.keep_playing_frame, text="Continue", font= 200, command=lambda: self.wait.set(0))
            self.keep_playing_button.pack()
            self.keep_playing_frame.place(x=450, y=300)
            self.keep_playing_button.wait_variable(self.wait)
            for j in range(4):
                self.com_cards_frames[j].place_forget()
            self.hand_card_play_frame_1.place_forget()
            self.hand_card_play_frame_2.place_forget()
            self.hand_card_play_frame_3.place_forget()
            self.hand_card_play_frame_4.place_forget()
            self.keep_playing_frame.place_forget()
            self.cut_card_frame.place_forget()






