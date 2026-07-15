import pandas as pd
import plotly.express as px

class HistoricalEventFinder:

    def __init__(self, file):
        self.df = pd.read_csv(file)
        
        # Drop rows with missing data in column: 'students5_estimated'
        self.df = self.df.dropna(subset=['students5_estimated'])

        # This was added later to get a quick count of unique countries per income group per region
        self.df_count_per_region_per_income = self.df.groupby(['region', 'incomegroup']).agg(country_count=('country', 'nunique')).reset_index()
        
        # Wanted to break out the income group by region across time
        # This was orginally just broken down into year by income group
        self.df_income = self.df.groupby(['year', 'incomegroup','region']).\
            agg(students5_estimated_sum=('students5_estimated', 'sum'),
                students5_estimated_mean=('students5_estimated', 'mean'),
                students5_estimated_std=('students5_estimated', 'std')).reset_index()
        
        # Performed 3 aggregations grouped on columns: 'country', 'year'
        self.df = self.df.groupby(['country', 'year', 'incomegroup']).\
            agg(students5_estimated_mean=('students5_estimated', 'mean'),
                students5_estimated_std=('students5_estimated', 'std'),
                students5_estimated_sum=('students5_estimated', 'sum')).reset_index()
        
        # Added a percent change column just to explore a normalized effect
        self.df["percent_change"]=self.df['students5_estimated_sum'].pct_change()*100

        

    def plot_line_chart(self, start_year, end_year):
        ''' This function can plot a line graph of the summed enrollment number over time
        A time  window of interest can be defined using start_year and end_year
        It will output an png and an interactive html into the results folder.
        '''

        title = "Enrollment by Country from " + str(start_year)+ " to " +  str(end_year)
        fig = px.line(
                self.df, 
                x="year", 
                y="students5_estimated_sum", 
                color="country", # Creates a separate line for each unique value in this column
                title=title,
                error_y="students5_estimated_std",
            )

        
        fig.add_vrect(
            x0=start_year, x1=end_year, 
            fillcolor="red", 
            opacity=0.5, 
            layer="below", 
            line_width=0
        )

        # 4. Display the chart
        # fig.show()

        # Save the charts
        fig.write_html("results\\enrollment_by_country.html")
        fig.write_image("results\\enrollment_by_country.png", width=1200, height=800, scale=2)

    def plot_line_chart_by_income(self, start_year, end_year):
        ''' This function can plot a line graph of the summed enrollment number over time by income group
        It will also plot each region as its own subplot
        A time  window of interest can be defined using start_year and end_year
        It will output an png and an interactive html into the results folder.
        '''

        title = "Enrollment by Income Group from " + str(start_year)+ " to " +  str(end_year)
        fig = px.line(
                self.df_income, 
                x="year", 
                y="students5_estimated_sum", 
                color="incomegroup", # Creates a separate line for each unique value in this column
                title=title,
                facet_col="region",
                facet_col_wrap=3, 
                error_y="students5_estimated_std"
            )

        # Add a vertical shaded block between X-coordinates start_year and end_year      
        fig.add_vrect(
            x0=start_year, x1=end_year, 
            fillcolor="red", 
            opacity=0.5, 
            layer="below", 
            line_width=0
        )

        # 4. Display the chart
        # fig.show()

        #Save the figures
        fig.write_html("results\\enrollment_by_incomegroup.html")
        fig.write_image("results\\enrollment_by_incomegroup.png", width=1200, height=800, scale=2)

    def plot_change_map(self, start_year, end_year):
        ''' This function can plot a world map of the change of summed enrollment number over time per country
        The time window that the change will be calculated over can be defined using start_year and end_year
        It will output an png and an interactive html into the results folder.
        '''
        title = "Change in Enrollment by Country from " + str(start_year)+ " to " +  str(end_year)
        # This function will generate the dataframe needed for the world plot, it will reurn the enrollment change coupled with the country name
        change_during_event = self.find_change_over_window(start_year,end_year)

        fig = px.choropleth(
            change_during_event,
            locations="country",
            locationmode='country names',
            color="rate_of_change",
            color_continuous_scale="Viridis",
            range_color=(change_during_event["rate_of_change"].min(), change_during_event["rate_of_change"].max()/3),
            title= title
            
        )
        # fig.show()

        # Save the figures
        fig.write_html("results\\increase_by_country_worldmap.html")
        fig.write_image("results\\increase_by_country_worldmap.png", width=1200, height=800, scale=2)

    def find_change_over_window(self, start_year, end_year):
        """
        This will produce the dataframe needed to populate the world map, with the enrollment change across the passed in years
        It subtracts the enrollment sum from start_year from the enrollment sum in end_year per country
        It returns a dataframe with the change, the country, and the incomegroup (added later)   
        
        """
        change_during_event = pd.DataFrame(columns=["country", "rate_of_change", "incomegroup"])
        # Let's create a measure of change over the time window of interest
        # This iterates through each country, gets the enrollment from the requested years and makes a new row in the new data from
        for value, subset in self.df.groupby('country'):
            try:
                rate = subset.query("year == @end_year")['students5_estimated_sum'].iloc[0]-subset.query("year == @start_year")['students5_estimated_sum'].iloc[0]
                new_row = pd.DataFrame([{'country':subset["country"].iloc[0],
                                        'rate_of_change':rate.astype('float64'), 
                                        'incomegroup':subset["incomegroup"].iloc[0]}])
                change_during_event = pd.concat([change_during_event, new_row], ignore_index=True)
            except IndexError:
                # In some cases, there wasn't the required data for every country, so I excluded them from the dataset for now
                # I'd through this information into a formal log
                print(f"{subset["country"].iloc[0]} does not have enough data")
        
        # The plotly map did not like this column in an object format, so we just forced it to numeric
        change_during_event['rate_of_change'] = pd.to_numeric(change_during_event['rate_of_change'], errors='coerce')
        return change_during_event



    def plot_bar_graph_percent_change(self, start_year, end_year):
        """
        This was a quick function at the end to plot a stacked bar chart, to see the percent change split up by country and income group
        It takes in start_year and end_year to add the highlight on the plot
        """
        fig = px.bar(self.df, x="year", 
                y="percent_change", color="incomegroup", title="Percent Change by Income Group", hover_data=['country'])
        fig.add_vrect(
            x0=start_year, x1=end_year, 
            fillcolor="red", 
            opacity=0.5, 
            layer="below", 
            line_width=0
        )

        # Save the figure
        fig.write_html("results\\percent_change_bar_graph.html")
        fig.write_image("results\\percent_change_bar_graph.png", width=1200, height=800, scale=2)
        # fig.show()

    def main(self):
        #put your years of interest here
        #with more time, I'd add input validation
        start_year, end_year = 2000, 2010
        
        # I originally wanted to see enrollment by country by time
        historyObj.plot_line_chart( start_year, end_year)
        # This was added later, but we broke it out by incomegroup and region as well
        historyObj.plot_line_chart_by_income( start_year, end_year)
        #  Plotted the change in enrollment across the event on a world map to see any geographical effects
        historyObj.plot_change_map( start_year, end_year)
        # Plotted the percent change across the time window by country and income group to try and account for population differences
        historyObj.plot_bar_graph_percent_change(start_year, end_year)

        # This printed out the unique number of countries per region per incomegroup
        print(self.df_count_per_region_per_income)

if __name__ == "__main__":
    historyObj = HistoricalEventFinder(r'data\enrollments.csv')
    historyObj.main()