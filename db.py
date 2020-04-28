import sqlite3

DB_NAME = 'yelp.sqlite'

def process_command(command):
	''' Fetch the data (records) from the database according to the given command.

	Args:
		command (list): A list of command parameters.

	Return:
		result (list): A list of tuples representing records that match the query.
	'''

	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()
	query = generate(command)
	result = cursor.execute(query).fetchall()
	connection.close()

	return result


def generate(command):
	''' Generate query according to the given command.

	Args:
		command (list): A list of command parameters.
	Returns:
		query (str): A query string.
	'''
	category, location, order, by, limit = command

	if category == 'NULL':
		where = ''
	else:
		where = "'" + category + "'" + ' IN (category_info.category_1, category_info.category_2, category_info.category_3)'

	if location == 'NULL':
		items = 'city, AVG(' + order + ')'
		order = 'AVG(' + order + ')'
		group = 'GROUP BY city'
	else:
		items = 'business_name, city, review_count, rating, price, address, url'
		group = ''
		if where != '':
			where += " AND city ='" + location + "'"
		else:
			where = "city='" + location + "'"

	by = 'DESC' if by == 'top' else ''
	if where:
		where = 'WHERE ' + where
	query = 'SELECT ' + items + ' ' + \
			'FROM business_info ' + \
			'JOIN category_info ON business_info.yelp_id = category_info.yelp_id ' + \
			where + ' ' + \
			group + ' ' + \
			'ORDER BY ' + order + ' ' + by + ' ' + \
			'LIMIT ' + limit
	return query


def load_help_text():
    with open('db_help.txt') as f:
        return f.read()


if __name__ == '__main__':
	command = ['Chinese', 'San Francisco', 'rating', 'top', '10']
	print(process_command(command))
