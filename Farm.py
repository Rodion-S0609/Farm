import asyncio
import tkinter as tk
from PIL import Image, ImageTk
import os

# ==========================
#          DATA
# ==========================

plants = [
    {"id": 1, "name": "Wheat", "baseGrowTime": 5},
    {"id": 2, "name": "Carrot", "baseGrowTime": 3},
    {"id": 3, "name": "Potato", "baseGrowTime": 8},
]

fertilizers = {
    "basic": {"name": "Basic Fertilizer", "multiplier": 0.8, "price": 10},
    "super": {"name": "Super Fertilizer", "multiplier": 0.5, "price": 20},
}

# Folder with plant images
IMAGE_FOLDER = r"C:\Users\hohli\OneDrive\Robochyi_stil\Plants_growing"

# Load all images for stages
plant_images = {}
for plant in plants:
    images = []
    for stage in range(1, 4):
        path = os.path.join(IMAGE_FOLDER, f"{plant['name']}-{stage}.png")
        img = Image.open(path).resize((64, 64))
        images.append(ImageTk.PhotoImage(img))
    plant_images[plant['name']] = images

# ==========================
#          PLOT
# ==========================

class Plot:
    def __init__(self, x, y, button):
        self.x = x
        self.y = y
        self.button = button
        self.state = "empty"  # empty / growing / ready
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
        stage_time = grow_time / 3  # 3 stages

        print(f"Planting {plant['name']} at ({self.x},{self.y}). Grow time: {grow_time} sec...")

        async def grow():
            for i in range(3):
                self.stage = i
                self.update_image()
                await asyncio.sleep(stage_time)
            self.state = "ready"
            print(f"{plant['name']} at ({self.x},{self.y}) is ready!")
            await on_ready(self)

        self.task = asyncio.create_task(grow())

    def harvest(self):
        if self.state != "ready":
            print(f"Plot ({self.x},{self.y}) is not ready!")
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
            self.button.image = img  # prevent garbage collection

# ==========================
#          BARN
# ==========================

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

# ==========================
#          PLAYER
# ==========================

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

# ==========================
#          SHOP
# ==========================

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

# ==========================
#       FARM GAME GUI
# ==========================

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

        # Action buttons
        tk.Button(self.root, text="Buy Basic Fertilizer", command=lambda: self.player.buy_fertilizer("basic")).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="Plant Wheat (0,0)", command=lambda: asyncio.create_task(self.plant_crop(0,0,"Wheat"))).grid(row=6, column=2)
        tk.Button(self.root, text="Harvest (0,0)", command=lambda: self.harvest_crop(0,0)).grid(row=6, column=3)
        tk.Button(self.root, text="Sell Wheat", command=lambda: Shop.sell("Wheat",1,12,self.player,self.barn)).grid(row=6, column=4)

    async def plant_crop(self, x, y, plant_name):
        plant = next(p for p in plants if p['name']==plant_name)
        await self.farm[y][x].plant_seed(plant, fertilizers["basic"], self.on_ready)

    async def on_ready(self, plot):
        harvested = plot.harvest()
        self.barn.add(harvested)
        print("Barn:", self.barn.storage)
        print("Balance:", self.player.balance)

    def harvest_crop(self, x, y):
        harvested = self.farm[y][x].harvest()
        if harvested:
            self.barn.add(harvested)
            print("Barn:", self.barn.storage)

    def run(self):
        self.root.mainloop()


# ==========================
#          RUN
# ==========================

game = FarmGame()
game.run()
