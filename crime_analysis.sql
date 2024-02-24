
-- This SQL script analyzes crime data within the city of San Francisco.
-- The script then performs various queries to derive insights from the data, including:
-- 1. Identifying the top 5 areas with the highest number of crimes in 2023.
-- 2. Determining the top 10 crime categories with the highest incidence rates.
-- 3. Analyzing crimes categorized as violent, including incidents such as rape, robbery, assault, and homicide.
-- 4. Examining incidents related to vehicle theft and their distribution across different areas.
-- 5. Examining the distribution of crimes across different days of the week.
-- 6. Analyzing the distribution of crimes based on time of day (morning, day, evening, night).
-- 7. Identifying areas with the highest number of crimes during evening hours.
-- 8. Calculate crime spikes by comparing the number of crimes on a particular day with the previous day that give us possibility to analyze their underlying causes

-- Create View to filter crimes for the year 2023 including only criminal cases.
create view crimes_2023 as
select * from crimes_sf
where incident_year = 2023 and incident_category != 'Non-Criminal';

-- Query to find top 5 areas with the highest number of crimes in 2023.
-- Taking into account that some entries in the "analysis_neighborhood" field may be null,
-- we can substitute those null values with "Police District" entries,
-- as they essentially represent the same geographic area.
select count(incident_id) as number_of_crimes,
       CASE
           WHEN analysis_neighborhood IS NULL THEN police_district
           ELSE analysis_neighborhood
       END AS area
from crimes_2023
group by area
order by 1 desc
limit 5;

-- Query to find top 10 categories of crime with the highest number of crimes in 2023.
select count(incident_id) as number_of_crimes, incident_category
from crimes_2023
group by incident_category
order by 1 desc
limit 10;

-- Query to find number of crimes for violent incident categories
-- According to FBI’s Uniform Crime Reporting (UCR) Program,
-- violent crime is composed of four offenses: murder and nonnegligent manslaughter, rape, robbery, and aggravated assault.
select count(incident_id) as number_of_crimes, incident_category
from crimes_2023
where incident_category ilike '%rape%' or incident_category ilike '%robbery%' or incident_category ilike '%assault%' or incident_category ilike '%homicide%'
group by incident_category
order by 1 desc;

-- Query to identify the ten regions with the most occurrences of vehicle thefts and thefts from vehicles.
select count(incident_id) as number_of_crimes, incident_category,
       CASE
           WHEN analysis_neighborhood IS NULL THEN police_district
           ELSE analysis_neighborhood
       END AS area
from crimes_2023
where incident_category ilike '%vehicle theft%'
group by incident_category, area
order by 1 desc
limit 10;

-- Query to find number of crimes by day of the week.
select count(incident_id) as number_of_crimes, incident_day_of_week
from crimes_2023
group by incident_day_of_week
order by 1 desc;

-- Query to find number of crimes by time of day.
select count(incident_id) as number_of_crimes,
    case
        when incident_time between '06:00' and '11:59' then 'morning'
        when incident_time between '12:00' and '17:59' then 'day'
        when incident_time between '18:00' and '23:59' then 'evening'
        else 'night'
    end as time_of_day
from crimes_2023
group by time_of_day;

-- Query to find number of crimes in each area during the evening hours (20:00 to 23:59).
select count(incident_id) as number_of_crimes,
       CASE
           WHEN analysis_neighborhood IS NULL THEN police_district
           ELSE analysis_neighborhood
       END AS area
from crimes_sf
where incident_time between '20:00' and '23:59'
group by 2
order by 1 Desc;

-- Common Table Expression (CTE) to calculate crime spikes.
with crime_spikes as (
    select
        "Incident Date" as date,
        count(incident_id) as number_of_crimes,
        lag(count(incident_id)) over (order by "Incident Date" asc) as number_of_crimes_previous_day
    from crimes_sf
    group by date
)

-- Query to find and display crime spikes and analyze their underlying causes.
select date, number_of_crimes - number_of_crimes_previous_day as difference
from crime_spikes
where number_of_crimes - number_of_crimes_previous_day is not null
order by difference desc














