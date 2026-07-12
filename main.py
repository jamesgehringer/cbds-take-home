import pandas as pd
import plotly.express as px

class HistoricalEventFinder:

    def __init__(self, file):
        self.df = pd.read_csv(file)
        
        # Drop rows with missing data in column: 'students5_estimated'
        self.df = self.df.dropna(subset=['students5_estimated'])

        # Performed 3 aggregations grouped on columns: 'country', 'year'
        self.df = self.df.groupby(['country', 'year']).\
            agg(students5_estimated_mean=('students5_estimated', 'mean'),
                students5_estimated_std=('students5_estimated', 'std'),
                students5_estimated_sum=('students5_estimated', 'sum')).reset_index()

    def test_print(self):
        print(self.df)

    def plot_line_chart(self, start_year, end_year):
        fig = px.line(
                self.df, 
                x="year", 
                y="students5_estimated_sum", 
                color="country", # Creates a separate line for each unique value in this column
                title="Line Graph Separated by Column Values"
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
        fig.show()



    def plot_change_map(self, start_year, end_year):
        change_during_event = self.find_change_over_window(start_year,end_year)

        fig2 = px.choropleth(
            change_during_event,
            locations="country",
            locationmode='country names',
            color="rate_of_change",
            color_continuous_scale="Viridis",
            range_color=(change_during_event["rate_of_change"].min(), change_during_event["rate_of_change"].max()),
        )
        fig2.show()

    def find_change_over_window(self, start_year, end_year):
        change_during_event = pd.DataFrame(columns=["country", "rate_of_change"])
        for value, subset in self.df.groupby('country'):
            try:
                rate = subset.query("year == @end_year")['students5_estimated_sum'].iloc[0]-subset.query("year == @start_year")['students5_estimated_sum'].iloc[0]
                new_row = pd.DataFrame([{'country':subset["country"].iloc[0], 'rate_of_change':rate.astype('float64')}])
                change_during_event = pd.concat([change_during_event, new_row], ignore_index=True)
            except IndexError:
                print(f"{subset["country"].iloc[0]} does not have enough data")
        
        change_during_event['rate_of_change'] = pd.to_numeric(change_during_event['rate_of_change'], errors='coerce')
        return change_during_event


    def main(self):
        start_year, end_year = 1980, 1995
        
        historyObj.test_print()
        historyObj.plot_line_chart( start_year, end_year)
        self.plot_change_map( start_year, end_year)

if __name__ == "__main__":
    historyObj = HistoricalEventFinder(r'c:\Users\james\Documents\Repos\cbds-take-home\enrollments.csv')
    historyObj.main()