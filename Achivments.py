class Achievement:
    def __init__(self, id, title, description, condition):
        self.id = id
        self.title = title
        self.description = description
        self.condition = condition
        self.unlocked = False

    def check(self, stats):
        """Проверяет, выполнено ли условие. Если да, возвращает True."""
        if not self.unlocked and self.condition(stats):
            self.unlocked = True
            return True
        return False


class AchievementManager:
    def __init__(self):
        # Статистика для ачивок
        self.stats = {
            "plants_planted": 0,
            "plants_harvested": 0,
            "fertilizers_used": 0,
            "plots_owned": 0,
            "plants_sold": 0,
            "balance": 0,
            "plants_per_type": {},  # для "Монокультура" и "Ботаник"
        }

        # Список ачивок
        self.achievements = [
            # 🌱 Посадка и рост
            Achievement(
                "first_plant",
                "Первый росток",
                "Посадите первое растение",
                lambda s: s["plants_planted"] >= 1
            ),
            Achievement(
                "gardener",
                "Огородник",
                "Посадите 10 растений",
                lambda s: s["plants_planted"] >= 10
            ),
            Achievement(
                "farmer",
                "Фермер",
                "Посадите 50 растений",
                lambda s: s["plants_planted"] >= 50
            ),
            Achievement(
                "monoculture",
                "Монокультура",
                "Посадите 20 растений одного вида",
                lambda s: any(v >= 20 for v in s["plants_per_type"].values())
            ),
            Achievement(
                "botanist",
                "Ботаник",
                "Посадите все виды растений хотя бы по одному разу",
                lambda s: all(v >= 1 for v in s["plants_per_type"].values())
            ),

            # 🌾 Урожай
            Achievement(
                "first_harvest",
                "Первый урожай",
                "Соберите первое растение",
                lambda s: s["plants_harvested"] >= 1
            ),
            Achievement(
                "harvest_25",
                "Жатва",
                "Соберите 25 растений",
                lambda s: s["plants_harvested"] >= 25
            ),
            Achievement(
                "harvest_100",
                "Комбайн",
                "Соберите 100 растений",
                lambda s: s["plants_harvested"] >= 100
            ),
            Achievement(
                "harvest_all",
                "Ничего не пропало",
                "Соберите урожай со всех грядок одновременно",
                lambda s: s.get("harvest_all_flag", False)
            ),

            # 🧪 Удобрения
            Achievement(
                "fertilizer_5",
                "Химик-любитель",
                "Используйте 5 удобрений",
                lambda s: s["fertilizers_used"] >= 5
            ),
            Achievement(
                "fertilizer_25",
                "Химик",
                "Используйте 25 удобрений",
                lambda s: s["fertilizers_used"] >= 25
            ),

            # 🧱 Грядки и ферма
            Achievement(
                "first_plot",
                "Маленький огород",
                "Купите первую дополнительную грядку",
                lambda s: s["plots_owned"] >= 1
            ),
            Achievement(
                "plots_5",
                "Расширение территории",
                "Купите 5 новых грядок",
                lambda s: s["plots_owned"] >= 5
            ),
            Achievement(
                "all_plots",
                "Фермер-магнат",
                "Купите все доступные грядки",
                lambda s: s["plots_owned"] >= 16
            ),

            # 💰 Экономика
            Achievement(
                "first_sale",
                "Первая продажа",
                "Продайте любое растение",
                lambda s: s["plants_sold"] >= 1
            ),
            Achievement(
                "earned_50",
                "Мелкий торговец",
                "Заработайте 50 монет на продажах",
                lambda s: s["balance"] >= 50
            ),
            Achievement(
                "earned_200",
                "Купец",
                "Заработайте 200 монет на продажах",
                lambda s: s["balance"] >= 200
            ),
            Achievement(
                "golden_hands",
                "Золотые руки",
                "Достигните баланса 500 монет",
                lambda s: s["balance"] >= 500
            ),
        ]

    def add_stat(self, key, amount=1, plant_type=None):
        """Добавляем к статистике и проверяем ачивки."""
        if key == "plants_planted" and plant_type:
            # отслеживаем по видам для Монокультура и Ботаник
            if plant_type not in self.stats["plants_per_type"]:
                self.stats["plants_per_type"][plant_type] = 0
            self.stats["plants_per_type"][plant_type] += amount

        self.stats[key] += amount
        self.check_achievements()

    def set_flag(self, key, value=True):
        """Для специальных условий (например harvest_all_flag)."""
        self.stats[key] = value
        self.check_achievements()

    def check_achievements(self):
        """Проверяем все ачивки и выводим новые."""
        for ach in self.achievements:
            if ach.check(self.stats):
                print(f"🏆 Ачивка получена: {ach.title} — {ach.description}")

    def get_unlocked(self):
        """Возвращает список всех открытых ачивок."""
        return [a for a in self.achievements if a.unlocked]
