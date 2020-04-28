# 507_final_proj

The final project is to design a tiny yelp website. It allows the user to find some restaurants by setting some filters and see
a ranking or average summary of price or rating of different restaurants.

Before running the program ("app.py"), you need to check two things to guarantee the program could run successfully.
1. Several required packages.
    flask, requests, bs4, plotly, sqlite3.
2. Yelp Web API.
    It is easy to get an API key after creating an app. More details could be found in Yelp Authetication guide page.

There are two main functions and pages, search and summary.

In search page, you have to set three parameters which would be passed through API.
  - Type: The type of restaurant, like "Chinese".
  - Location: The city or specific address, like "Seattle".
  - Count: The number of restaurants, like "3".
After cliking "submit" button, you would get a comprehensive new page containing detailed infor about restaurant, including the
name, the phone number, the most recent review, the picture and so on.

In summary page, you have to set some parameters and then would get a graph.
  - Type of restaurant: Choose one from avaialable choices. There are 5 choices, "Chinese", "Japanese", "Korean", "Indian", and
    "Mexican".
  - Location: Choose one from available cities, "San Francisco", "Seattle", "New York", "Chicago", "Los Angeles" and "Las Vegas".
  - Item: There are two options, "price" or "rating".
  - order: There are two options, "top" or "bottom". "top" means the result would be shown in descending order and "bottom" means
    the result should be shown in ascending order.
