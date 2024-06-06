import streamlit as st
import pandas as pd

# Cache our data
@st.cache_data
def load_df():
    df = pd.read_csv("titanic.csv")
    df['Survived'] = df['Survived'].map({0: 'Dead', 1: 'Alive'})  # Mapping the numeric values to 'Dead' or 'Alive'
    survival_options = df['Survived'].unique()
    p_class_options = df['Pclass'].unique()
    sex_options = df['Sex'].unique()
    embark_options = df['Embarked'].unique()
    min_fare = df['Fare'].min()
    max_fare = df['Fare'].max()
    min_age = df['Age'].min()
    max_age = df['Age'].max()
    return df, survival_options, p_class_options, sex_options, embark_options, min_fare, max_fare, min_age, max_age

def check_rows(column, options):
    return res.loc[res[column].isin(options)]

df, survival_options, p_class_options, sex_options, embark_options, min_fare, max_fare, min_age, max_age = load_df()
res = df

st.title("Titanic Database Query App")

name_query = st.text_input("String match for Name")

# Filtering options
cols = st.columns(5)
gender_filter = cols[0].selectbox("Gender", ['All'] + list(sex_options))
siblings_spouses = cols[1].selectbox("Siblings/Spouses", ['All', 'None', '1 or more'])

# Multiselect for various filters
survival = cols[2].multiselect("Survived", survival_options)
p_class = cols[3].multiselect("Passenger Class", p_class_options)
embark = cols[4].multiselect("Embarked", embark_options)

range_cols = st.columns(3)
min_fare_range, max_fare_range = range_cols[0].slider("Lowest Fare", float(min_fare), float(max_fare), [float(min_fare), float(max_fare)])
min_age_range, max_age_range = range_cols[2].slider("Lowest Age", float(min_age), float(max_age), [float(min_age), float(max_age)])

# Applying filters based on user input
if name_query:
    res = res[res['Name'].str.contains(name_query, case=False, na=False)]

if gender_filter != 'All':
    res = res[res['Sex'] == gender_filter]

if siblings_spouses == 'None':
    res = res[res['SibSp'] == 0]
elif siblings_spouses == '1 or more':
    res = res[res['SibSp'] > 0]

if survival:
    res = check_rows("Survived", survival)
if p_class:
    res = check_rows("Pclass", p_class)
if embark:
    res = check_rows("Embarked", embark)
if range_cols[0].checkbox("Use Fare Range"):
    res = res[(res['Fare'] >= min_fare_range[0]) & (res['Fare'] <= max_fare_range[1])]
if range_cols[2].checkbox("Use Age Range"):
    res = res[(res['Age'] >= min_age_range) & (res['Age'] <= max_age_range)]

removal_columns = st.multiselect("Select Columns to Remove", df.columns.tolist())
for column in removal_columns:
    res = res.drop(column, axis=1)

st.write(res)
