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
state_review_chart = alt.Chart(df).mark_bar(color="lightblue").encode(
    x=alt.X("state", scale=alt.Scale(zero=False), sort="-x"),
    y=alt.Y("mean(stars)", scale=alt.Scale(zero=False), title="Mean of stars"),
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


st.markdown("This project was created by Yining Wang and Jiaxiang Wu for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")

