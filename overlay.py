import tkinter as tk
from tkinter import filedialog
import os
import functools
class Overlay:
    def __init__(self, map_name, cars, update_cars_callback, call_change_car_callback, main_loop_callback):
        """
        desc: map_name is the name of the current map and cars is a list
        of the car build names to choose from that have been added
        returns none
        """
        self._map_name = map_name
        self._cars = cars
        self._root = None
        self._update_cars_callback = update_cars_callback
        self._call_change_car_callback = call_change_car_callback
        self._main_loop_callback = main_loop_callback
    def render(self):
        root = tk.Tk()
        self._root = root

        #root.attributes('-type', 'dock')
        root.attributes('-topmost', True)  # Makes the window always on top
        root.overrideredirect(True)  # Removes the window frame

        root.geometry("500x500+0+500")
        root.title("Car Switcher")

        label = tk.Label(root, text=self._map_name)
        label.pack()

        self.appendButton(self._cars)

        add_car  = tk.Button(root, text="Add Car Setup", command=self.UploadAction)
        add_car.pack()
        
        root.after(500, self._opacity_callback)
        root.mainloop()

    def alpha(self, alpha):
        self._root.attributes('-alpha', alpha)
    def appendButton(self, adding):
         if adding == [None]:
            return
         for text in adding:
            callback = functools.partial(self._call_change_car_callback, text)
            car_label = tk.Button(self._root, text=text.split("/")[-1], command=callback)
            car_label.pack()
    def UploadAction(self):
            file_path = filedialog.askopenfilenames(filetypes=[('Car Setups', '*.sto')], initialdir=os.path.expanduser(r'~\Documents\iRacing\setups'))
            print(file_path)
            self.appendButton(file_path)
            if self._cars == [None]:
                self._cars = [*file_path]
            else:
                self._cars.append(*file_path)
            self._update_cars_callback(self._map_name, self._cars)
    def _opacity_callback(self):
        self._main_loop_callback()
        self._root.after(2000, self._opacity_callback)