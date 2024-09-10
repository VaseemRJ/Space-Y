import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

#Create app
app = dash.Dash(__name__)
#Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True
# Read the historical_automobile_sales data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')
#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year
year_list = [i for i in range(1980, 2024, 1)]
#Layout Section of Dash
#Task 1 Add the Title to the Dashboard
app.layout = html.Div(children=[html.H1('Automobile Sales Statistics Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),

# TASK 2: Add drop-down menus to the dashboard with appropriate titles and options below the first inner division
     #outer division starts
     html.Div([
                    #Dropdown1 to select Report-type
                    dcc.Dropdown(id='Dropdown-Statistics', 
                   	options=[
                           {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                           {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                           ],
                 	 placeholder='Select a report type', value = 'Select Statistics',
                 	 style={'width': '80%', 'padding': '3px', 'font_size': '20px'})

                    #Dropdown2 to select Year
 		            dcc.Dropdown(id='Select-Year', 
                   	options=[
                            {'label': i, 'value': i} for i in year_list],
                  	placeholder='Select-year',
                  	style={'width': '30%', 'padding': '3px', 'font_size': '20px'})
        ]),

#TASK 3: Add two empty divisions for output inside the next inner division. 
         #Second Inner division for adding 2 inner divisions for 2 output graphs

		html.Div([
    			html.Div(id='output-container',
                className='chart-grid, style={'display': 'flex'}),
			])

                    html.Div([
                
                        html.Div([ ], id='plot1'),
                        html.Div([ ], id='plot2'),
                        html.Div([ ], id='plot3'),
                        html.Div([ ], id='plot4'),
                    ], style={'display': 'flex'}),

    ])
    #outer division ends

])
#layout ends

#TASK 4: Add the Ouput and input components inside the app.callback decorator.
#Place to add @app.callback Decorator
@app.callback(
		[Output(component_id='plot1', component_property='children'),
        Output(component_id='plot2', component_property='children')],
        [Input(component_id='Dropdown-Statistics', component_property='value'),
        Input(component_id='Select-Year', component_property='value')])

#TASK 5: Add the callback function.   
#Place to define the callback function .
def update_output_container(input_statistics,input_year):
    if input_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = df[df['Recession'] == 1]
    else:
	input_year == 'Yearly Statistics':
        # Filter the data based on the selected year
       	input_year = df['Year']

#Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
         # grouping data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        # Plotting the line graph
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Automobile sales in Recession Period"))
..........
#Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
 # use groupby to create relevant data for plotting. 
 #Hint:Use Vehicle_Type and Automobile_Sales columns
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                
        R_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title="Vehicle Sales by Type"))

............
# Plot 3 : Pie chart for total expenditure share by vehicle type during recessions
            # grouping data for plotting
            # Hint:Use Vehicle_Type and Advertising_Expenditure columns
            exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
            R_chart3 = dcc.Graph(
                    figure=px.pie(exp_rec,
                    values='Advertising_Expenditure',
                    names='Vehicle_Type',
                 title="Advertising Expenditure by Vehicle Type"
                )
        )
..........
# Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
       #grouping data for plotting
       # Hint:Use unemployment_rate,Vehicle_Type and Automobile_Sales columns
        unemp_data= recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data,
        x='unemployment_rate',
        y='Automobile_Sales',
        color='Vehicle_Type',
        labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
        title='Effect of Unemployment Rate on Vehicle Type and Sales'))

    return [
            html.Div(children=[R_chart1, R_chart2],style={'display': 'flex'}),
            html.Div(children=[R_chart3, R_chart4],style={'display': 'flex'})
            ]
 
# Yearly Statistic Report Plots 
     # Check for Yearly Statistics.
    elif input_statistics == 'Yearly Statistics':
        yearly_data = df[df['Year'] == input_year]
                              
..........
# Plot 1 :Yearly Automobile sales using line chart for the whole period.
............
        # grouping data for plotting.
        # Hint:Use the columns Year and Automobile_Sales.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
        title='Average Automobile Sales Over Years'))
            
..........
# Plot 2 :Total Monthly Automobile sales using line chart.

..........
         # grouping data for plotting.
        # Hint:Use the columns Month and Automobile_Sales.
        mas=data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas,
            x='Month',
            y='Automobile_Sales',
            title='Total Monthly Automobile Sales'))


 ..........
# Plot bar chart for average number of vehicles sold during the given year
............
         # grouping data for plotting.
         # Hint:Use the columns Year and Automobile_Sales
        avr_vdata=yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=avr_vdata,
	title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

..........
# Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
          # grouping data for plotting.
          # Hint:Use the columns Vehicle_Type and Advertising_Expenditure
         exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, 
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title='Total Advertisment Expenditure for Each Vehicle'))

  return [
                html.Div(className='chart-item', 	children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'}),
                html.Div(className='chart-item',
	 children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
	no_update
                ]
return no_update, no_update   

   return [dcc.Graph(figure=Y_chart1),
            dcc.Graph(figure=Y_chart2),
            dcc.Graph(figure=Y_chart3),
            dcc.Graph(figure=Y_chart4) ]
if __name__ == '__main__':
    app.run_server()
