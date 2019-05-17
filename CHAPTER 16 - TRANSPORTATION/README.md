# Chapter 16 - Transportation
### [CEQR technical manual chapter 16](https://www1.nyc.gov/assets/oec/technical-manual/16_Transportation_2014.pdf)
A positive effect on one mode of travel may
negatively impact another, while a negative effect on travel modes may negatively impact several aspects of the transportation
system. The objective of the transportation analyses is to determine whether a proposed project may have a
potential significant impact on traffic operations and mobility, public transportation facilities and services, pedestrian
elements and flow, safety of all roadway users (pedestrians, cyclists, transit users and motorists), on- and off-street
parking, or goods movement. 

### Analysis steps:
1. build a python code that acquires **Census / ACS data** to give a picture of the study area (in this case the 3 census tracts of Red Hook) of the following: (1) labor force (census) (2) # of jobs (could do by industry, not necessary for Friday) (3) unemployment rate (census)

2. analyze commuting patterns of the **existing labor force** of the study area; include **modes of transportation capacities** (i.e citibike / ferry capacity). show in *graphs for every mean of transportation* and in *pie chart* for the whole labor force.

3. Draw the **job opportunities shed**: map a 45-minutes commute "shed" from the center of each of the 3 census tracts to understand availability of jobs. see this as a reference (page 13):
https://www1.nyc.gov/assets/planning/download/pdf/about/dcp-priorities/data-expertise/nyc-geography-jobs-0718.pdf

4. predict transportation mode usage considering the RWCDS additions of *housing units* and *jobs*

5. project / map the 45-minutes commute "shed"  if a **"B-71" bus** would be added, connecting Red Hook to to Financial District through the tunnel


### Data:
- PLUTO and MapPLUTO
- Census / ACS : age; labor force, commuting patterns
- Citi bike, TLC, NYC Ferry, MTA
- SONYC data

