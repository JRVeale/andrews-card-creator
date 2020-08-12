# Prereqs https://www2.graphviz.org/Packages/stable/windows/10/msbuild/Release/Win32/graphviz-2.38-win32.msi
# Can be found as the .msi @ https://www2.graphviz.org/Packages/stable/windows/10/msbuild/Release/Win32/

# build with pyinstaller with the command pyinstaller -F card_creator.py

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import simplejson   # needed so that is included in exe build
import jsonpickle
import os
import pydot

from plotcard import PlotCard
from CanvasImage import CanvasImage


class CardManager:

    def __init__(self):
        self.version = "1.0"

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
        self.master.title("Card Creator v" + self.version)

        # Create main containers
        self.graph_frame = tk.Frame(self.master, bg="white")
        self.details_frame = tk.Frame(self.master, bg="white")
        # Layout main containers
        self.graph_frame.grid(row=0, column=1)
        self.details_frame.grid(row=0, column=0, sticky="n")

        # Create details containers
        self.buttons_frame = tk.Frame(self.details_frame, bg="white")
        self.fields_frame = tk.Frame(self.details_frame, bg="white")
        self.options_frame = tk.Frame(self.details_frame, bg="white")
        # Layout details containers
        self.buttons_frame.grid(row=0, column=0, sticky="W")
        self.fields_frame.grid(row=1, column=0)
        self.options_frame.grid(row=2, column=0)

        # Create buttons
        self.new_button = tk.Button(self.buttons_frame, text="NEW", command=self.new_card, width=20)
        self.open_button = tk.Button(self.buttons_frame, text="OPEN", command=self.open_card, width=20)
        self.save_button = tk.Button(self.buttons_frame, text="SAVE", command=self.save_card, width=20)
        self.delete_button = tk.Button(self.buttons_frame, text="DELETE", command=self.delete_card_button_func, width=20)
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
        self.id = tk.Entry(self.fields_frame, width=107)
        self.id.configure(state="readonly")
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
        self.set_new_id()

        self.image = None
        self.redraw_graph()

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
            return -1

        self.options_labels[-1].destroy()
        self.options_labels = self.options_labels[:-1]
        self.options[-1].destroy()
        self.options = self.options[:-1]
        self.options_actions[-1].destroy()
        self.options_actions = self.options_actions[:-1]

        new_button_row = len(self.options)
        self.add_option_button.grid(row=new_button_row, column=3)
        self.remove_option_button.grid(row=new_button_row - 1, column=3)
        return 0

    def new_card(self):
        # Empty all the fields
        self.clear_all()

        # Fill in available id
        self.set_new_id()

    def open_card(self):
        # Get card to edit
        desired_id = tk.simpledialog.askinteger("Open Card", "Enter card ID to open for edit",
                                                parent=self.master, minvalue=0)
        if desired_id is None:
            return
        if desired_id not in self.get_used_ids():
            tk.messagebox.showerror("Error", "No cardfile with id " + str(desired_id))
            return
        for card in self.cards:
            # Find card for desired_id
            if card.id == desired_id:
                # Clear current values
                self.clear_all()

                # Fill in fields from card
                self.id.configure(state=tk.NORMAL)
                self.id.insert(0, str(card.id).zfill(4))
                self.id.configure(state="readonly")

                self.title.insert(0, card.title)
                self.subtitle.insert(0, card.subtitle)
                self.text.insert("1.0", card.text)

                # Fill in options from card
                num_options = len(card.plotcardoptions)
                for i in range(0, num_options - 1):
                    self.add_option()
                for i in range(0, num_options):
                    self.options[i].insert(0, card.plotcardoptions[i].text)
                    self.options_actions[i].insert(0, card.plotcardoptions[i].action_string)

                # Update graph
                self.redraw_graph()
                return

    def save_card(self):
        # Delete old card from list
        self.delete_card()

        # Create card and add to list
        new_card = PlotCard(self.id, self.title, self.subtitle, self.text, self.options, self.options_actions)
        self.cards.append(new_card)

        # Create cardfile and save
        full_filepath = self.directory + "/Card_" + str(self.id.get().zfill(4)) + ".json"
        self.card_files.append(full_filepath)
        print("Saved card " + str(self.id.get()) + " to " + full_filepath)
        f = open(full_filepath, "w+")
        f.write(self.cards[-1].json())
        f.close()

        # Update graph
        self.redraw_graph()

    def delete_card_button_func(self):
        self.delete_card()

        # Get ready to make a new card
        self.new_card()

        # Update graph
        self.redraw_graph()

    def delete_card(self):
        # Find index for this id (same for cards and cardfiles lists)
        for i in range(0, len(self.cards)):
            # Find card for currently editted if has been saved
            if self.cards[i].id == int(self.id.get()):
                self.cards.pop(i)                   # remove from cards list
                cardfile = self.card_files.pop(i)   # remove from cardfiles list
                os.remove(cardfile)                 # Delete cardfile itself
                break

    def redraw_graph(self):
        # Create graph
        graph = pydot.Dot(graph_type="digraph")
        graph.set_node_defaults(color="lightgray", style="filled", shape="box")

        # Create all the nodes and add them to graph
        nodes = {}
        for card in self.cards:
            if len(card.title) > 20:
                node_title = card.title[:20] + "..."
            else:
                node_title = card.title
            nodes[card.id] = pydot.Node(str(card.id).zfill(4) + "\n" + node_title)
            graph.add_node(nodes[card.id])

        # Create all edges and add them to graph
        for card in self.cards:
            for o in card.plotcardoptions:
                ids = o.get_possible_destination_ids()
                for i in ids:
                    try:
                        graph.add_edge(pydot.Edge(nodes[card.id], nodes[i]))
                    except KeyError:
                        pass

        # Save image
        full_filename = self.directory + "/CardGraph.png"
        graph.write_png(full_filename)

        # Load into graph_frame (deleting previous)
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        '''
        load = Image.open(full_filename)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(master=self.graph_frame, image=render)
        self.image = render  # keep a reference to the image by attaching it to the label, else it gets garbage collected
        img.pack()
        '''
        canvas = CanvasImage(self.graph_frame, full_filename, width=1000, height=800)
        canvas.grid(row=0, column=0)

        # TODO Make zoom and pan-able

    def clear_all(self):
        self.id.configure(state=tk.NORMAL)
        self.id.delete(0, tk.END)
        self.id.configure(state="readonly")

        self.title.delete(0, tk.END)
        self.subtitle.delete(0, tk.END)
        self.text.delete("1.0", tk.END)

        while self.remove_option() == 0:
            pass

        self.options[-1].delete(0, tk.END)
        self.options_actions[-1].delete(0, tk.END)

    def get_used_ids(self):
        used_ids = []
        for card in self.cards:
            used_ids.append(card.id)
        return used_ids

    def set_new_id(self):
        self.id.configure(state=tk.NORMAL)
        self.id.insert(0, str(self.get_next_id()).zfill(4))
        self.id.configure(state="readonly")

    def get_next_id(self):
        used_ids = self.get_used_ids()  # an unordered list of IDs in use
        num_used_ids = len(used_ids)
        l = [False] * num_used_ids      # a list of bools as long as the number of IDs in use
        for i in used_ids:              # if an ID is used and is less than length, set l[ID] to True
            if i < num_used_ids:
                l[i] = True
        # Now the first false is in the position of lowest available unsigned int, if all are true, the answer is N
        for i in range(0, num_used_ids):
            if not l[i]:
                return i
        return num_used_ids


card_manager = CardManager()
