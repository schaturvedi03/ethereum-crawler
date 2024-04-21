# Ethereum Crawler
The Ethereum Crawler is a Python script that retrieves Ethereum transactions within a specified block range and stores them in an SQLite database. It utilizes the Web3.py library to interact with the Ethereum blockchain.

## Prerequisites

- Python 3.x
- Web3.py library
- SQLite

## Installation

1. Clone the repository or download the script files.

2. Install the required dependencies using pip:

   ```
   pip install web3
   ```
3. Install SQLite3 if it's not already installed on your system:
   - For Linux:
     - SQLite is usually pre-installed on most Linux distributions. If it's not available, you can install it using your distribution's package manager. For example:
       - On Ubuntu or Debian: `sudo apt-get install sqlite3`
       - On Fedora or CentOS: `sudo dnf install sqlite3`
4. Verify the installation of SQLite3 by running the following command in a terminal or command prompt:

   ```
   sqlite3 --version
   ```

   If SQLite3 is installed correctly, it will display the version number.

## Usage

To run the Ethereum Crawler script, use the following command:

```
python block_crawler.py <rpc-endpoint> <path-to-db> <range-of-block>
```

The script expects the following command-line arguments:

1. `<rpc-endpoint>`: The RPC endpoint URL for Ethereum, e.g., `https://eth.llamarpc.com`.
2. `<path-to-db>`: The path to the SQLite database file where the transactions will be stored, e.g., `transactions.db`.
3. `<range-of-block>`: The range of blocks to fetch transactions from, in the format `start-end`, e.g., `1000-1500`.

Example usage:

```
python block_crawler.py https://eth.llamarpc.com transactions.db 1000-1500
```

This command will fetch Ethereum transactions from blocks 1000 to 1500 (inclusive) using the RPC endpoint and store them in the `transactions.db` SQLite database file.

- A database file containing a `Transactions` table with the following columns:
  - `hash`: The transaction hash associated with each transaction. This is the primary key of the table.
  - `block_no`: The block number associated with each transaction.
  - `amount`: The transaction amount.
  - `ts`: The timestamp of the transaction.


The `max_total_volume.sql` file contains an SQL query that retrieves the block number with the maximum total volume of transactions within a specific time range. The query is designed to be executed in the SQLite3 command-line interface.

To execute the query and retrieve the block number with the maximum total volume, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the directory where the `max_total_volume.sql` file is located.

3. Run the following command to start the SQLite3 command-line interface and connect to your database file:

   ```
   sqlite3 transactions.db
   ```

4. Once connected to the database, execute the query by running the following command:

   ```
   .read max_total_volume.sql
   ```

   This command will read and execute the SQL query from the `max_total_volume.sql` file.

5. The query will retrieve the block number with the maximum total volume of transactions within the specified time range (from '2024-01-01 00:00:00' to '2024-01-01 00:30:00').

6. The result will be displayed in the SQLite3 command-line interface, showing the block number (`block_no`) and the corresponding maximum total volume (`total_volume`).

## Query Explanation

The SQL query in the `max_total_volume.sql` file consists of the following parts:

1. The outer `SELECT` statement retrieves the `block_no` and the maximum `total_volume` from the subquery.

2. The subquery (`SELECT` statement inside the parentheses) calculates the total volume of transactions for each block within the specified time range.
   - It selects the `block_no` and calculates the sum of `amount` values, aliased as `total_volume`.
   - The `WHERE` clause filters the transactions based on the `ts` (timestamp) column, considering only the transactions between '2024-01-01 00:00:00' and '2024-01-01 00:30:00'.
   - The `GROUP BY` clause groups the transactions by `block_no`, allowing the calculation of the total volume for each block.

3. The outer `SELECT` statement then retrieves the `block_no` and the maximum `total_volume` from the subquery result.

## Functionality

The Ethereum Crawler script performs the following steps:

1. Validates the provided command-line arguments:
   - Checks if the RPC endpoint URL is valid.
   - Checks if the database file path is accessible.
   - Parses and validates the block range.

2. Initializes the SQLite database by creating the necessary tables.

3. Fetches the transactions from the specified block range using the provided RPC endpoint.

4. Stores the retrieved transactions in the SQLite database.

If any of the validations fail or if the required command-line arguments are missing, the script displays appropriate error messages and exits with a non-zero status code.

## Configuration

The script uses the following configuration:

- The `schema.sql` file contains the SQL statements to create the necessary tables in the SQLite database. You can modify this file to change the database schema if needed.

## Error Handling

The script includes error handling for the following scenarios:

- Missing or invalid command-line arguments.
- Invalid RPC endpoint URL.
- Inaccessible database file path.
- Invalid block range format or range.

If any of these errors occur, the script will display an appropriate error message and exit with a non-zero status code.

## License

This project is licensed under the [Apache License](LICENSE).
