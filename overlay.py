import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
class Overlay:
    def __init__(self, map_name, cars):
        """
        desc: map_name is the name of the current map and cars is a list
        of the car build names to choose from that have been added
        returns none
        """
        self._map_name = map_name
        self.cars = cars
    def render(self):
        root = tk.Tk()
        root.geometry("500x500")
        root.title("Car Switcher")

        label = tk.Label(root, text=self._map_name)
        label.pack()

        for car in self.cars:
            car_label = tk.Label(root, text=car)
            car_label.pack()

        add_car  = tk.Button(root, text="Add Car Setup", command=self.UploadAction)
        add_car.pack()

        root.mainloop()
    def UploadAction(event=None):
            file_path = filedialog.askopenfilename()
            file_name = file_path.split("/")[-1]
            print(file_path, file_name)
    

test = Overlay("mapdd",  ['car.exe'])
test.render()