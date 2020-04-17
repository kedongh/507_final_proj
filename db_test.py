import unittest
import db

'''
Some test cases for db.py
'''

class Test_Part_1(unittest.TestCase):
	def test_1_two_null(self):
		command = ['NULL', 'NULL', 'rating', 'top', '5']
		result = db.process_command(command)
		self.assertEqual(len(result), 5)
		self.assertEqual(result, [('Alsip', 5.0), ('Chelsea', 5.0), ('Grosse Pointe Park', 5.0), ('Hermosa Beach', 5.0), ('Hingham', 5.0)])

	def test_2_term_null(self):
		command = ['NULL', 'San Francisco', 'rating', 'top', '10']
		result = db.process_command(command)
		self.assertEqual(len(result), 10)
		self.assertEqual(result, [('Presidio Kebab', 'San Francisco', 25, 5.0, 2, '3277 Sacramento St', 'https://www.yelp.com/biz/presidio-kebab-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Mr Dragon', 'San Francisco', 19, 5.0, 0, '3914 Judah St', 'https://www.yelp.com/biz/mr-dragon-san-francisco-2?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Ichido', 'San Francisco', 120, 5.0, 4, '50 Apparel Way', 'https://www.yelp.com/biz/ichido-san-francisco-6?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Rose Indian Cuisine', 'San Francisco', 104, 5.0, 2, '1386 9th Ave', 'https://www.yelp.com/biz/rose-indian-cuisine-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Istanbul Modern SF', 'San Francisco', 79, 5.0, 3, '', 'https://www.yelp.com/biz/istanbul-modern-sf-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Breakfast Little', 'San Francisco', 141, 5.0, 1, '3224 1/2 22nd St', 'https://www.yelp.com/biz/breakfast-little-san-francisco-2?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Early To Rise', 'San Francisco', 185, 5.0, 3, '1098 Jackson St', 'https://www.yelp.com/biz/early-to-rise-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Sunset29 BBQ', 'San Francisco', 34, 5.0, 0, '103 Horne Ave', 'https://www.yelp.com/biz/sunset29-bbq-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Bayview Bistro', 'San Francisco', 2, 5.0, 0, '4101 3rd St', 'https://www.yelp.com/biz/bayview-bistro-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Twisted St. Cafe', 'San Francisco', 12, 5.0, 0, '2320 Lombard St', 'https://www.yelp.com/biz/twisted-st-cafe-san-francisco?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw')])

	def test_3_location_null(self):
		command = ['Chinese', 'NULL', 'price', 'top', '3']
		result = db.process_command(command)
		self.assertEqual(len(result), 3)
		self.assertEqual(result, [('Beverly Hills', 4.0), ('Alhambra', 3.0), ('Arcadia', 3.0)])

	def test_4_both_not_null(self):
		command = ['Japanese', 'Seattle', 'rating', 'bottom', '5']
		result = db.process_command(command)
		self.assertEqual(len(result), 5)
		self.assertEqual(result, [('I Love Sushi On Lake Union', 'Seattle', 664, 3.5, 2, '1001 Fairview Ave N', 'https://www.yelp.com/biz/i-love-sushi-on-lake-union-seattle-2?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Fuji Sushi', 'Seattle', 452, 3.5, 2, '520 S Main St', 'https://www.yelp.com/biz/fuji-sushi-seattle?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Gokan Sushi & Katsu House', 'Seattle', 298, 3.5, 2, '954 E Union St', 'https://www.yelp.com/biz/gokan-sushi-and-katsu-house-seattle?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									("Musashi's", 'Seattle', 281, 3.5, 2, '512 S King St', 'https://www.yelp.com/biz/musashis-seattle-3?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw'),
									('Japonessa Sushi Cocina', 'Seattle', 4628, 4.0, 2, '1400 1st Ave', 'https://www.yelp.com/biz/japonessa-sushi-cocina-seattle?adjust_creative=M0e5k4FmE4KKyc5kjSTUsw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=M0e5k4FmE4KKyc5kjSTUsw')])

if __name__ == '__main__':
	unittest.main()