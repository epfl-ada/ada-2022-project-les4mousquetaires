# Once upon a time there was a small brewer... 🍻🍺

___Temporal study of the beer market around the world in order to simulate it___

## Abstract
Once upon a time there was a little and gentle brewer who dreamed of spreading happiness in the world. As everyone knows, beer makes people happy, so he decided to reach his dream by creating a beer and to spread it around the world. The problem is that he sucked at market study and didn't know how to begin with his business... If he aimed to reach the most people with his beer, he had to make the good choices ! Which type of beers to choose ? Where to open his brewery ? ... That's a complicated problem, isn't it ? Fortunately, ___Les4Mousquetaires___ were here to help this litte and gentle brewer by creating a tool that would help him a lot. This tool is a market simulator that will predict the spread of his beer according to the choice of his beer and brewery. Will this gentle and little brewer reach is dream ? 

## Research questions
How to create a trustworthy prediction model that simulates the spread of a beer around the world based on the available datas from  _RateBeer_ and _BeerAdvocate_ ?

* **Q1** : Can we study and predict how the breweries exports beers in the world ? Can we estimate the exportation rate, i.e. how many percent of a specific beer's type produced in one country are exported in the world ? Is this rate time sensitive ? 
* **Q2** : Can we find a trend in the popularity of the different type of beers during time in each countries ? Can we create a  meaningful model to predict these popularities based on the number of ratings ? 
* **Q3** : How behaves the distribution of the different beer's ratings according to time, to type and to country ? Can we notice a trend ?
* **Q4** : By combining the results from points 1) 2) and 3), can we create a more complexe prediction model that simulates the spread of one type of beer brewed in one specific country ? How trustworthy is this model and which hidden covariates can influence this model ? Can we simulate the part of randomness of the beer's market in our model ?

## Methods
We divide our work in this way: 

### ___1) Pipeline and data preprocessing___

We use the two datasets _RateBeer_ and _BeerAdvocate_ from the website [**RateBeer**](https://www.ratebeer.com/) and [**BeerAdvocate**](https://www.beeradvocate.com/) to get enough datas for our analysis. To facilitate the use of these datasets, we create one datafram containing all the ratings with the corresponding user and brewery information merged to it . We have clusterized all beers in the dataset into a dozen of type.

### ___2) Study of the export of beer___

For each beer type produced in one country and for each year, we estimate the ratios of exportations. From the dataset, we use the number of reviews and the breweries locations to get this estimation. The brewery is considered as the export point and the user as the import point of a beer mentionned in the rating. We make the assumption that the proportion of reviews for brewery location to a user location is a good estimator of the exportations ratios. 

### ___3) Study of the popularity of beer___

We want to see how the popularity of different beer's type varies across years and in each country. In this context, this means that we calculate the proportion of one type of beer among all the beers considered in one year and for one country. To estimate it, we use the number of reviews in the dataset written in one country and during one year and calculate the proportion of each beers type. From this, we use machine learning to get a function that gives the proportion of one beer type in one country at a specific time. We make the assumption that a decreasing _popularitiy_ means that people drink less of this beer and vice versa.

### ___4) Study of the beer's ratings distribution___

We calculate the distribution of the beers ratings (Q3) for all types of beer and for all countries across years. To do that, we plot histograms of the ratings to get an idea of how these distributions looks like. Then, by using statistics, we choose known distributions that best represents these distributions for all countries and type of beers. Their parameters are estimated.

### ___5) Creation of a prediction model___

By combining these last points, we produce a model for the simulation with, as input, a number of a certain type of beers produced in one specific brewery in one country:

* Step 1: Given an number of beers produced for one year, use 2) to estimate how many beers are exported (or not) in each country this year. 
* Step 2: Use 3) and 4) to estimate how the consumption of this beer will vary in each country during one year
* Step 3: From these variations, adjust the number of beers produced for the next year.

We repeat these 3 steps across the simulated years. Because of the lack of datas, we consider that this simulation follows a pattern according the datas between 2000 and 2017. For step 2, we weight the popularity variation with a random coefficient drawn from distributions in 4) to better simulate the unpredicability of the beer's world market.

### ___6) Improve the model___

Further experimentations on the datas used to improve the model.

### ___7) Creation of the website___

We split our website in two parts. As first part, a simulation and as second part, the explanations through the stroy of this simulation.

## Proposed timeline
Some preliminary analysis  are already done and are presented in the jupyter notebooks.

* **02/12/22**  : finish 2)3)4)6)
* **09/12/22**  : finish 5)6) and begin 7)
* **16/12/22** : continue 6) and 7)
* **23/12/22** : finish 7)

## Organization within the team

* D'Artagnan : 2) 6)
* Aramis     : 3) 6)
* Athos      : 4) 6)
* Porthos    : 5) 7)
  
  
<p align="center">
  <img src="https://user-images.githubusercontent.com/77831063/202671376-6a4ebd1e-e6d2-4096-af15-e275b3d00cd3.png" />
</p>

Inspiration for our team name [**Les_Trois_Mousquetaires**](https://en.wikipedia.org/wiki/Les_Trois_Mousquetaires)

