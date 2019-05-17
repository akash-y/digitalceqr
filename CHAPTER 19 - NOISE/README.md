# Chapter 19 - Noise
### [CEQR technical manual chapter 19](https://www1.nyc.gov/assets/oec/technical-manual/19_Noise_2014.pdf)
noise levels that are not
considered hazardous should not be overlooked since they can cause stress-related illnesses, disrupt sleep, and interrupt
activities requiring concentration. In New York City, with its high concentration of population and commercial activities,
such problems may be common.
This chapter discusses the topic of noise as it relates to regulations and guidelines that govern activities in New York
City. It defines technical terms, discusses the appropriateness of a noise analysis, and provides information related to
study area definitions, technical subareas, models, and detailed noise analysis techniques. 

Subjects to be considered in this analysis:
- Challenging **CEQR manual thresholds**
- Determining **analysis radius / scope**
- Noise for each land-use
- Compare to other **manufacturing and mixed-used neighborhoods**

Data:
- PLUTO and MapPLUTO
- SONYC data
- Trucks routes 
- ZAP: permits / constructions
- 311 Noise complaints: _please note that 311 data biases must be acknowledged_

### Analysis
For the **SONYC** data analysis of detecting trucks, we will use **Network traffic anomaly detection based on sliding window** technique. Through sliding time window, traffic anomaly detection will be limited to the specified scope of time. This significantly reduces the amount of data analysis to improve the speed of anomaly detection. Using the dataset from real network to simulate, we validate that the proposed algorithm is effective and feasible.

See notebook named 
