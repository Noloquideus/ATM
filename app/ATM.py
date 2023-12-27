import decimal
import tkinter as tk

from database.utils import card_database_manager, user_database_manager
from database.utils.cards_table.CardDatabaseManager import find_card
from logger import configure_logger


# Configure the logger
configure_logger()


class ATM:
    """
    Initializes a new instance of the class.
    """

    def __init__(self):
        """
        Initializes the object.
        """
        self.root = tk.Tk()
        self.interface = self.Interface(self.root)

    class Interface:
        """
        Initializes an instance of the class with the given `root` parameter.
        """

        def __init__(self, root):
            self.root = root
            self.login_button = None
            self.login_entry = None
            self.password_entry = None

        def start(self):
            self.root.title("Bank")  # set window title
            self.root.geometry("800x600")  # set window size
            self.root.configure(bg="#000000")  # set color

            self.login_button = tk.Button(self.root, text="Sign in", command=self.show_login_fields)
            self.login_button.pack(pady=10)

            self.root.mainloop()

        def show_login_fields(self):
            """
            Creates and displays login fields in the GUI.
            Parameters:
            - self (object): The instance of the class.
            """
            self.login_button.destroy()  # remove login button

            """
            Creates and displays login fields in the GUI.
            """
            login_label = tk.Label(self.root, text="Login:", font=("Arial", 18), bg="#000000", fg="#FFFFFF")
            login_label.pack(pady=10)

            self.login_entry = tk.Entry(self.root, font=("Arial", 14))
            self.login_entry.pack(pady=5)
            """
            Creates and displays password fields in the GUI.
            """
            password_label = tk.Label(self.root, text="Password:", font=("Arial", 18), bg="#000000", fg="#FFFFFF")
            password_label.pack(pady=10)

            self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
            self.password_entry.pack(pady=5)

            login_button = tk.Button(self.root, text="Авторизоваться", command=self.authenticate)
            login_button.pack(pady=10)

        def display_message(self, message, color):
            message_label = tk.Label(self.root, text=message, font=("Arial", 16), bg="#000000", fg=color)
            message_label.pack(pady=10)

        def authenticate(self):
            login = self.login_entry.get()
            password = self.password_entry.get()

            # Use the UserDatabaseManager for search user
            user = user_database_manager.find_user(login)

            """
            Checks if the user exists and the password is correct.
            """
            if user and user["password"] == password:
                self.display_message("Авторизация успешна", "green")
                # Use the CardDatabaseManager for search user
                user_cards = card_database_manager.find_user_cards(user["uid"])
                self.clear_login_fields()
                self.display_user_cards(user_cards)
                self.display_transaction_buttons()
            else:
                self.display_message("Неверный логин или пароль", "red")
                self.clear_login_fields()
                self.root.after(1000, self.clear_message)

        def clear_login_fields(self):
            self.login_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

        def clear_message(self):
            """
            Clears the login fields by deleting the text in both the login entry and password entry widgets.
            """
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("text") == "Неверный логин или пароль":
                    widget.destroy()

        def display_user_cards(self, user_cards):
            """
            Display the user's cards on the screen.
            """
            for widget in self.root.winfo_children():
                widget.destroy()

            cards_label = tk.Label(self.root, text="Ваши карты:", font=("Arial", 18), bg="#000000", fg="#FFFFFF")
            cards_label.pack(pady=10)

            for card in user_cards:
                card_info = f"Номер карты:\n {card['number']} \nБаланс: {card['balance']}\n"
                card_label = tk.Label(self.root, text=card_info, font=("Arial", 14), bg="#000000", fg="#FFFFFF")
                card_label.pack(pady=5)

        def display_transaction_buttons(self):
            """
            Display transaction buttons for deposit, withdraw, and transfer operations.
            """
            deposit_button = tk.Button(self.root, text="Внести деньги", command=self.display_deposit_window)
            deposit_button.pack(pady=10)

            withdraw_button = tk.Button(self.root, text="Снять деньги", command=self.display_withdraw_window)
            withdraw_button.pack(pady=10)

            transfer_button = tk.Button(self.root, text="Перевести деньги", command=self.display_transfer_window)
            transfer_button.pack(pady=10)

        def display_deposit_window(self):
            """
            Creates and displays a deposit window for entering card number and amount.
            """
            deposit_window = tk.Toplevel(self.root)
            deposit_window.title("Внести деньги")
            deposit_window.geometry("400x300")

            card_number_label = tk.Label(deposit_window, text="Номер карты", font=("Arial", 18))
            card_number_label.pack(pady=10)

            card_number_entry = tk.Entry(deposit_window, font=("Arial", 14))
            card_number_entry.pack(pady=5)

            amount_label = tk.Label(deposit_window, text="Сумма:", font=("Arial", 18))
            amount_label.pack(pady=10)

            amount_entry = tk.Entry(deposit_window, font=("Arial", 14))
            amount_entry.pack(pady=5)

            deposit_button = tk.Button(
                deposit_window,
                text="Внести",
                command=lambda: self.deposit_money(card_number_entry.get(), amount_entry.get()),
            )
            deposit_button.pack(pady=10)

        def display_withdraw_window(self):
            """
            Creates and displays a withdrawal window.
            """
            withdraw_window = tk.Toplevel(self.root)
            withdraw_window.title("Снять деньги")
            withdraw_window.geometry("400x300")

            card_number_label = tk.Label(withdraw_window, text="Номер карты", font=("Arial", 18))
            card_number_label.pack(pady=10)

            card_number_entry = tk.Entry(withdraw_window, font=("Arial", 14))
            card_number_entry.pack(pady=5)

            amount_label = tk.Label(withdraw_window, text="Сумма", font=("Arial", 18))
            amount_label.pack(pady=10)

            amount_entry = tk.Entry(withdraw_window, font=("Arial", 14))
            amount_entry.pack(pady=5)

            withdraw_button = tk.Button(
                withdraw_window,
                text="Снять",
                command=lambda: self.withdraw_money(card_number_entry.get(), amount_entry.get()),
            )
            withdraw_button.pack(pady=10)

        def display_transfer_window(self):
            """
            Display the transfer window for transferring money.
            This function creates a new window using the `tk.Toplevel()` method and sets its title to "Перевести деньги".
            The window size is set to 400x300 pixels using the `geometry()` method.
            The function then creates several labels and entry fields using the `tk.Label()` and `tk.Entry()` methods
            to collect information about the transfer.
            - `from_label` is a label for the "Откуда" field.
            - `from_entry` is an entry field for entering the source of the transfer.
            - `to_label` is a label for the "Куда" field.
            - `to_entry` is an entry field for entering the destination of the transfer.
            - `amount_label` is a label for the "Сумма" field.
            - `amount_entry` is an entry field for entering the amount to be transferred.
            Finally, the function creates a transfer button using the `tk.Button()` method with the text "Перевести"
            and a command that calls the `self.transfer_money()` method with the values entered in the entry fields.
            This function does not have any parameters.
            It does not return any values.
            """
            transfer_window = tk.Toplevel(self.root)
            transfer_window.title("Перевести деньги")
            transfer_window.geometry("400x300")

            from_label = tk.Label(transfer_window, text="Откуда", font=("Arial", 18))
            from_label.pack(pady=10)

            from_entry = tk.Entry(transfer_window, font=("Arial", 14))
            from_entry.pack(pady=5)

            to_label = tk.Label(transfer_window, text="Куда", font=("Arial", 18))
            to_label.pack(pady=10)

            to_entry = tk.Entry(transfer_window, font=("Arial", 14))
            to_entry.pack(pady=5)

            amount_label = tk.Label(transfer_window, text="Сумма", font=("Arial", 18))
            amount_label.pack(pady=10)

            amount_entry = tk.Entry(transfer_window, font=("Arial", 14))
            amount_entry.pack(pady=5)

            transfer_button = tk.Button(
                transfer_window,
                text="Перевести",
                command=lambda: self.transfer_money(from_entry.get(), to_entry.get(), amount_entry.get()),
            )
            transfer_button.pack(pady=10)

        def deposit_money(self, card_number, amount):
            # Use the card_database_manager to find the card with the given card number
            card = find_card(card_number)

            if card:
                # Convert the amount to a decimal
                amount = decimal.Decimal(amount)

                # Update the card balance by adding the deposited amount
                card["balance"] += amount

                # Display a success message
                self.display_message("Деньги успешно внесены", "green")

                # Update the card balance in the database
                card_database_manager.update_card_balance(card_number, amount)
            else:
                # Display an error message if the card is not found
                self.display_message("Карта не найдена", "red")

        def withdraw_money(self, card_number, amount):
            # Use the card_database_manager to find the card with the given card number
            card = find_card(card_number)

            if card:
                # Check if the card has enough balance to withdraw the requested amount
                if card["balance"] >= float(amount):
                    # Update the card balance by subtracting the withdrawn amount
                    card["balance"] -= float(amount)

                    # Display a success message
                    self.display_message("Деньги успешно сняты", "green")

                    # Update the card balance in the database
                    card_database_manager.update_card_balance(card_number, -float(amount))
                else:
                    # Display an error message if the card balance is insufficient
                    self.display_message("Недостаточно средств", "red")
            else:
                # Display an error message if the card is not found
                self.display_message("Карта не найдена", "red")

        def transfer_money(self, from_card, to_card, amount):
            # Use the card_database_manager to find the "from" card and the "to" card
            from_card = find_card(from_card)
            to_card = find_card(to_card)

            if from_card and to_card:
                # Check if the "from" card has enough balance to transfer the requested amount
                if from_card["balance"] >= float(amount):
                    # Update the "from" card balance by subtracting the transferred amount
                    from_card["balance"] -= float(amount)

                    # Update the "to" card balance by adding the transferred amount
                    to_card["balance"] += float(amount)

                    # Display a success message
                    self.display_message("Деньги успешно переведены", "green")

                    # Update the "from" card balance in the database
                    card_database_manager.update_card_balance(from_card["number"], -float(amount))

                    # Update the "to" card balance in the database
                    card_database_manager.update_card_balance(to_card["number"], float(amount))
                else:
                    # Display an error message if the "from" card balance is insufficient
                    self.display_message("Недостаточно средств", "red")
            else:
                # Display an error message if either the "from" card or the "to" card is not found
                self.display_message("Одна из карт не найдена", "red")

    def start(self):
        self.interface.start()


atm = ATM()
atm.start()
