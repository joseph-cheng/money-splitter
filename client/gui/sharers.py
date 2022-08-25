import tkinter as tk
from tkinter import ttk
import config


class GuiSharers:

    WIDTH = 100

    def __init__(self, container_receipt, container_item, num_sharers, row, start_column, sharer_names, underlying_sharers=None):
        self.container_receipt = container_receipt
        self.container_item = container_item
        self.num_sharers = num_sharers
        self.row = row
        self.start_column = start_column
        self.sharer_names = sharer_names

        # this gets immediately swapped in self.create_widgets()
        self.checkbuttons_showing = False

        self.create_widgets()
        self.format_widgets()

        self.underlying_sharers = underlying_sharers 
        if self.underlying_sharers is None:
            self.trace_variables()
            self.make_dirty()
        else:
            self.dirty = False

    def make_dirty(self):
        self.dirty = True
        self.container_item.make_dirty()
        self.container_receipt.make_dirty()


    def get_underlying_sharers(self):
        if self.dirty:
            self.update_underlying_sharers()
        return self.underlying_sharers

    def update_underlying_sharers(self):
        if not(self.dirty):
            return
        sharer_values = self.get_sharer_values()
        self.underlying_sharers = {sharer_name: sharer_value for sharer_name, sharer_value in zip(self.sharer_names, sharer_values)}
        self.dirty = False


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
            checkbuttons_toggled = 0
            for var in self.checkbutton_vars:
                if var.get() == "1":
                    checkbuttons_toggled += 1
            for var in self.checkbutton_vars:
                if var.get() == "1":
                    ret.append(1/checkbuttons_toggled)
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

            if total_sum == 0:
                total_sum = 1
            if abs(total_sum - 1) >= config.EPSILON:
                print("WARNING: sharers do not sum to 1, implicitly normalising")
            for var in self.entry_vars:
                try:
                    ret.append(float(var.get()) / total_sum)
                except ValueError:
                    pass
        return ret

    def set_sharer_entrys(self):
        self.make_dirty()
        total_sharers = 0
        for sharer_var in self.checkbutton_vars:
            if sharer_var.get() == "1":
                total_sharers += 1
        for ii, (sharer_entry, entry_var) in enumerate(zip(self.sharer_entrys, self.entry_vars)):
            if self.checkbutton_vars[ii].get() == "1":
                entry_var.set(1/total_sharers)
            else:
                entry_var.set(0)

    def sharer_change_callback(self):
        self.make_dirty()
        self.container_receipt.update_cost_labels()


    def create_widgets(self):
        self.sharer_checkbuttons = []
        self.checkbutton_vars = []

        for ii in range(self.num_sharers):
            sharer_var = tk.StringVar()
            sharer_checkbutton = ttk.Checkbutton(self.container_receipt, variable=sharer_var, command=self.set_sharer_entrys)
            self.sharer_checkbuttons.append(sharer_checkbutton)
            self.checkbutton_vars.append(sharer_var)

        self.sharer_entrys = []
        self.entry_vars = []

        for ii in range(self.num_sharers):
            sharer_var = tk.StringVar()
            sharer_entry = ttk.Entry(self.container_receipt, width=5, textvariable=sharer_var)
            self.sharer_entrys.append(sharer_entry)
            self.entry_vars.append(sharer_var)

        self.granular = tk.StringVar()
        self.granular_button = ttk.Checkbutton(self.container_receipt, variable=self.granular, command=self.swap)
        self.swap()

    def trace_variables(self):
        for entry_var in self.entry_vars:
            entry_var.trace("w", lambda *_: self.sharer_change_callback())


    def format_widgets(self):
        options = {'padx': 5, 'pady': 5}
        if self.checkbuttons_showing:
            for ii, sharer_checkbutton in enumerate(self.sharer_checkbuttons):
                sharer_checkbutton.grid(column=self.start_column + ii, row=self.row, padx=20)

        else:
            for ii, sharer_entry in enumerate(self.sharer_entrys):
                sharer_entry.grid(column=self.start_column + ii, row=self.row)
        self.granular_button.grid(column=12, row=self.row, **options)

    def delete(self):
        for sharer_checkbutton in self.sharer_checkbuttons:
            sharer_checkbutton.grid_forget()

        for sharer_entry in self.sharer_entrys:
            sharer_entry.grid_forget()

        self.granular_button.grid_forget()

    @staticmethod
    def create_from_data(sharers, parent_receipt, parent_container, row, start_column):
        ret = GuiSharers(parent_receipt, parent_container, len(sharers), row, start_column, parent_receipt.sharer_names, underlying_sharers=sharers)
        unique_sharer_values = set(sharers.values())
        # if this is true, then we should use checkbuttons
        if 0 in unique_sharer_values and len(unique_sharer_values) == 2 or len(unique_sharer_values) == 1:
            for ii, sharer in enumerate(sharers):
                if sharers[sharer] != 0:
                    ret.checkbutton_vars[ii].set("1")
        # otherwise, use the entry fields
        else:
            ret.swap()
            for ii, sharer in enumerate(sharers):
                ret.entry_vars[ii].set(str(sharers[sharer]))

        ret.trace_variables()
        return ret




