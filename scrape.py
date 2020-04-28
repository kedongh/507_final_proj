from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'UMSI 507 final project',
    'From': 'kedongh@umich.edu',
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}


def get_info_from_url(url):
	''' Scrape the info from the given url.

	Args:
		url (str): A string web link to scrape.

	Returns:
		pics (list): A list of 3 picture links.
		reviews (list): A list of 3 recent reviews
	'''
	response = requests.get(url, headers=headers).text
	soup = BeautifulSoup(response, 'html.parser')

	all_pics_items = soup.find_all('div', class_='lemon--div__373c0__1mboc photo-header-media__373c0__1fmzx photo-header-media--4__373c0__1CGN1 display--inline-block__373c0__2de_K border-color--default__373c0__2oFDT')
	all_revs_items = soup.find_all('p', class_='lemon--p__373c0__3Qnnj text__373c0__2pB8f comment__373c0__3EKjH text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_')

	pics = ''
	reviews = ''

	for i in range(min(1, len(all_pics_items))):
		pic_item = all_pics_items[i].find('img', class_='lemon--img__373c0__3GQUb')
		pics = pic_item['src']

	for i in range(min(1, len(all_revs_items))):
		rev_item = all_revs_items[i].find('span', class_='lemon--span__373c0__3997G')
		reviews = rev_item.text.strip()

	return pics, reviews


if __name__ == '__main__':
	print(get_info_from_url('https://www.yelp.com/biz/sam-wo-restaurant-san-francisco-3?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'))
