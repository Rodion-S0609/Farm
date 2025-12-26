import unittest

from achievements import AchievementManager
from Farm import Barn, Player, Shop, plants


class TestAchievements(unittest.TestCase):

    def setUp(self):
        self.manager = AchievementManager()

    def test_first_plant_achievement(self):
        self.manager.add_stat("plants_planted", 1, plant_type="Wheat")
        unlocked = self.manager.get_unlocked()
        self.assertTrue(any(a.id == "first_plant" for a in unlocked))

    def test_monoculture_achievement(self):
        for _ in range(20):
            self.manager.add_stat("plants_planted", 1, plant_type="Wheat")
        unlocked = self.manager.get_unlocked()
        self.assertTrue(any(a.id == "monoculture" for a in unlocked))

    def test_balance_achievement(self):
        self.manager.add_stat("balance", 500)
        unlocked = self.manager.get_unlocked()
        self.assertTrue(any(a.id == "golden_hands" for a in unlocked))


class TestBarn(unittest.TestCase):

    def setUp(self):
        self.barn = Barn()
        self.wheat = {"name": "Wheat"}

    def test_add_plant(self):
        self.barn.add(self.wheat)
        self.assertEqual(self.barn.storage["Wheat"], 1)

    def test_remove_plant_success(self):
        self.barn.add(self.wheat)
        result = self.barn.remove("Wheat", 1)
        self.assertTrue(result)
        self.assertEqual(self.barn.storage["Wheat"], 0)

    def test_remove_plant_fail(self):
        result = self.barn.remove("Wheat", 1)
        self.assertFalse(result)


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def test_buy_fertilizer_success(self):
        result = self.player.buy_fertilizer("basic")
        self.assertTrue(result)
        self.assertEqual(self.player.inventory["basic"], 1)

    def test_buy_fertilizer_fail(self):
        self.player.balance = 0
        result = self.player.buy_fertilizer("basic")
        self.assertFalse(result)


class TestShop(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.barn = Barn()
        self.barn.add({"name": "Wheat"})

    def test_sell_success(self):
        result = Shop.sell("Wheat", 1, 10, self.player, self.barn)
        self.assertTrue(result)
        self.assertEqual(self.player.balance, 60)

    def test_sell_fail(self):
        result = Shop.sell("Wheat", 5, 10, self.player, self.barn)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
