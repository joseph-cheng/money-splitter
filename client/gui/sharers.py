import tkinter as tk
from tkinter import ttk

class GuiSharers:

    WIDTH = 100

    def __init__(self, container, num_sharers, row, start_column=4):
        self.container = container
        self.num_sharers = num_sharers
        self.row = row
        self.start_column = start_column

        # this gets immediately swapped in self.create_widgets()
        self.checkbuttons_showing = False

        self.create_widgets()
        self.format_widgets()

    def shift_up_row(self):
        self.row = self.row - 1
        self.format_widgets()


    def swap(self):
        if self.checkbuttons_showing:
            for checkbutton in self.sharer_checkbuttons:
                checkbutton.grid_forget()
            for ii, entry in enumerate(self.sharer_entrys):
                entry.grid(column=self.start_column + ii, row=self.row)
                entry.tkraise()

        else:
            for ii, checkbutton in enumerate(self.sharer_checkbuttons):
                checkbutton.grid(column=self.start_column + ii, row=self.row, padx=20)
                checkbutton.tkraise()
            for entry in self.sharer_entrys:
                entry.grid_forget()
        self.checkbuttons_showing = not(self.checkbuttons_showing)

    def get_sharer_values(self):
        ret = []
        if self.checkbuttons_showing:
            for var in self.checkbutton_vars:
                if var.get() == "1":
                    ret.append(1/self.num_sharers)
                else:
                    ret.append(0)

        else:
            total_sum = 0
            for var in self.entry_vars:
                try:
                    total_sum += float(var.get())
                except ValueError:
                    print(f"WARNING: sharer value '{var.get()}' cannot be converted to float, ignoring")
                    pass

            if total_sum - 1 >= config.EPSILON:
                print("WARNING: sharers do not sum to 1, implicitly normalising")
            for var in self.entry_vars:
                try:
                    ret.append(float(var.get()) / total_sum)
                except ValueError:
                    pass
        return ret


    def create_widgets(self):
        self.sharer_checkbuttons = []
        self.checkbutton_vars = []

        def set_sharer_entrys():
            total_sharers = 0
            for sharer_var in self.checkbutton_vars:
                if sharer_var.get() == "1":
                    total_sharers += 1
            for ii, (sharer_entry, entry_var) in enumerate(zip(self.sharer_entrys, self.entry_vars)):
                if self.checkbutton_vars[ii].get() == "1":
                    entry_var.set(1/total_sharers)
                else:
                    entry_var.set(0)



        for ii in range(self.num_sharers):
            sharer_var = tk.StringVar()
            sharer_checkbutton = ttk.Checkbutton(self.container, variable=sharer_var, command=set_sharer_entrys)
            self.sharer_checkbuttons.append(sharer_checkbutton)
            self.checkbutton_vars.append(sharer_var)

        self.sharer_entrys = []
        self.entry_vars = []

        for ii in range(self.num_sharers):
            sharer_var = tk.StringVar()
            sharer_entry = ttk.Entry(self.container, width=5, textvariable=sharer_var)
            self.sharer_entrys.append(sharer_entry)
            self.entry_vars.append(sharer_var)

        self.swap()


    def format_widgets(self):
        if self.checkbuttons_showing:
            for ii, sharer_checkbutton in enumerate(self.sharer_checkbuttons):
                sharer_checkbutton.grid(column=self.start_column + ii, row=self.row, padx=20)

        else:
            for ii, sharer_entry in enumerate(self.sharer_entrys):
                sharer_entry.grid(column=self.start_column + ii, row=self.row)

    def delete(self):
        for sharer_checkbutton in self.sharer_checkbuttons:
            sharer_checkbutton.grid_forget()

        for sharer_entry in self.sharer_entrys:
            sharer_entry.grid_forget()

