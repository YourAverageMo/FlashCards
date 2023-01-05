from random import randint
from tkinter import *

import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"

current_card = {}
# ---------------------------- WORD HANDLING ------------------------------- #


def gen_new_words_dict():
    words = pandas.read_csv("./data/french_words.csv")
    return pandas.DataFrame.to_dict(words, orient="records")

def get_words_to_learn():
    words = pandas.read_csv("./data/words_to_learn.csv",)
    return pandas.DataFrame.to_dict(words, orient="records")


def is_known():
    words_to_learn.remove(current_card)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("./data/words_to_learn.csv", index=False)
    gen_new_words()

def gen_new_words():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    random_list_index = randint(0, len(words_to_learn) - 1)
    current_card = words_to_learn[random_list_index]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(
        card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(bg, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(bg, image=card_back_img)


# ---------------------------- UI SETUP ------------------------------- #
try:
    words_to_learn = get_words_to_learn()
    print("using old words to learn list")
except FileNotFoundError:
    words_to_learn = gen_new_words_dict()
    print("generating new words list")

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
wrong_img = PhotoImage(file="./images/wrong.png")
right_img = PhotoImage(file="./images/right.png")

canvas = Canvas(width=800, height=520,
                highlightthickness=0, bg=BACKGROUND_COLOR)
bg = canvas.create_image(400, 260, image=card_front_img)

card_title = canvas.create_text(
    400, 150, text="Title", font=(FONT_NAME, 40, "italic"), fill="black"
)
card_word = canvas.create_text(
    400, 263, text="Word", font=(FONT_NAME, 60, "bold"), fill="black"
)
canvas.grid(column=0, row=0, columnspan=2)

wrong_button = Button(
    image=wrong_img, command=gen_new_words, highlightthickness=0)
wrong_button.grid(column=0, row=1)

right_button = Button(
    image=right_img, command=is_known, highlightthickness=0)
right_button.grid(column=1, row=1)

gen_new_words()

window.mainloop()
