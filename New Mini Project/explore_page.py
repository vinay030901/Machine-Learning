import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def remove_countries(counts,bar):
    counts_map={}
    for i in range(len(counts)):
        if counts.values[i]>=bar:
            counts_map[counts.index[i]]=counts.index[i]
        else:
            counts_map[counts.index[i]]="other"
    return counts_map

def years(x):
    if x=="More than 50 years":
        return 50
    if x=="Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

def clean_devtype(x):
    if 'front-end' in x:
        return 'front-end developer'
    if 'back-end' in x:
        return 'back-end developer'
    if 'mobile' in x:
        return 'mobile developer'
    if 'academic' in x:
        return 'academic researcher'
    if 'game' in x:
        return 'game developer'
    if 'data' in x:
        return 'data scientist'
    if 'full-stack' in x:
        return 'full-stack developer'

@st.cache
def load_data():
    df=pd.read_csv("survey_results_public.csv")
    df=df[["Country","EdLevel","YearsCodePro","Employment","DevType","ConvertedCompYearly"]]
    df=df.rename({"ConvertedCompYearly":"Salary"},axis=1)
    df=df.rename({"DevType":"Devtype"},axis=1)
    df=df[df["Salary"].notnull()]
    df=df.dropna()
    df=df[df["Employment"]=="Employed full-time"]
    df=df.drop("Employment",axis=1)
    
    country_map = remove_countries(df.Country.value_counts(),300)
    df.Country = df.Country.map(country_map)
    df=df[df.Salary<=250000]
    df=df[df.Salary>=10000]
    df=df[df["Country"]!="Other"]
    df.YearsCodePro = df.YearsCodePro.apply(years)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df['Devtype'] = df['Devtype'].apply(clean_devtype)
    return df

df=load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salary")
    
    st.write("""### Stack Overflow Developer Survey 2020""")
    
    data=df.Country.value_counts()
    
    fig1,ax1=plt.subplots(1,1,figsize=(20,15))
    ax1.pie(data,labels=data.index,autopct="%1.1f%%",shadow=True,startangle=90)
    ax1.axis("equal")
    
    st.write("""#### Number of data from different countries""")
    
    st.pyplot(fig1)
    
    st.write("""#### Mean Salary based on country""")
    data=df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    st.write("""#### Median Salary based on country""")
    data=df.groupby(["Country"])["Salary"].median().sort_values(ascending=True)
    st.bar_chart(data)
    
    st.write("""#### Mean Salary based on Profession""")
    data=df.groupby(["Devtype"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    st.write("""#### Mean Salary based on Profession""")
    data=df.groupby(["Devtype"])["Salary"].median().sort_values(ascending=True)
    st.bar_chart(data)