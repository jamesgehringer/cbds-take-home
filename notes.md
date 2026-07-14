# Historical Events

# Increases
- Civil Rights 
- Title 9
- Affirmative action

# Decreases
- **Economic Downrurns/Recessions** 2008 Recession is global
- Dotcom bubble, housing crisis, start of Covid
- International Conflicts
- Wars (Vietnam, Korea, Middle East x2)
- Post 9/11 enlistment burst

# Process
- Increases - Look for largest rate of changes 
- Decreases - Find Valleys
- Might need to combine both 

# Thoughts
- Might need to turn the enrollment data into change from previous year
- ~~Can we break it into phasic/tonic portions of the timeseries~~
- Do we need to smooth the data, or will that potentially destroy anything interesting 
- Relative change vs raw numbers vs normalized to a year

# Limitations
- This is very US centric 
- It would potentially be worth while to normalize to country population, but we were instructed to only use the existing data sources

# Things I learned
- Economic down turns may lead to increased enrollment, as people don't have jobs so they go back to school
- Data set is every 5 years
- Each country is sorted into 1 income group
- The income group with the greatest change across 2000-2010 was upper-middle income, this would need further investigation, normalization by population of this group (China, Brazil, Mexico is upper middle income, likely driving this)
- Second largest increase is lower-middle income, with the same limitation as before, as India and Philipines is lower middle income
- If we look at things in a somewhat normalized way, in percent change, you can see low income groups countries rate went down across the 2008 financial crisis, and continued to drop beyond
- Looking at the map I made, it seems like there is 1 or 2 countries per region that have huge increases, and with what we saw in the GDP question, each region seems to have its own pattern, so I split out the income based plot by region and saw some interesting patterns between the groups. 
    - Upper-Middle income is the biggest increase in Latin America and Caribbean and East Asia and Pacific
    - High income is the largest increase in Europe and Central Asia (Also North America, but it is the only group there)
    - Lower-Middle Income is the largest increase in South Asia and Sub-Saharan Africa
        - These are all be driven by the fact that these are the largest group per region

| region | incomegroup | country_count |
| --- | --- | --- |
| East Asia and Pacific | High income | 8 |
| East Asia and Pacific | Low income | 1 |
| East Asia and Pacific | Lower middle income | **9** |
| East Asia and Pacific | Upper middle income | 7 |
| Europe and Central Asia | High income | **34** |
| Europe and Central Asia | Low income | 1 |
| Europe and Central Asia | Lower middle income | 4 |
| Europe and Central Asia | Upper middle income | 14 |
| Latin America and Caribbean | High income | 8 |
| Latin America and Caribbean | Low income | 1 |
| Latin America and Caribbean | Lower middle income | 4 |
| Latin America and Caribbean | Upper middle income | **17** |
| Middle East and North Africa | High income | **8** |
| Middle East and North Africa | Low income | 2 |
| Middle East and North Africa | Lower middle income | 6 |
| Middle East and North Africa | Upper middle income | 5 |
| North America | High income | **2** |
| South Asia | Low income | 1 |
| South Asia | Lower middle income | **6** |
| South Asia | Upper middle income | 1 |
| Sub-Saharan Africa | High income | 2 |
| Sub-Saharan Africa | Low income | **23** |
| Sub-Saharan Africa | Lower middle income | 18 |
| Sub-Saharan Africa | Upper middle income | 5 |

- In the percent change from previous year bar graph, Saudi Arabia and Madagascar have incredibly large increases (89000% in 1955 and 70250% in 1960). Both of these countries started expanding the number of their universities. These large percent changes demonstrate the establishment of modern universities in these countries. 
    - Saudi Arabia: Universities established in 1949, 1953, and 1957. With 6 students enrolled in a single university in 1955, and 5383 after the second univesity opened in 1953, we see the 89000% increase in the graph.
        - The discovery of oil in 1938 led to resources being available to invest in academic institutions, to make sure educational growth paced economic growth, leading to the establishment of universities across the 1950s.
    - Madagascar had 1 university in 1955, with 2 students enrolled. By 1960, there were 5 total universities, each with about 40 students, excluding the university established in 1955, which jumped to 1245, which would cause that large percent change.
        - Madagascar gained its independence from France in June 1960, which kicked off a want to develop their own national system.