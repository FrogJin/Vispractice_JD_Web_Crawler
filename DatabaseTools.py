# -*- coding: utf-8 -*-
import MySQLdb

# Open MySQL database; Return a connect
def open_mysql():
	con = MySQLdb.Connect(host = 'localhost', user = 'root', passwd = 'root', charset = 'utf8')
	return con

# Get MySQL cursor; Return a cursor
def get_cursor(con):
	cur = con.cursor()
	return cur

# Print the version of MySQL
def print_mysql_version(cur):
	sql = "SELECT VERSION()"
	cur.execute(sql)
	print "MySQL version : {version}".format(version = cur.fetchone())

# Create or open database
def create_database(cur, db_name, db_charset, db_collate):
	sql = "CREATE DATABASE IF NOT EXISTS {name} DEFAULT CHARSET={charset} COLLATE {collate}".format(name = db_name, charset = db_charset, collate = db_collate)
	try: cur.execute(sql)
	except: pass
	
# Use database
def use_database(cur, db_name):
	sql = "USE {database}".format(database = db_name)
	cur.execute(sql)
	
# Create or open table
def create_table(cur, tb_name, tb_cont, tb_engine, tb_charset):
	sql = "CREATE TABLE IF NOT EXISTS {name} ({content}) ENGINE={engine} DEFAULT CHARSET={charset}".format(name = tb_name, content = tb_cont, engine = tb_engine, charset = tb_charset)
	try: cur.execute(sql)
	except: pass

# Get column names from table; Return a 1D-list (column_names = [name, name, ...])
def get_column_names(cur, tb_name):
	column_names = []
	sql = "SHOW COLUMNS FROM {table}".format(table = tb_name)
	cur.execute(sql)
	columns = list(cur.fetchall())						# cur.fetchall() return a 2D-tuple of all columns
	for column in columns:							# For each column in columns
		column_names.append(column[0])					# Add its first parameter (name) to column_names
	return column_names
	
# Get table; Return a 2D-list (table = [[row_data], [row_data], ...]) for print
def get_table(cur, tb_name):
	table = []
	sql = "SELECT * FROM {table}".format(table = tb_name)
	cur.execute(sql)
	table_data = list(cur.fetchall())								# cur.fetchall() return a 2D-tuple of all columns, turn it to a 2D-list
	for i in range(len(table_data)):								# For each row of data
		table.append(str(table_data[i]).replace('u\'', '\'').decode("unicode-escape"))		# Turn it to string and decode it with unicode, then add the string to table list
	return table

# Get the PID of a product from its code; Return a int(PID) or a str('not exist')
def get_PID(cur, p_code):
	sql = "SELECT PID FROM JDMobile_mobile WHERE code = '{code}'".format(code = p_code)
	try:
		cur.execute(sql)	# Get the PID if exists, else raise exception
		p_PID = int(str(cur.fetchone()).replace('(', '').replace('L,)', ''))			
		return p_PID
	except: return "not exist"

# Add a column to the table
def add_column_to_table(cur, tb_name, col_name):
	sql = "ALTER TABLE {table} ADD COLUMN {column} VARCHAR(255) DEFAULT ''".format(table = tb_name, column = col_name)
	cur.execute(sql)

# Insert a row of data into the table
def insert_values_into_table(cur, tb_name, col_name, val):
	for i in range (len(val)):
		val[i] = "'" + str(val[i]) + "'"		# Surrounding variable contents by quotes, very important!
	sql = "INSERT INTO {table}({column}) VALUES ({value})".format(table = tb_name, column = ','.join(col_name), value = ','.join(val))
	cur.execute(sql)

# Check the existence of certain parameter; Return a int (0 for not exist, 1 for exist)
def check_if_parameter_exists(cur, tb_name, name, p_PID):
	sql = "SELECT * FROM {table} WHERE name='{name}' AND p_PID_id='{PID}'".format(table = tb_name, name = name, PID = p_PID)
	return cur.execute(sql)

# Update a selected row of data in the table
def update_values_of_table(cur, tb_name, val, set_val, nm, match_nm):
	sql = "UPDATE {table} SET {value} = '{set_value}' WHERE {name} = '{match_name}'".format(table = tb_name, value = val, set_value = set_val, name = nm, match_name = match_nm)
	cur.execute(sql)

# Match Keywords; Return a 1D-list
def match_values(cur, tb_name, match_col, match_kw):
	sql = "SELECT * FROM {table} WHERE MATCH(match_column) AGAINST(match_keyword)".format(table = tb_name, match_column = ','.join(match_col), match_keyword = ' '.join(match_kw))
	try:
		cur.execute(sql)
		return list(cur.fetchall())
	except: return "not exist"

# Delete all the data in the table
def truncate_table(cur, tb_name):
	sql = "DELETE FROM {table}".format(table = tb_name)
	cur.execute(sql)
	sql = "ALTER TABLE {table} AUTO_INCREMENT = 1".format(table = tb_name)
	cur.execute(sql)

# Drop table if exists
def drop_table(cur, tb_name):
	sql = "DROP TABLE IF EXISTS {table}".format(table = tb_name)
	try: cur.execute(sql)
	except: pass

# Drop database if exists
def drop_database(cur, db_name):
	sql = "DROP DATABASE IF EXISTS {database}".format(database = db_name)
	try: cur.execute(sql)
	except: pass

# Close MySQL database
def close_cursor(cur):
	cur.close()

# Commit and close the database
def commit_close_mysql(con):
	con.commit()
	con.close()
