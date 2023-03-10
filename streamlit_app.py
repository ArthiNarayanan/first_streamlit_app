import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favourites')
streamlit.text('🍛Omega 3 and Blueberry oatmeal')
streamlit.text('🥗Kale Spinach and rocket Smoothie')
streamlit.text('🐔Hard boiled free Ranged Egg')
streamlit.text('🥑🍞Avacado Toast')
streamlit.header('🍌🍓Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

def get_fruity_vice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice) 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return(fruityvice_normalized)
  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function=get_fruity_vice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    

    
except URLError as e:
  streamlit.error()
  
  





streamlit.header("View Our Fruit List-Add Your Favourites:")
#sf funs
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
if streamlit.button('Get fruit List'):  
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
#streamlit.stop()

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')")
        return 'Thanks for adding '+new_fruit
        
    

try:
   fruit_choice1= streamlit.text_input('What fruit would you like to add?',)
   if not fruit_choice1:
    streamlit.error("Please select a fruit to add")
  else :
    if streamlit.button('Add Fruit'):  
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_v=insert_row_snowflake(fruit_choice1)
        streamlit.write(my_v)
        my_cnx.close()
 except URLError as e:
    streamlit.error()



