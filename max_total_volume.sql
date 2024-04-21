SELECT
	block_no, MAX(total_volume) AS total_volume
FROM
	(
        SELECT
            block_no, SUM(amount) AS total_volume
        FROM
            Transactions
        WHERE
            ts >= strftime('%s', '2024-01-01 00:00:00') AND
            ts <= strftime('%s', '2024-01-01 00:30:00')
        GROUP BY
            block_no
	);