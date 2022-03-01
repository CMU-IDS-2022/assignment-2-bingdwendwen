# Restaurant Incubator
 
## Project Goals
Our project aims to assist entrepreneurs who want to open a restaurant in the United States by giving them recommendations on the **Where**, **When**, **What**, **How** questions:
- **Where**: Where should I locate my business?
- **When**: When should my restaurant open? 
- **What**: What category of cuisines should I choose?
- **How**: How can I add other attributes to accelerate my business? 

Considering 92% of consumers now read online reviews before purchasing, a positive presence on Yelp can give a small business a huge advantage. Thus, our project uses Yelp Dataset(https://www.yelp.com/dataset), and we choose **stars** as out objective, specifcally, we want to give audience recommendations that could maximize the values of stars. 

<!-- Our project use Yelp data to help a user to see the stars in different states/provinces in North America. The user can choose the **state** and **days** in which he/she want to open a restaurant. Then the project will show the rating of different categories in selected state and days. At last the user needs to decide which **state.** he/she want to open the restaurant. Then we use a **DecisionTree Regression** to find the features that infuluence the rate of the stars. The user can decide whether to invest on these features to provide better services. -->

## Quick Tour for Our Project
**The project is made by four parts:**
Our project aims to assist entrepreneurs who want to open a restaurant in 
1. A summary of the relationship between the mean of stars and review counts.
2. A bar chart shows a relationship between state and stars. 
3. Choose state and days, find a relationship between category and stars.
4. Explore attribute recommendations with the Decision Tree regression model.
5. *hint: we also have checkbox to show the data*


![](imagefiles/overview.jpg)

## Design
We use several charts to help the user understand what they are seeing
The following gifs show how to use these filters:
### 1. Relationship between review counts and stars 
This graph is intended to show if any outliers are caused by the lack of review counts. If the restaurant is just open, the reviews are likely made by the friends or relatives of the business owner, which causes biased data. From the graph, we can see the vias didn't appear in this dataset we choose. 
### 2. Relationship between state and stars. 
From this graph, the user can see a distribution of rating preferences in each state. Specifically, if the user has decided to start a business in GA, we can see the average rating there is 0.1 lower than average, thus the user has a rough measurement in the future. If in the future, his/her restaurant got a star of 3.5, although it is below the country average, the restaurant did a good job in the GA.
By hovering on each bar, the user can see the statistics of each state. Each bar is colored in different intensities, if the color is deep blue, it means the states have sufficient data, thus the statistics are more reliable; else, if light blue, the data counts are smaller, thus the statistic is less reliable.
![](imagefiles/choose_state.png)
### 3. Choose state and days, find a relationship between category and stars.
Here, the user has decided where he wants to open his business, and he can multi-choose the days the restaurant opens. After the user decided the state and the days, the user can see the popularity distributions of different categories of cuisines. 
Users can click on the left chart to choose multiple categories by pressing **SHIFT** and clicking. The right line chart will show what you selected in the left chart.
For example, from the gif, we can see French, Korean and Indian cuisines are easier to get high ratings in the state of BC. 
![filter_data](imagefiles/filter_data.gif)

### 4. Explore attribute recommendations. 
In this step, the user should have to decide the state, hours, and category of cuisines for his/her business. After the user selects those three, the program will automatically compute the data that satisfies the filters. The user can see the data by clicking "show filter data".
With the filtered data, we use a machine learning model - Decision Tree Regression - to draw the relationships between attributes with stars. The attributes contain 37 features, including latitude, longitude, freeWIFI, hasTV ... so on, that users could add to increase the popularity of his/her business. The model will compute the distribution of each feature and its importance in rating contribution. We selected the top five features for recommendations. If the user is interested in all features that have positive contributions, just click "show all features".  
![category](imagefiles/choose_category.gif)

<!-- TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices? -->

## Development

### How we process the data:
The raw data was JSON form. So we use pandas to formalize the JSON data and transfer it into a CVS file. We keep about **50,000** out of **160,000** rows data because the other part of the data is not related to restaurants. And also about **14,000** rows data are from restaurants that are marked as "not_open", so we also drop them. Finally, we have about 36,000 rows of data.

 For **days**, these data originally stand for the time scope of opening. We transfer these data into **0/1** forms(1 for open that day,0 otherwise)

And the category data are originally multiple tags about this restaurant, like *"Salad, Soup, Sandwiches, Delis, Restaurants, Cafes, Vegetarian"*. We simplify the category to one word, like 'vegetarian'. We use the function category() to filter all the tags. This function is not precise since we don't classify all the tags. So you will see lots of "Other" categories in our charts. The category list is actually from Yelp's official website:
https://blog.yelp.com/businesses/yelp_category_list/#section21


@norawangyining(**Yining Wang**) 
- Makes the **DecisonTree Regression Model** and the first two charts.
- Roughly 16 hours in total. Spent most of the time in data selection, data cleaning, and model training.

@JackInCMU(**Jiaxiang Wu**) 
- Makes the **Interactive charts** and filter function.
- Spent about 15 hours in total, the interactive charts took the most time

**WriteUP** was finished by the entire team.
<!-- TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time? -->

## Success Story
### @JackInCMU(**Jiaxiang Wu**) 

It's very hard to find a good dataset. We spent about two hours then we found a dataset that was acceptable. Also, the dataset has lots of N/A and we have to clean the dataset first. It was tough for me to deal with the 160,000 rows of data at first. I can imagine how hard would it be when it comes to real industry needs.

On the other hand, it's important to read the official documents of any library. These documents can help you understand any function in a short time. And also, thanks to StackOverflow, it's a good website.

### @norawangyining(**Yining Wang**) 
Add to Jiaxiang's comments, when we are choosing the datasets, we found interesting datasets are often not free. What I mean by interesting, is that the dataset can solve real-world unsolved problems.
From our analysis, it is interesting to find that foreign dishes are quite popular in the United States. Especially for Indian and Korean dishes, they usually have higher ratings than the local American dishes. 

<!-- TODO:  **A success story of your project.** Describe an insight or discovery you gain with your application that relates to the goals of your project. -->
