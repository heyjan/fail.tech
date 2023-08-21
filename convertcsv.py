import sqlite3
import pandas as pd

try:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv('unfriendtech-2023-08-21.csv')
    print("CSV file successfully read.")

    try:
        # Create an SQLite database and save the DataFrame to it
        conn = sqlite3.connect('mydatabase.db')

        # Try writing data to the database
        df.to_sql('data', conn, if_exists='replace', index=False)
        print("Data successfully written to the SQLite database.")

    except sqlite3.Error as e:
        print(f"An SQLite error occurred: {e}")

    finally:
        # Close the connection (important!)
        conn.close()

except FileNotFoundError:
    print("Error: CSV file not found.")
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
except pd.errors.ParserError:
    print("Error: Problem occurred during parsing the CSV.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
