# -*- coding: utf-8 -*-
import MySQLdb
import CrawlerTools as cTools
import DatabaseTools as dbTools

# Manually set system default encoding to utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

target_url = "http://list.jd.com/list.html?cat=9987,653,655"

class Mobile:
	def __init__(self, info):
		self.name = info[0]
		self.code = info[1]
		self.para = info[2]

def add_product(cur, mobile):
	dbTools.insert_values_into_table(cur, 'JDMobile_mobile', ['name', 'code'], [mobile.name, mobile.code])
	p_PID = dbTools.get_PID(cur, mobile.code)
	print 'Downloading product\t', str(p_PID), '\t... ...\t',
	for para in mobile.para:
		dbTools.insert_values_into_table(cur, 'JDMobile_parameter', ['name', 'value', 'p_PID_id'], [para[0], para[1], int(p_PID)])
	print 'Success'

def update_product(cur, mobile, p_PID):
	print 'Updating product\t', str(p_PID), '\t... ...\t',
	dbTools.update_values_of_table(cur, 'JDMobile_mobile', 'name', mobile.name, 'code', mobile.code)
	for para in mobile.para:
		if dbTools.check_if_parameter_exists(cur, 'JDMobile_parameter', para[0], int(p_PID)) == "not exist":
			dbTools.insert_values_into_table(cur, 'JDMobile_parameter', ['name', 'value', 'p_PID_id'], [para[0], para[1], int(p_PID)])
		else:
			dbTools.update_values_of_table(cur, 'JDMobile_parameter', 'value', para[1], 'name', para[0])
	print 'Success'

def main():
	''' Initialize MySQL Database '''
	con = dbTools.open_mysql()
	cur = dbTools.get_cursor(con)
	#dbTools.drop_database(cur, 'JDMobile')
	#dbTools.create_database(cur, 'JDMobile', 'utf8', 'utf8_general_ci')
	dbTools.use_database(cur, 'JDMobile')
	#dbTools.truncate_table(cur, 'JDMobile_parameter')
	#dbTools.truncate_table(cur, 'JDMobile_mobile')

	''' Crawling '''
	page_num = cTools.get_page_num(target_url)
	for num in range(4, 5):
		page_url = target_url + "&page=" + str(num)
		prod_ids = cTools.get_product_ids(page_url)
		for prod_id in prod_ids:
			try:
				mobile = Mobile(cTools.get_product_information(prod_id))
				p_PID = dbTools.get_PID(cur, mobile.code)
				if p_PID == 'not exist':
					add_product(cur, mobile)
				else:
					update_product(cur, mobile, p_PID)
			except:
				error_msg = sys.exc_info()
				print 'Fail', error_msg[0], ':', error_msg[1]
	
	dbTools.close_cursor(cur)
	dbTools.commit_close_mysql(con)
				
if __name__ == "__main__":
	main()
