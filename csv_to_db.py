import pandas
import sqlite3


cnx = sqlite3.connect('db.sqlite3')
df = pandas.read_csv('ingredients.csv')

df.to_sql('recipe_ingredient', cnx, if_exists='append', index=False)



