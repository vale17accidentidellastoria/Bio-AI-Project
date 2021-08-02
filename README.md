# Bio-Inspired Artificial Intelligence Project 
## A multi-objective optimization approach to sustainability in the fashion industry 
**Abstract**   
Fashion industry is accountable for about 10% of global greenhouses emissions and 20% of water pollution. This research tries to define the sustainability of cotton fiber in terms of policies towards workers of the supply chain and wise handling of pollutant elements involved in the process of cotton growing and transportation. Once the variables to take into account and their ranges have been defined, a Non-dominated Sorting Genetic Algorithm has been performed to identify solutions that, while maximizing the overall sustainability, keep cotton prices to acceptable levels. The obtained Pareto front can be compared with the indexes that have been assigned to 10 countries representative of different levels of sustainability.  <br> <br>
**NNSGA-2**  
Non-Dominated Sorting Genetic Algorithm has been used to solve the multi-obejective optimization problem of maximizing textile sustainability while minimizing fiber cost. 
It has been implemented with Gaussian Mutations with a rate of 0.1, 10 generations (that could be increased) and a population of 100 individuals. 
<br> <br>
**Fitness Function**  
It has been formalized a sustainability index as a weighted sum of three sub-indexes taking into account:
* aspects related to the fiber production sustainability (defined as emissions dued to fertilizer application and waste of water)
* the sustainability of fiber transportation (accounting for means of transport and connected greenhouse gases emissions, load factor, freight and distance to be covered) 
* ethical value of policies towards workers (hours of work per day, minor work, cost of the life related to salary perceived).


This index, that is an approximation based on the available data, has been used to evaluate the fitness of the individuals in the population of solutions.
<br> <br>
````
Run options:

python3 main.py -d Italy -f data/transport_co2_data.csv
````
## Future Work 
This project might be improved better defining the constraints describing the relationship betweeen sustainability and final price and improving the approximations realized taking into account more data. 
Data availability has, in fact, been the main problem affecting this research. 
