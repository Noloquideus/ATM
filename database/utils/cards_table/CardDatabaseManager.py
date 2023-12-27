from database import connect_to_database
from logger import configure_logger


configure_logger()


def find_card(card_number):
    """
    Finds a card in the database based on the provided card number.
    :param card_number: The number of the card to be searched.
    :type card_number: int
    :return: A dictionary containing the card information if found, None otherwise.
    :rtype: dict or None
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "SELECT * FROM cards WHERE number = %s"
    cursor.execute(query, (card_number,))
    card = cursor.fetchone()

    # Checking if the card was found
    if card:
        card_info = {"id": card[0], "uid": card[1], "number": card[2], "balance": card[3]}
    else:
        card_info = None

    # Closing the database connection and returning the card information
    cursor.close()
    conn.close()
    return card_info


class CardDatabaseManager:
    @staticmethod
    def find_user_cards(user_id):
        """
        Retrieves all the cards associated with a given user ID from the database.
        Args:
            user_id (int): The ID of the user whose cards need to be retrieved.
        Returns:
            list: A list of dict-ies containing information about the user's cards. Each dict has the following keys:
                - id (int): The ID of the card.
                - uid (int): The user ID associated with the card.
                - number (str): The card number.
                - balance (float): The balance on the card.
        """
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM cards WHERE uid = %s"
        cursor.execute(query, (user_id,))
        cards = cursor.fetchall()

        # Generating a list of user cards
        user_cards = []
        for card in cards:
            card_info = {"id": card[0], "uid": card[1], "number": card[2], "balance": card[3]}
            user_cards.append(card_info)

        # Closing the database connection and returning the list of user cards
        cursor.close()
        conn.close()
        return user_cards

    @staticmethod
    def add_card(uid, number, balance):
        """
        Adds a card to the database with the given UID, number, and balance.
        Parameters:
            uid (int): The user ID associated with the card.
            number (str): The card number.
            balance (float): The initial balance of the card.
        """
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "INSERT INTO cards (uid, number, balance) VALUES (%s, %s, %s)"
        values = (uid, number, balance)
        cursor.execute(query, values)
        conn.commit()

        # Closing a database connection
        cursor.close()
        conn.close()

    @staticmethod
    def update_card_balance(card_number, amount):
        """
        Updates the balance of a card in the database.
        Parameters:
        - card_number (str): The number of the card to update.
        - amount (float): The amount to add to the card's balance.
        """
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "UPDATE cards SET balance = balance + %s WHERE number = %s"
        values = (amount, card_number)
        cursor.execute(query, values)
        conn.commit()

        # Closing a database connection
        cursor.close()
        conn.close()
