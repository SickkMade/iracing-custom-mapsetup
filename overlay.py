import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
class Overlay:
    def __init__(self, map_name, cars, update_cars_callback, call_change_car_callback):
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
        self._current_car = None
    @property
    def cars(self):
        return self._cars
    def render(self):
        root = tk.Tk()
        self._root = root

        root.geometry("500x500")
        root.title("Car Switcher")

        label = tk.Label(root, text=self._map_name)
        label.pack()

        self.appendButton(self._cars)

        add_car  = tk.Button(root, text="Add Car Setup", command=self.UploadAction)
        add_car.pack()

        root.mainloop()
    def appendButton(self, adding):
         for text in adding:
            self._current_car = text
            car_label = tk.Button(self._root, text=text.split("/")[-1], command=self.change_car)
            car_label.pack()
    def change_car(self):
         self._call_change_car_callback(self._current_car)
    def UploadAction(self):
            file_path = filedialog.askopenfilenames()
            self.appendButton(file_path)
            if self._cars == [None]:
                self._cars = file_path
            else:
                 self._cars.append(file_path)
            self._update_cars_callback(self._map_name, self._cars)