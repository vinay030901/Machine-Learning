import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

path = r'D:\Numpy\Machine Learning\gdp-life.csv'
data = pd.read_csv(path)

df = pd.DataFrame(data)

plt.scatter(df.earnings, df.Life_satisfaction, color='red')
plt.xlabel("GDP per capita")
plt.ylabel("life satisfaction")
# plt.show()

model = LinearRegression()
model.fit(df[['earnings']], df.Life_satisfaction)
print(model.predict([[21711]]))

kmodel = KNeighborsRegressor(n_neighbors=3)
kmodel.fit(df[['earnings']], df.Life_satisfaction)
print(kmodel.predict([[21711]]))
plt.plot(df.earnings,model.predict(df[['earnings']]),color='blue')
plt.plot(df.earnings,kmodel.predict(df[['earnings']]),color='black')
plt.show()