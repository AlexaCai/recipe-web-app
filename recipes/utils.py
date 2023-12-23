from io import BytesIO 
import base64
import matplotlib.pyplot as plt
import pandas as pd

def get_graph():
   buffer = BytesIO()         
   plt.savefig(buffer, format='png')
   buffer.seek(0)
   image_png=buffer.getvalue()
   graph=base64.b64encode(image_png)
   graph=graph.decode('utf-8')
   buffer.close()
   return graph

def get_chart(chart_type, data, **kwargs):
   #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
   #AGG is preferred solution to write PNG files
   plt.switch_backend('AGG')

   #specify figure size
   fig=plt.figure(figsize=(6,3))

   if chart_type == '#1':
       country_counts = data['origin_country'].value_counts()

       country_counts.plot(kind='bar')

       plt.xlabel('Origin Country')
       plt.ylabel('Number of Recipes')
       plt.title('Number of Recipes per Origin Country')

   elif chart_type == '#2':
        category_counts = data['recipe_category'].value_counts()

        plt.figure(figsize=(6, 6))
        plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')
        plt.title("Recipe Categories")
        plt.show()


   elif chart_type == '#3':
        categories = ['15 min or less', '30 min or less', '45 min or less', '60 min or less', '60 min or more']
        cooking_time_counts = {category: 0 for category in categories}

        for index, row in data.iterrows():
            cooking_time = row['cooking_time']

            cooking_time = int(cooking_time)

            if cooking_time <= 15:
                cooking_time_counts['15 min or less'] += 1
            elif cooking_time <= 30:
                cooking_time_counts['30 min or less'] += 1
            elif cooking_time <= 45:
                cooking_time_counts['45 min or less'] += 1
            elif cooking_time <= 60:
                cooking_time_counts['60 min or less'] += 1
            else:
                cooking_time_counts['60 min or more'] += 1

        cooking_time_counts_series = pd.Series(cooking_time_counts)

        category_order = ['15 min or less', '30 min or less', '45 min or less', '60 min or less', '60 min or more']

        cumulative_counts = cooking_time_counts_series[category_order].cumsum()
        ax = cumulative_counts.plot(kind='line', marker='o', figsize=(8, 6))

        ax.set_xticks(range(len(category_order)))
        ax.set_xticklabels(category_order, rotation=45, fontsize=10, horizontalalignment='right')
        plt.xlabel('Cooking Time Category')
        plt.ylabel('Cumulative Number of Recipes')
        plt.title('Cumulative Number of Recipes in Cooking Time Categories')

        # Display grid lines
        ax.grid(True)

   else:
       print ('unknown chart type')

   #specify layout details
   plt.tight_layout()

   #render the graph to file
   chart =get_graph() 
   return chart       