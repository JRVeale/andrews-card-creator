import tkinter as tk
from tkinter import filedialog
import jsonpickle
import os
from PIL import Image, ImageTk

from plotcard import PlotCard, PlotCardOption


class CardManager:

    def __init__(self):
        # Get directory
        self.directory = tk.filedialog.askdirectory(title="Where are your cards?")

        # Get existing cards in directory
        self.card_files = []
        self.cards = []
        for file in os.listdir(self.directory):
            if file.endswith(".json"):
                # add filepath to cardfiles list
                self.card_files.append(self.directory + "/" + file)
                # decode card and add to cards list
                f = open(self.card_files[-1])
                self.cards.append(jsonpickle.decode(f.read()))
                f.close()
        print(self.card_files)
        print(self.cards)

        # Create window
        self.master = tk.Toplevel()
        self.master.title("Card Creator")

        # Create main containers
        self.graph_frame = tk.Frame(self.master, bg="green")
        self.details_frame = tk.Frame(self.master, bg="blue")
        # Layout main containers
        self.graph_frame.grid(row=0, column=1)
        self.details_frame.grid(row=0, column=0)

        # Create details containers
        self.buttons_frame = tk.Frame(self.details_frame, bg="white")
        self.fields_frame = tk.Frame(self.details_frame, bg="gray")
        self.options_frame = tk.Frame(self.details_frame, bg="gray2")
        # Layout details containers
        self.buttons_frame.grid(row=0, column=0, sticky="W")
        self.fields_frame.grid(row=1, column=0)
        self.options_frame.grid(row=2, column=0)

        # Create buttons
        self.new_button = tk.Button(self.buttons_frame, text="NEW", command=self.new_card, width=20)
        self.open_button = tk.Button(self.buttons_frame, text="OPEN", command=self.open_card, width=20)
        self.save_button = tk.Button(self.buttons_frame, text="SAVE", command=self.save_card, width=20)
        self.delete_button = tk.Button(self.buttons_frame, text="DELETE", command=self.delete_card, width=20)
        # Layout buttons
        self.new_button.grid(row=0, column=0)
        self.open_button.grid(row=0, column=1)
        self.save_button.grid(row=0, column=2)
        self.delete_button.grid(row=0, column=3)

        # Create and layout field labels
        tk.Label(self.fields_frame, text="ID").grid(row=0)
        tk.Label(self.fields_frame, text="Title").grid(row=1)
        tk.Label(self.fields_frame, text="Subtitle").grid(row=2)
        tk.Label(self.fields_frame, text="Text").grid(row=3)
        # Create fields
        self.id = tk.Entry(self.fields_frame, width=107) # TODO make id field uneditable
        self.title = tk.Entry(self.fields_frame, width=107)
        self.subtitle = tk.Entry(self.fields_frame, width=107)
        self.text = tk.Text(self.fields_frame)
        # Layout fields
        self.id.grid(row=0, column=1)
        self.title.grid(row=1, column=1)
        self.subtitle.grid(row=2, column=1)
        self.text.grid(row=3, column=1)

        self.options_labels = []
        self.options = []
        self.options_actions = []
        # Create and layout option labels
        tk.Label(self.options_frame, text="Options").grid(row=0, column=0)
        tk.Label(self.options_frame, text="Text").grid(row=0, column=1)
        tk.Label(self.options_frame, text="'Action String'").grid(row=0, column=2)

        # Create add and remove option buttons
        self.add_option_button = tk.Button(self.options_frame, text="+", command=self.add_option)
        self.remove_option_button = tk.Button(self.options_frame, text="-", command=self.remove_option)

        self.add_option()   # Does layout and adds first option row

        # Put picture in chart
        # TODO
        load = Image.open("C:/Users/James/PycharmProjects/andrews-card-creator/Assets/DickButt.jpg")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(master=self.graph_frame, image=render)
        img.image = render  # keep a reference to the image by attaching it to the label, else it'll be garbage collected
        img.pack()

        # Update window
        self.master.mainloop()

    def add_option(self):
        # Called upon by pressing add_option_button

        number_of_options = len(self.options)
        new_button_row = number_of_options+1

        # Update location of add and remove option buttons
        self.add_option_button.grid(row=new_button_row, column=3)
        self.remove_option_button.grid(row=new_button_row-1, column=3)

        # Add new option label
        label_text = str(number_of_options+1)
        self.options_labels.append(tk.Label(self.options_frame, text=label_text))
        self.options_labels[-1].grid(row=new_button_row, column=0)

        # Add a new option
        self.options.append(tk.Entry(self.options_frame))
        self.options[-1].grid(row=new_button_row, column=1)

        # Add a new option_action
        self.options_actions.append(tk.Entry(self.options_frame))
        self.options_actions[-1].grid(row=new_button_row, column=2)

    def remove_option(self):
        # Called upon by pressing remove_option_button

        if len(self.options) <= 1:
            return

        self.options_labels[-1].destroy()
        self.options_labels = self.options_labels[:-1]
        self.options[-1].destroy()
        self.options = self.options[:-1]
        self.options_actions[-1].destroy()
        self.options_actions = self.options_actions[:-1]

        new_button_row = len(self.options)
        self.add_option_button.grid(row=new_button_row, column=3)
        self.remove_option_button.grid(row=new_button_row - 1, column=3)

    def new_card(self):
        # TODO Clear fields
        # TODO Generate unique ID (not currently in use in folder) and fill in
        pass

    def open_card(self):
        # TODO create popup window for user to pick ID num to open
        # TODO fill in fields and options from card
        pass

    def save_card(self):
        # TODO if cardfile doesn't exist create it, else replace existing (cardfile and card in list)
        # TODO update graph
        pass

    def delete_card(self):
        # TODO delete cardfile and remove card from list
        # TODO update graph
        pass

    def generate_json(self):
        card = PlotCard(self.id, self.title, self.subtitle, self.text, self.options)
        return card.json()


card_manager = CardManager()
