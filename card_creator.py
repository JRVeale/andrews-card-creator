import tkinter as tk


class Window:

    def __init__(self):
        # create window
        self.master = tk.Tk()
        self.master.title("Card Creator")

        # Draw labels
        tk.Label(self.master, text="Title").grid(row=0)
        tk.Label(self.master, text="Subtitle").grid(row=1)
        tk.Label(self.master, text="Text").grid(row=2)
        tk.Label(self.master, text="Options").grid(row=3)
        tk.Label(self.master, text="1").grid(row=4)

        # Add entry boxes
        self.title = tk.Entry(self.master, width=107)
        self.subtitle = tk.Entry(self.master, width=107)
        self.text = tk.Text(self.master)
        self.options = []
        self.options.append(tk.Entry(self.master, width=107))
        self.add_option_button = tk.Button(self.master, text="+", command=self.add_option)

        self.title.grid(row=0, column=1)
        self.subtitle.grid(row=1, column=1)
        self.text.grid(row=2, column=1)
        self.options[0].grid(row=4, column=1)
        self.add_option_button.grid(row=4, column=2)

        # Add generate JSON button
        self.generate_button = tk.Button(self.master, text="Generate", command=self.generate_JSON)
        self.generate_button.grid(row=5, column=1)

        # Add output Text field
        tk.Label(self.master, text="Output JSON").grid(row=1, column=4)
        self.output_JSON = tk.Text(self.master, state="disabled")
        self.output_JSON.grid(row=2, column=4)

        # Update window
        self.master.mainloop()

    def add_option(self):
        # Called upon by pressing add_option_button
        number_of_options = len(self.options)
        new_button_row = number_of_options+3
        self.add_option_button.grid(row=new_button_row, column=2)
        self.options.append(tk.Entry(self.master, width=107))
        self.options[-1].grid(row=new_button_row, column=1)
        label_text = str(number_of_options)
        tk.Label(self.master, text=label_text).grid(row=new_button_row)
        self.update_generate_button_position(new_button_row)

    def update_generate_button_position(self, new_button_row):
        self.generate_button.grid(row=new_button_row+1)
        # Moves generate button to the bottom of the page

    def generate_JSON(self):
        self.output_JSON.configure(state="normal")
        self.output_JSON.delete(1.0, "end")
        card = PlotCard()                           # Todo: Implement PlotCard
        self.output_JSON.insert(1.0, card.JSON())   # Todo: Implement PlotCard.JSON()
        self.output_JSON.configure(state="disabled")




window = Window()
