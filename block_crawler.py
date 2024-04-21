import sys
import os
import re
from web3 import Web3
import sqlite3

def initialize_db(db_path, schema_file='schema.sql'):
    """
    Initializes an SQLite database by executing the SQL statements from the provided schema file.

    This function establishes a connection to the SQLite database specified by `db_path`,
    reads the SQL statements from the `schema_file`, and executes them using the SQLite cursor.
    The changes are then committed to the database, and the connection is closed.

    :param db_path: The path to the SQLite database file.
    :param schema_file: The path to the SQL file containing the database schema (default: 'schema.sql').
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(schema_file, 'r') as file:
        schema = file.read()
        c.executescript(schema)

    conn.commit()
    conn.close()


def fetch_transactions(start, end, db_path, endpoint):
    """
    Retrieves Ethereum transactions from the specified block range and stores them in an SQLite database.

    This function connects to the Ethereum network using the provided JSON-RPC endpoint, iterates over the blocks
    within the given range, and fetches the transactions for each block. The retrieved transaction data, including
    the transaction hash, block number, value (in Ether), and block timestamp, is then inserted into the specified
    SQLite database.

    If the Ethereum network cannot be reached or an error occurs during the process, an appropriate message is printed.

    :param start: The starting block number (inclusive) of the range to fetch transactions from.
    :param end: The ending block number (inclusive) of the range to fetch transactions from.
    :param db_path: The path to the SQLite database file where the transaction data will be stored.
    :param endpoint: The URL of the Ethereum JSON-RPC endpoint to connect to.
    """
    w3 = Web3(Web3.HTTPProvider(endpoint))
    if not w3.is_connected():
        print("Ethereum network cannot be reached")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        for block_no in range(start, end + 1):
            print(f"Parsing block {block_no}")
            block = w3.eth.get_block(block_no, True)
            for tx in block.transactions:
                # Insert transaction data into the database
                cursor.execute('INSERT OR IGNORE INTO Transactions VALUES (?, ?, ?, ?)',
                          (tx.hash.hex(), tx.blockNumber, str(w3.from_wei(tx['value'], 'ether')), block.timestamp))
            conn.commit()
            print(f"Block {block_no}: {len(block.transactions)} transactions persisted to DB.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


def is_valid_endpoint(url):
    """
    Checks if the provided URL is a valid Ethereum JSON-RPC endpoint.

    This function uses a regular expression pattern to validate the format of the given URL.
    The pattern ensures that the URL follows a specific structure expected for an Ethereum
    JSON-RPC endpoint, including the protocol (http, https, wss, or rpc), domain or IP address,
    and optional port number.

    The function returns True if the URL matches the expected pattern, indicating a valid endpoint,
    and False otherwise.

    :param url: The URL string to be validated as an Ethereum JSON-RPC endpoint.
    :return: A boolean value indicating whether the provided URL is a valid Ethereum JSON-RPC endpoint.
    """

    url_pattern = re.compile(
        r'^(?:http|wss|rpc)s?://'  # Protocol
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # Port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_pattern, url) is not None


def is_valid_db_path(db_path):
    """
    Checks if the provided database file path is valid for writing.

    This function performs the following validations on the given `db_path`:
    1. Checks if the `db_path` is a directory. If it is, the function returns False, as a directory
       is not a valid database file path.
    2. Attempts to open the file specified by `db_path` in append mode ('a'). If the file can be
       successfully opened, it means the path is valid and writable, and the function returns True.

    If an IOError occurs while opening the file, indicating that the path is not valid or accessible,
    the function returns False.

    :param db_path: The path to the database file to be validated.
    :return: A boolean value indicating whether the provided database file path is valid and writable.
             Returns True if the path is valid and writable, False otherwise.
    """
    try:
        # Check if the path is a directory
        if os.path.isdir(db_path):
            return False

        # Try opening the file in append mode
        with open(db_path, 'a'):
            pass
        return True
    except IOError:
        return False


def is_valid_blocks_range(blocks):
    """
    Validates and parses the given block range string.

    This function takes a block range string in the format "start-end" and performs the following checks:
    1. Splits the string into two parts using the '-' delimiter.
    2. Attempts to convert both parts into integers using the `int()` function.
    3. Checks if the start block number is less than or equal to the end block number.

    If the block range string is valid and passes all the checks, the function returns a tuple containing
    the start and end block numbers as integers.

    If the block range string is invalid, either due to incorrect format or invalid block numbers,
    the function returns None.

    :param blocks: The block range string in the format "start-end".
    :return: A tuple containing the start and end block numbers as integers if the block range is valid,
             or None if the block range is invalid.
    """
    try:
        start, end = map(int, blocks.split('-'))
        if start <= end:
            return start, end
    except ValueError:
        pass
    return None

if __name__ == "__main__":
    print("Welcome to Block Crawler")

    while True:
        if len(sys.argv) == 4:
            endpoint_url, db_instance, blocks = sys.argv[1], sys.argv[2], sys.argv[3]
            break
        else:
            print("Missing command line arguments")
            print("Expected <script-file> <rpc-endpoint> <path-to-db> <range-of-block>")

    # Run the Input Validation
    if not is_valid_endpoint(endpoint_url):
        print("Input endpoint URL for Ethereum is not valid %s", endpoint_url)
        sys.exit(1)

    if not is_valid_db_path(db_instance):
        print("Input database path is not accessible")
        sys.exit(1)

    block_range = is_valid_blocks_range(blocks)
    if block_range is None:
        print("Invalid block range format or range")
        sys.exit(1)

    start, end = block_range

    initialize_db(db_instance)
    fetch_transactions(start, end, db_instance, endpoint_url)
