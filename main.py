from GUI import *


def main():
    window = Tk()
    window.title('Cribbage')
    window.geometry('1036x564')
    window.configure(background='green')
    window.resizable(True, True)

    widgets = GUI(window)
    window.mainloop()


if __name__ == '__main__':
    main()