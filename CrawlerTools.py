# -*- coding: utf-8 -*-
import re, urllib2, HTMLParser, json

# Match regular expression from url; Return a 1D-list
def match_regex(pattern, url):
	html_parser = HTMLParser.HTMLParser()						# Initialize HTML Parser
	match_list = []									# Initialize match list for return
	src = urllib2.urlopen(url)							# Open the url
	html = src.read()								# Read the html data from the source
	charset_pat = re.compile(r'charset=(.*?)"', re.I|re.S)				# Compile the pattern of the charset of the page
	charset = charset_pat.findall(html)[0]						# Find the charset of the page
	charset.replace('"', '')							# Eliminate " in some case (e.g. "gbk)
	if charset == 'gbk' or charset == 'GBK':					# Replace gbk with gb18030 which is a more complete set
		charset = 'gb18030'
	html = html.decode(charset).encode('utf8')					# Decode the html with its charset and encode it with utf-8
	html = html_parser.unescape(html)						# Unescape the html with HTML Parser to elimnate the messy code (e.g. &nbsp)
	com = re.compile(pattern, re.I|re.S)						# Compile the pattern with re.I [case-insensitive] and re.S [Dot'.' represents all]
	match_list = com.findall(html)							# Return all non-overlapping matches of pattern in the source as a list of string(s)
	src.close()									# Close the url
	return match_list								# Return match list
	
# Get the number of pages from url; Return an integer
def get_page_num(url):
	page_num = match_regex(ur'共<b>(.*?)</b>页', url)
	return int(page_num[0])

# Get the product IDs from url; Return a 1D-list
def get_product_ids(url):
	prod_ids = match_regex('<a target="_blank" href="//item.jd.com/(.*?).html".*?>', url)
	return prod_ids

# Get the prices of a product from its ID; Return a 1D-list[price_jd, price_mk]
def get_prices(prod_id):
	prices = []									# prices = [price_jd, price_mk]
	prices_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + str(prod_id)		# Build the page url
	jsonString = urllib2.urlopen(prices_url).read()					# read the html data from the url
	jsonObject = json.loads(jsonString.decode())					# decode the json code from the html and store it as json object (python dict)
	try:										# Find the JD price and the market price from the json object
		price_jd = jsonObject[0]["p"]
		price_mk = jsonObject[0]["m"]
	except:										# If the price url failed and json object is invalid
		price_jd = ''
		price_mk = ''
	prices.append(price_jd)								# Add the prices into return list
	prices.append(price_mk)
	return prices

# Get the url of the picture of a product from its ID; Return a string
def get_product_img_url(prod_id):
	prod_url = 'http://item.jd.com/' + str(prod_id) + '.html'
	img_url_small = match_regex('img-hover.*?src=(.*?) data-url', prod_url)[0]
	img_url = str(img_url_small).replace('\'//', '').replace('\'', '').replace('/n5/s54x54_', '/imgzone/')
	return img_url.encode('utf8')

# Get the details of a product from its ID; Return a 3D-list (info_list = [name, code, [[name, value], [name, value], ...]])
def get_product_information(prod_id):
	info_list = []												# info_list = [Name, Code, [Parameter]]
	p_list = []												# p_list = [[names, values], ...]
	prod_url = 'http://item.jd.com/' + str(prod_id) + '.html'						# Build the product url
	parameter_lists = match_regex('<ul class="parameter\d p-parameter-list">(.*?)</ul>', prod_url)	# Get the parameter lists from product url
	for parameter_list in parameter_lists[::-1]:								# For each parameter list
		parameter_pattern = re.compile('title=.*?>(.*?)<', re.I|re.S)					# parameters = ['name：value', ...]
		parameters = parameter_pattern.findall(parameter_list)						# Get the parameters from the list
		for parameter in parameters:									# For each parameter parameter = 'name：value'
			para = parameter.replace('-', '').split('：')						# Turn the parameter to a list para = ['name', 'value']
			p_list.append([para[0], para[1]])							
			
	prices = get_prices(prod_id)
	p_list.append(['京东价格', prices[0]])
	p_list.append(['市场价格', prices[1]])									# Add the prices of the product to p_list
	p_list.append(['图片网址', get_product_img_url(prod_id)])						# Add the img url of the product to p_list

	info_list.append(p_list[0][1])										# Get Name
	info_list.append(p_list[1][1])										# Get Code
	info_list.append(p_list[2:])										# Get Parameters
	return info_list
