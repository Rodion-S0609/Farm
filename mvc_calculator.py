# MVC Calculator Project (Console Version)
# Files represented in a single script for convenience
# Structure:
# - Model: CalculatorModel
# - View: ConsoleView
# - Controller: CalculatorController

class CalculatorModel:
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Нельзя делить на ноль")
        return a / b


class ConsoleView:
    def show_menu(self):
        print("\n=== MVC Calculator ===")
        print("1) Сложение (+)")
        print("2) Вычитание (-)")
        print("3) Умножение (*)")
        print("4) Деление (/)")
        print("5) Выход")

    def get_input(self, msg):
        return input(msg)

    def show_result(self, result):
        print(f"Результат: {result}")

    def show_error(self, msg):
        print(f"Ошибка: {msg}")


class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.get_input("Выберите действие: ")

            if choice == "5":
                print("Выход...")
                break

            if choice not in ["1", "2", "3", "4"]:
                self.view.show_error("Неверный пункт меню")
                continue

            try:
                a = float(self.view.get_input("Введите первое число: "))
                b = float(self.view.get_input("Введите второе число: "))

                if choice == "1":
                    result = self.model.add(a, b)
                elif choice == "2":
                    result = self.model.sub(a, b)
                elif choice == "3":
                    result = self.model.mul(a, b)
                elif choice == "4":
                    result = self.model.div(a, b)

                self.view.show_result(result)

            except ValueError:
                self.view.show_error("Введите корректные числа!")

            except ZeroDivisionError as e:
                self.view.show_error(str(e))


if __name__ == "__main__":
    model = CalculatorModel()
    view = ConsoleView()
    controller = CalculatorController(model, view)
    controller.run()
