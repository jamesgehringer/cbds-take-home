import pandas as pd
import plotly.express as px

class HistoricalEventFinder:

    def __init__(self, file):
        self.df = pd.read_csv(file)
        
        # Drop rows with missing data in column: 'students5_estimated'
        self.df = self.df.dropna(subset=['students5_estimated'])
        self.df_count_per_region_per_income = self.df.groupby(['region', 'incomegroup']).agg(country_count=('country', 'nunique')).reset_index()
        self.df_income = self.df.groupby(['year', 'incomegroup','region']).\
            agg(students5_estimated_sum=('students5_estimated', 'sum'),
                students5_estimated_mean=('students5_estimated', 'mean'),
                students5_estimated_std=('students5_estimated', 'std')).reset_index()
        # Performed 3 aggregations grouped on columns: 'country', 'year'
        self.df = self.df.groupby(['country', 'year', 'incomegroup']).\
            agg(students5_estimated_mean=('students5_estimated', 'mean'),
                students5_estimated_std=('students5_estimated', 'std'),
                students5_estimated_sum=('students5_estimated', 'sum')).reset_index()
        
        self.df["percent_change"]=self.df['students5_estimated_sum'].pct_change()*100

        

    def plot_line_chart(self, start_year, end_year):
        title = "Enrollment by Country from " + str(start_year)+ " to " +  str(end_year)
        fig = px.line(
                self.df, 
                x="year", 
                y="students5_estimated_sum", 
                color="country", # Creates a separate line for each unique value in this column
                title=title,
                error_y="students5_estimated_std",
            )

                # Add a vertical shaded block between X-coordinates 2 and 3
        fig.add_vrect(
            x0=start_year, x1=end_year, 
            fillcolor="red", 
            opacity=0.5, 
            layer="below", 
            line_width=0
        )

        # 4. Display the chart
        # fig.show()
        fig.write_html("results\\enrollment_by_country.html")
        fig.write_image("results\\enrollment_by_country.png")

    def plot_line_chart_by_income(self, start_year, end_year):
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

                # Add a vertical shaded block between X-coordinates 2 and 3
        fig.add_vrect(
            x0=start_year, x1=end_year, 
            fillcolor="red", 
            opacity=0.5, 
            layer="below", 
            line_width=0
        )

        # 4. Display the chart
        # fig.show()
        fig.write_html("results\\enrollment_by_incomegroup.html")
        fig.write_image("results\\enrollment_by_incomegroup.png")

    def plot_change_map(self, start_year, end_year):
        title = "Change in Enrollment by Country from " + str(start_year)+ " to " +  str(end_year)
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
        fig.write_html("results\\increase_by_country_worldmap.html")
        fig.write_image("results\\increase_by_country_worldmap.png")

    def find_change_over_window(self, start_year, end_year):
        change_during_event = pd.DataFrame(columns=["country", "rate_of_change", "incomegroup"])
        # Let's create a measure of change over the window of interest
        for value, subset in self.df.groupby('country'):
            try:
                rate = subset.query("year == @end_year")['students5_estimated_sum'].iloc[0]-subset.query("year == @start_year")['students5_estimated_sum'].iloc[0]
                new_row = pd.DataFrame([{'country':subset["country"].iloc[0],
                                        'rate_of_change':rate.astype('float64'), 
                                        'incomegroup':subset["incomegroup"].iloc[0]}])
                change_during_event = pd.concat([change_during_event, new_row], ignore_index=True)
            except IndexError:
                # I'd through this information into a formal log
                print(f"{subset["country"].iloc[0]} does not have enough data")
        
        change_during_event['rate_of_change'] = pd.to_numeric(change_during_event['rate_of_change'], errors='coerce')
        return change_during_event



    def plot_bar_graph_percent_change(self, start_year, end_year):
        fig = px.bar(self.df, x="year", 
                y="percent_change", color="incomegroup", title="Long-Form Input", hover_data=['country'])
        fig.add_vrect(
            x0=start_year, x1=end_year, 
            fillcolor="red", 
            opacity=0.5, 
            layer="below", 
            line_width=0
        )

        fig.write_html("results\\percent_change_bar_graph.html")
        fig.write_image("results\\percent_change_bar_graph.png")
        # fig.show()

    def main(self):
        #put your years of interest here
        #with more time, I'd add input validation
        start_year, end_year = 2000, 2010
        
        historyObj.plot_line_chart( start_year, end_year)
        historyObj.plot_line_chart_by_income( start_year, end_year)
        historyObj.plot_change_map( start_year, end_year)
        historyObj.plot_bar_graph_percent_change(start_year, end_year)

        print(self.df_count_per_region_per_income)

if __name__ == "__main__":
    historyObj = HistoricalEventFinder(r'c:\Users\james\Documents\Repos\cbds-take-home\data\enrollments.csv')
    historyObj.main()