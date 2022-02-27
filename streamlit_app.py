from turtle import color
from typing import Tuple
from xml.dom.minidom import Element

from numpy import sort
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
# pip install -U scikit-learn scipy matplotlib

daylist = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
st.title("Let's analyze some Yelp Restaurant Business Data.")

def getCategory(x):
    x = x.lower()
    if "american" in x:
        return "American"
    elif "chinese" in x:
        return "Chinese"
    elif "thai" in x:
        return "Thai"
    elif "mexican" in x:
        return "Mexican"
    elif "indian" in x:
        return "Indian"
    elif "italian" in x:
        return "Italian"
    elif "french" in x:
        return "French"
    elif "japanese" in x:
        return "Japanese"
    elif "korean" in x:
        return "Korean"
    elif "vietnamese" in x:
        return "Vietnamese"
    else:
        return "Other"
    

@st.cache  # add caching so we load the data only once
def load_data():
    business_path = "yelp_restaurant.csv"
    df = pd.read_csv(business_path, low_memory=False)
    df = df[df['is_open']==1]
    df['stars'] = pd.to_numeric(df['stars'])
    df['review_count'] = pd.to_numeric(df['review_count'])
    for day in daylist:
        df[day+'_avaliable'] = df[day].apply(lambda x : False if pd.isna(x) else True)
    df['category'] = df['categories'].apply(getCategory)
    return df


@st.cache
def get_slice(df,state,days):
    labels = pd.Series([True] * len(df), index=df.index)
    if state:
        labels &= df['state'].apply(lambda x : True if x==state else False)
    if days:
        for day in days:
            labels &= df[day+'_avaliable'] 
    return labels

df = load_data()

if st.checkbox("show raw data"):
    st.write(df[:50])

st.header("This is the summary of mean of stars and review count")
review_count_chart = alt.Chart(df).mark_line().encode(
    x=alt.X("review_count", scale=alt.Scale(zero=False), sort="-x"),
    y=alt.Y("mean(stars)", scale=alt.Scale(zero=False)),
    color = 'count(stars)',
).properties(
    width=800, height=400
).interactive()

st.write(review_count_chart)

st.header("This is the mean of stars in different states/provinces")
state_review_chart = alt.Chart(df).mark_bar(color="lightblue").encode(
    x=alt.X("state", scale=alt.Scale(zero=False), sort="-x"),
    y=alt.Y("mean(stars)", scale=alt.Scale(zero=False), title="Mean of stars"),
    color = 'count(stars)',
    tooltip = ['count(stars)','median(stars)', 'max(stars)', 'min(stars)' ]
).properties(
    width=800, height=400
)

aggregates = alt.Chart(df).transform_aggregate(
    mean='mean(stars)',
    median = 'median(stars)'
).transform_fold(
    ['mean','median']
).mark_rule(size = 3).encode(
    y='value:Q',
    color=alt.Color(
        'key:N',
        scale=alt.Scale(
            domain=['mean', 'median'],
            range=['red', 'green'])
    )
)

st.write(state_review_chart + aggregates)

st.write('choose the state and hour you prefer:')
option_cols = st.columns(2)
with option_cols[0]:
    stateOption = st.selectbox(
        'state',
        df['state'].unique()
    )

with option_cols[1]:
    daysOption = st.multiselect(
        'days',
        daylist
    )

    

slices= get_slice(df,stateOption,daysOption)
category_selector = alt.selection_multi(fields=['category'])
st.write("The sliced dataset contains {} elements ({:.1%} of total).".format(slices.sum(), slices.sum() / len(df)))
hist_chart_selected = alt.Chart(df[slices],title="sliced data from filter").mark_bar(tooltip=True).encode(
    alt.Y('category', sort="y"),
    alt.X('mean(stars)'),
    tooltip = ['count(stars)'],
    color=alt.condition(category_selector, 'mean(stars)', alt.value('lightgray')),
).properties(
    width=250,
    height=250
).add_selection(category_selector)

hist_chart_category_detail = alt.Chart(df[slices],title="selected categories").mark_line().encode(
    alt.X('stars', sort='x'),
    alt.Y('count()'), 
    alt.Color('category')
).properties(
    width=250,
    height=250
).transform_filter(category_selector)
st.altair_chart(hist_chart_selected | hist_chart_category_detail)

