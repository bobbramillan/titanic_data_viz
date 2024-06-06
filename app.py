import streamlit as st
import pandas as pd

# Cache our data
@st.cache
def load_df():
    df = pd.read_csv("titanic.csv")
    df['Survived'] = df['Survived'].map({0: 'Dead', 1: 'Alive'})  # Mapping the numeric values to 'Dead' or 'Alive'
    df = df.rename(columns={'SibSp': 'Siblings/Spouses Aboard', 'Parch': 'Parents/Children Aboard'})
    return df

df = load_df()

st.title("Titanic Database Query App")

name_query = st.text_input("String match for Name")

# Filtering options
cols = st.columns(5)
gender_filter = cols[0].selectbox("Gender", ['All', 'Male', 'Female'], help="Select the gender of the passengers.")
siblings_spouses = cols[1].selectbox("Siblings/Spouses Aboard", ['All', 'None', '1 or more'], help="Number of siblings or spouses aboard.")
parents_children = cols[2].selectbox("Parents/Children Aboard", ['All', 'None', '1 or more'], help="Number of parents or children aboard.")
survival = cols[3].multiselect("Survived", ['All', 'Alive', 'Dead'], help="Survival status of the passengers.")
p_class = cols[4].multiselect("Passenger Class", df['Pclass'].unique(), help="Select the class of ticket purchased.")

embark_options = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
embark = st.multiselect("Embarked", options=list(embark_options.keys()), format_func=lambda x: embark_options[x], help="Port of embarkation")

range_cols = st.columns(3)
min_fare_range, max_fare_range = range_cols[0].slider("Fare range", float(df['Fare'].min()), float(df['Fare'].max()), [float(df['Fare'].min()), float(df['Fare'].max())], help="Range of ticket fares.")
min_age_range, max_age_range = range_cols[2].slider("Age range", float(df['Age'].min()), float(df['Age'].max()), [float(df['Age'].min()), float(df['Age'].max())], help="Range of passenger ages.")

# Filter based on the selected criteria
filtered_df = df

if name_query:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(name_query, case=False, na=False)]

if gender_filter != 'All':
    filtered_df = filtered_df[filtered_df['Sex'] == gender_filter]

if siblings_spouses == 'None':
    filtered_df = filtered_df[filtered_df['Siblings/Spouses Aboard'] == 0]
elif siblings_spouses == '1 or more':
    filtered_df = filtered_df[filtered_df['Siblings/Spouses Aboard'] > 0]

if parents_children == 'None':
    filtered_df = filtered_df[filtered_df['Parents/Children Aboard'] == 0]
elif parents_children == '1 or more':
    filtered_df = filtered_df[filtered_df['Parents/Children Aboard'] > 0]

if 'Alive' in survival:
    filtered_df = filtered_df[filtered_df['Survived'] == 'Alive']
if 'Dead' in survival:
    filtered_df = filtered_df[filtered_df['Survived'] == 'Dead']

if p_class:
    filtered_df = filtered_df[filtered_df['Pclass'].isin(p_class)]
if embark:
    filtered_df = filtered_df[filtered_df['Embarked'].isin(embark)]

filtered_df = filtered_df[(filtered_df['Fare'] >= min_fare_range) & (filtered_df['Fare'] <= max_fare_range)]
filtered_df = filtered_df[(filtered_df['Age'] >= min_age_range) & (filtered_df['Age'] <= max_age_range)]

st.write(filtered_df)
