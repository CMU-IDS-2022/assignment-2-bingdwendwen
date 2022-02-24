from turtle import color

from numpy import sort
import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Yelp Business Data.")

@st.cache  # add caching so we load the data only once
def load_data():
    business_path = "yelp_business_cleaned.csv"
    df = pd.read_csv(business_path).astype(str)
    return df

df = load_data()

st.write(df)

st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")


# df_map = [pd.to_numeric(df['latitude']),pd.to_numeric(df['longitude'])]
# st.map(df_map)


df['stars'] = pd.to_numeric(df['stars'])
df['review_count'] = pd.to_numeric(df['review_count'])

review_count_chart = alt.Chart(df).mark_line().encode(
    x=alt.X("review_count", scale=alt.Scale(zero=False), sort="-x"),
    y=alt.Y("mean(stars)", scale=alt.Scale(zero=False)),
    color = 'count(stars)',
).properties(
    width=800, height=400
).interactive()

st.write(review_count_chart)



chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("state", scale=alt.Scale(zero=False), sort="-x"),
    y=alt.Y("mean(stars)", scale=alt.Scale(zero=False)),
    color = 'count(stars)',
    tooltip = ['count(stars)','median(stars)', 'max(stars)', 'min(stars)' ]
).properties(
    width=800, height=400
).interactive()

st.write(chart)






st.markdown("This project was created by Yining Wang and Jiaxiang Wu for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")

