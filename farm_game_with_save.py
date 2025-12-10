# farm_game.py
import asyncio
import tkinter as tk
from PIL import Image, ImageTk
import os
import json
import time

SAVE_FILE = "farm_save.json"

def save_game(state):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

plants = [
    {"id": 1, "name": "Wheat", "baseGrowTime": 5},
    {"id": 2, "name": "Carrot", "baseGrowTime": 3},
    {"id": 3, "name": "Potato", "baseGrowTime": 8},
]

fertilizers = {
    "basic": {"name": "Basic Fertilizer", "multiplier": 0.8, "price": 10},
    "super": {"name": "Super Fertilizer", "multiplier": 0.5, "price": 20},
}

IMAGE_FOLDER = r"C:\Users\hohli\OneDrive\Robochyi_stil\Plants_growing"
plant_images = {}
for plant in plants:
    images = []
    for stage in range(1, 4):
        path = os.path.join(IMAGE_FOLDER, f"{plant['name']}-{stage}.png")
        img = Image.open(path).resize((64, 64))
        images.append(ImageTk.PhotoImage(img))
    plant_images[plant['name']] = images

class Plot:
    def __init__(self, x, y, button):
        self.x = x
        self.y = y
        self.button = button
        self.state = "empty"
        self.plant = None
        self.stage = 0
        self.task = None

    async def plant_seed(self, plant, fertilizer, on_ready):
        if self.state != "empty":
            print(f"Plot ({self.x},{self.y}) is occupied!")
            return
        self.state = "growing"
        self.plant = plant
        self.stage = 0
        grow_time = plant["baseGrowTime"] * fertilizer["multiplier"]
        stage_time = grow_time / 3

        async def grow():
            for i in range(3):
                self.stage = i
                self.update_image()
                await asyncio.sleep(stage_time)
            self.state = "ready"
            await on_ready(self)

        self.task = asyncio.create_task(grow())

    def harvest(self):
        if self.state != "ready":
            return None
        harvested = self.plant
        self.state = "empty"
        self.plant = None
        self.stage = 0
        self.update_image()
        return harvested

    def update_image(self):
        if self.state == "empty":
            self.button.config(image='')
        else:
            img = plant_images[self.plant['name']][self.stage]
            self.button.config(image=img)
            self.button.image = img

class Barn:
    def __init__(self):
        self.storage = {}

    def add(self, plant):
        name = plant["name"]
        self.storage[name] = self.storage.get(name, 0) + 1

    def remove(self, plant_name, amount):
        if self.storage.get(plant_name, 0) < amount:
            return False
        self.storage[plant_name] -= amount
        return True

class Player:
    def __init__(self):
        self.balance = 50
        self.inventory = {"basic": 0, "super": 0}

    def buy_fertilizer(self, fert_type):
        f = fertilizers[fert_type]
        if self.balance < f["price"]:
            print("Not enough money!")
            return False
        self.balance -= f["price"]
        self.inventory[fert_type] += 1
        print(f"Bought {f['name']}. Balance: {self.balance}")
        return True

class Shop:
    @staticmethod
    def sell(plant_name, amount, price, player, barn):
        if not barn.remove(plant_name, amount):
            print("Not enough product in barn!")
            return False
        earned = amount * price
        player.balance += earned
        print(f"Sold {plant_name} x{amount}. Earned {earned}. Balance: {player.balance}")
        return True

class FarmGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Farm 5x5")
        self.player = Player()
        self.barn = Barn()

        self.farm = []
        for y in range(5):
            row = []
            for x in range(5):
                btn = tk.Button(self.root, width=64, height=64)
                btn.grid(row=y, column=x)
                plot = Plot(x, y, btn)
                row.append(plot)
            self.farm.append(row)

        tk.Button(self.root, text="Buy Basic Fertilizer", command=lambda: self.player.buy_fertilizer("basic")).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="Plant Wheat (0,0)", command=lambda: asyncio.create_task(self.plant_crop(0,0,"Wheat"))).grid(row=6, column=2)
        tk.Button(self.root, text="Harvest (0,0)", command=lambda: self.harvest_crop(0,0)).grid(row=6, column=3)
        tk.Button(self.root, text="Sell Wheat", command=lambda: Shop.sell("Wheat",1,12,self.player,self.barn)).grid(row=6, column=4)
        tk.Button(self.root, text="Save Game", command=self.save_game).grid(row=7, column=0, columnspan=2)
        tk.Button(self.root, text="Load Game", command=self.load_game).grid(row=7, column=2, columnspan=2)

        self.load_game()

    async def plant_crop(self, x, y, plant_name):
        plant = next(p for p in plants if p['name']==plant_name)
        await self.farm[y][x].plant_seed(plant, fertilizers["basic"], self.on_ready)

    async def on_ready(self, plot):
        harvested = plot.harvest()
        if harvested:
            self.barn.add(harvested)

    def harvest_crop(self, x, y):
        harvested = self.farm[y][x].harvest()
        if harvested:
            self.barn.add(harvested)

    def save_game(self):
        farm_state = []
        for row in self.farm:
            row_state = []
            for plot in row:
                if plot.plant:
                    row_state.append({"state": plot.state, "plant_name": plot.plant['name'], "stage": plot.stage})
                else:
                    row_state.append({"state": "empty"})
            farm_state.append(row_state)

        save_data = {"player": {"balance": self.player.balance, "inventory": self.player.inventory}, "barn": self.barn.storage, "farm": farm_state}
        save_game(save_data)
        print("Game saved!")

    def load_game(self):
        data = load_game()
        if not data:
            print("No save file found!")
            return
        self.player.balance = data["player"]["balance"]
        self.player.inventory = data["player"]["inventory"]
        self.barn.storage = data["barn"]
        for y, row in enumerate(self.farm):
            for x, plot in enumerate(row):
                plot_data = data["farm"][y][x]
                if plot_data["state"] == "empty":
                    plot.state = "empty"
                    plot.plant = None
                    plot.stage = 0
                else:
                    plant = next(p for p in plants if p['name']==plot_data["plant_name"])
                    plot.state = plot_data["state"]
                    plot.plant = plant
                    plot.stage = plot_data["stage"]
                    plot.update_image()
        print("Game loaded!")

    def run(self):
        self.root.mainloop()

game = FarmGame()
game.run()
