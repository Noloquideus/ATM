from psycopg2 import Error

from database import connect_to_database
from logger import configure_logger, logger


# Configure the logger
configure_logger()


class UserDatabaseManager:
    @staticmethod
    def find_user(login):
        """
        Finds a user in the database by login.
        Args:
            login (str): The login of the user to find.
        Returns:
            dict or None: If the user is found, a dictionary containing the user's data. If the user is not found, None.
        """
        try:
            # Create a cursor object to execute SQL queries
            cursor = connect_to_database().cursor()

            # Form and execute an SQL query to find a user by login
            query = f"SELECT * FROM users WHERE login = '{login}'"
            cursor.execute(query)

            # Get the results of the query
            result = cursor.fetchone()

            # If the user is found, return their data
            if result:
                user_id, uid, first_name, surname, user_login, user_password = result
                user_data = {
                    "id": user_id,
                    "uid": uid,
                    "first_name": first_name,
                    "surname": surname,
                    "login": user_login,
                    "password": user_password,
                }

                # Log the successful execution of the query
                logger.info(f"Query executed successfully. User data retrieved: {user_data}")

                return user_data

            # If the user is not found, return None
            return None

        except (Exception, Error) as error:
            # Log the error
            logger.error(f"Error executing SQL query: {error}")
