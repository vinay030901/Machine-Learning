import streamlit  as st
import pickle
import numpy as np

def load_model():
    with open('steps1.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data=load_model()

regressor = data["model"]
le_country=data["le_country"]
le_education = data["le_edu"]
le_dev=data["le_dev"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    
    st.write("""### We need some information to predict the salary""")
    

    countries={"Argentina","Australia","Austria","Belgium","Brazil","Canada","Denmark","Finland","France","Germany","India",
           "Iran, Islamic Republic of...","Italy","Mexico","Netherlands","Norway","Pakistan","Poland",
           "Russian Federation","South Africa","Spain","Sweden","Switzerland","Turkey","Ukrainia",
           "United Kingdom of Great Britain and Northern Ireland","United States of America"}

    education={'Master’s degree', 'Bachelor’s degree', 'Less than a Bachelors','Post grad'}
    
    devtype={"full-stack developer","front-end developer","back-end developer","data scientist","mobile developer","game developer"}

    country=st.selectbox("Country", countries)

    education = st.selectbox("Education Level", education)

    experience=st.slider("Years of Experience",0,50,3)
    
    devtype=st.selectbox("Developer type",devtype)

    predict = st.button("Predict Salary")
    if predict:
        X = np.array([[country,education,experience,devtype]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X[:, 3] = le_dev.transform(X[:,3])
        X = X.astype(float)
    
        salary=regressor.predict(X)
        st.subheader(f"the estimated salary is ${salary[0]:.2f}")