categoryOption = st.selectbox(
        'Choose your final decision on category:',
        sorted(df['category'].unique())
    )

st.header("Given your choices on state and category, we will give your attributes recommendations.")

@st.cache
def get_slice2(df,state,days,category):
    labels = pd.Series([True] * len(df), index=df.index)
    if state:
        labels &= df['state'].apply(lambda x : True if x==state else False)
    if days:
        for day in days:
            labels &= df[day+'_avaliable'] 
    if category:        
        labels &= df['category'].apply(lambda x : True if x==category else False)
    return labels
slices2= get_slice2(df,stateOption,daysOption,categoryOption)
df_filtered = df[slices2]
 
df_prepared  = df_filtered.drop(['name', 'state', 'review_count','categories','is_open', 'BusinessParking', 'Ambience', 'GoodForMeal', 'AcceptsInsurance', 'HairSpecializesIn', 'BestNights','Music', 'Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 
'Saturday', 'Sunday', 'Monday_avaliable', 'Tuesday_avaliable', 'Wednesday_avaliable', 'Thursday_avaliable', 'Friday_avaliable', 'Saturday_avaliable','Sunday_avaliable', 'category'],axis=1)
st.write("The final dataset contains {} records.".format(len(df_prepared)))
if st.checkbox("show filtered data"):
    st.write(df_prepared[:50])


##########start to train##########
from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(df_prepared, test_size=0.2)
df_prepared_no_labels = df_prepared.drop("stars", axis=1)
business_train = train_set.drop("stars", axis=1)
business_labels = train_set["stars"].copy()

business_test = test_set.drop("stars", axis=1)
business_test_labels = test_set["stars"].copy()

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

business_cat = business_train.drop(['latitude', 'longitude'], axis=1)

num_features = ['latitude', 'longitude']
cat_features = list(business_cat)
# print(len(business_train),len(business_test), len(business_labels),len(cat_features))
full_pipeline = ColumnTransformer([
  ("num", StandardScaler(), num_features),
  ("cat", OneHotEncoder(), cat_features),              
])
full_pipeline.fit(df_prepared_no_labels)
business_prepared = full_pipeline.transform(business_train)
business_test_prepared = full_pipeline.transform(business_test)
# print("*")
# print(business_prepared.shape)
tree_reg = DecisionTreeRegressor()
tree_reg.fit(business_prepared, business_labels)

business_predictions = tree_reg.predict(business_test_prepared)
tree_mse = mean_squared_error(business_test_labels, business_predictions)
tree_rmse = np.sqrt(tree_mse)
st.metric(label = "Resulted Tree_RMSE", value = round(tree_rmse,5))

print(tree_rmse)
#housing
column_names = list(business_train.columns) + list(full_pipeline.transformers_[1][1].get_feature_names_out())
for x in list(business_cat):
    column_names.remove(x)
print(column_names)
treefeature_d = {'Importance Score': tree_reg.feature_importances_, 'Features': list(column_names)}
treefeature_df = pd.DataFrame(treefeature_d)
treefeature_df = treefeature_df[treefeature_df['Importance Score']!=0]
treefeature_df = treefeature_df.sort_values('Importance Score',ascending=False)
treefeature_df['Importance Score'] = treefeature_df['Importance Score'].apply(lambda x: round(x, 5))

feature_importance_chart = alt.Chart(treefeature_df).mark_bar().encode(
    alt.X("Importance Score"),
    alt.Y("Features", sort='-x')
)

top_five_features = treefeature_df[0:5]
top_five_features_chart = alt.Chart(top_five_features).mark_bar().encode(
    alt.X("Importance Score"),
    alt.Y("Features", sort='-x')
)

top_five_text = top_five_features_chart.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='Importance Score'
)

all_features_text = feature_importance_chart.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='Importance Score'
)

st.header("The top five features")
st.altair_chart(top_five_features_chart + top_five_text, use_container_width=True)
if st.checkbox("show all features"):
    st.altair_chart(feature_importance_chart + all_features_text, use_container_width=True)

st.markdown("This project was created by Yining Wang and Jiaxiang Wu for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")


