from turtle import color
from typing import Tuple

from numpy import sort
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np


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
state_review_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("state", scale=alt.Scale(zero=False), sort="-x"),
    y=alt.Y("mean(stars)", scale=alt.Scale(zero=False)),
    color = 'count(stars)',
    tooltip = ['count(stars)','median(stars)', 'max(stars)', 'min(stars)' ]
).properties(
    width=800, height=400
).interactive()

st.write(state_review_chart)

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
st.write("The sliced dataset contains {} elements ({:.1%} of total).".format(slices.sum(), slices.sum() / len(df)))
chart1 = alt.Chart(df[slices]).mark_circle().encode(
    alt.X('category',scale=alt.Scale(zero=False), sort="x"),
    alt.Y('stars'),
    size = 'count(stars)',
    color = 'count(stars)',
    tooltip = ["stars","category","count(stars)"]
)
st.altair_chart(chart1, use_container_width=True)


chart2 = alt.Chart(df[~slices]).mark_circle(size = 20).encode(
    alt.X('category',scale=alt.Scale(zero=False), sort="x"),
    alt.Y('stars'),
    size = 'count(stars)',
    tooltip = ["stars","category","count(stars)"]
)
st.altair_chart(chart2, use_container_width=True)


st.markdown("This project was created by Yining Wang and Jiaxiang Wu for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")

