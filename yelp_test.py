import unittest
import yelp

'''
Some test cases for yelp.py
'''

class Test_Part_1(unittest.TestCase):
	def setUp(self):
		self.busi_list = yelp.get_business_list(term='Japanese restaurants',
											location='San Francisco', count=30)

	def test_1_1_type(self):
		self.assertEqual(type(self.busi_list), list)

	def test_1_2_length(self):
		self.assertEqual(len(self.busi_list), 30)

	def test_1_3_contents(self):
		busi = self.busi_list[0]
		self.assertEqual(busi.business_name, "Ryoko's")
		self.assertEqual(busi.yelp_id, 'mydKjdG8gJOcRQ9cZwkQpQ')
		self.assertEqual(busi.url, 'https://www.yelp.com/biz/ryokos-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw')
		self.assertEqual(busi.review_count, 3000)
		self.assertEqual(busi.city, 'San Francisco')
		self.assertEqual(busi.phone_number, '+14157751028')
		self.assertEqual(busi.rating, 4.0)
		self.assertEqual(busi.price, 2)
		self.assertEqual(busi.address, '619 Taylor St')
		self.assertEqual(busi.category, ['Sushi Bars', 'Japanese', 'NULL'])

	def test_1_4_get_business_info(self):
		busi = self.busi_list[1]
		correct_info = ['KUSAKABE', 'U0GqpXzcIDlad7vQHbB63Q', 'San Francisco', '+14157570155', 902, 4.5, 4, 'https://www.yelp.com/biz/kusakabe-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw', '584 Washington St']
		self.assertEqual(busi.get_business_info(), correct_info)

	def test_1_5_get_category_info(self):
		busi = self.busi_list[1]
		correct_info = ['Sushi Bars', 'Japanese', 'NULL']
		self.assertEqual(busi.get_category_info(), correct_info)



if __name__ == '__main__':
	unittest.main()