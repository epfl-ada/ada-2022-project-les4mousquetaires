# Once upon a time there was a little and gentle brewer... 🍻🍺

___An original ADA story about beer !___

Here is the link of the website : https://juliengasser.github.io/ADA4mousquetaires/

## Abstract
Once upon a time there was a little and gentle brewer who dreamed of spreading happiness in the world. As everyone knows, beer makes people happy, so he decided to reach his dream by creating a beer and to spread it around the world. The problem is that he sucked at market study and didn’t know how to begin with his business… If he first aimed to reach as many countries as possible and secondly the most people as possible with his beer, he had to make the good choices ! Which type of beers to choose ? Where to open his brewery ? … That’s a complicated problem, isn’t it ? Fortunately, Les4Mousquetaires were here to help this litte and gentle brewer by creating a tool that would help him a lot. This tool is a brewery success simulation that will predict the spread of his beer according to the choice of his beer and brewery. Will this gentle and little brewer reach is dream ?

## Research questions
How to create a trustworthy prediction model that simulates the spread of a beer across years around the world based on the available datas from  _RateBeer_ and _BeerAdvocate_ ?

* **Q1** : Can we study how the breweries exports beers in the world ? Can we estimate the exportation profile, i.e. how many percent of a specific beer's type produced in one country are exported in the world ? Is this rate time sensitive ? 
* **Q2** : Can we find a trend in the popularity of the different type of beers during time in each countries ? Can we create a meaningful model to establish these popularities based on the number of ratings ? 
* **Q3** : How behaves the distribution of the different beer's ratings according to time, to type and to country ? Can we notice a trend ?
* **Q4** : By combining the results from points 1) 2) and 3), can we create a more complexe prediction model that simulates the spread of one type of beer brewed in one specific country ? How trustworthy is this simulation algorithm for the brewery success simulation? Can we simulate the part of randomness of the beer's market in our model ?

## Methods
We divide our work in this way: 

### ___1) Pipeline and data preprocessing___

We use the two datasets _RateBeer_ and _BeerAdvocate_ from the website [**RateBeer**](https://www.ratebeer.com/) and [**BeerAdvocate**](https://www.beeradvocate.com/) to get enough datas for our analysis. To facilitate the use of these datasets, we create one datafram containing all the ratings with the corresponding user and brewery information merged to it. An important effort has been performed to deal with the size of the dataset. We have also clusterized all beers in the dataset into a dozen of type. 

### ___2) Study of the export of beer___

For each beer type produced in one country and for each year, we estimate the ratios of exportations. From the dataset, we use the posting date, the number of reviews and the breweries locations to get this estimation. The brewery is considered as the export point and the user as the import point of a beer mentionned in the rating. We make the assumption that the proportion of reviews for brewery location to a user location is a good estimator of the exportations ratios. 

### ___3) Study of the popularity of beer___

We want to see how the popularity of different beer's type varies across years and in each country. In this context, this means that we calculate the proportion of one type of beer among all the beers considered in one year and for one country. To estimate it, we use the number of reviews in the dataset written in one country and during one year and calculate the proportion of each beers type. As the obtained curves are tortuous and not smooth, we use a KNN with large k to smooth them out. The idea behind that is to get curves that better represent the behaviour of a popularity evolution. We make the assumption that a decreasing popularitiy means that people drink less of this beer and vice versa.

### ___4) Study of the beer's ratings distribution___

We calculate the distribution of the beers ratings for all types of beer and for all countries across years. To do that, we plot histograms of the ratings to get an idea of how these distributions looks like. Then, by using statistics, distributions are analyzed and parameters are exctracted for all countries and beer styles.

### ___5) Creation of the simulation algorithm___


The algorithm works as follow. First, the little and gentle brewer has to choose, as input, the type of beers that he wants to produce and the country where he wants to open his brewery. Then, the next three steps are iterated across the years :

* Step 1: At the start of the year, the number of beers expected to be distributed during this year is divided in shares of beers that are allocated to different beer consuming countries. This is the exportation rate step determined with the beer exportation profile.
* Step 2: Estimate how beer exports will vary during the year, based on the popularity of beer and the affinity that the country has for a style of beer. This resulting number of beers that will be effectively consummed this current year.
* Step 3: The number of beers expected to be distributed during the next year (step 1, next iteration) is taken as the effectively consummed number of beers this current year.

The output of this algorithm is the brewery success simulation tool.

### ___6) Creation of the website___

We split our website in two parts. As first part, a simulation and as second part, the explanations through the stroy of this simulation. The website is built by Beautiful Jekyll. The creation of the website was divided in two parts : 6.1 technical part to build and support the website, 6.2 write the story 


## Organization within the team

* D'Artagnan : 2) Study of the export of beer, 5) Creation of the simulation algorithm, 6.2) Creation of the website (write the story)
* Aramis     : 1) Pipeline and data preprocessing, 6.1) Creation of the website (technical part to build and support the website)
* Athos      : 4) Study of the beer's ratings distribution, 5) Creation of the simulation algorithm, 6.2) Creation of the website (write the story)
* Porthos    : 3) Study of the popularity of beer, 5) Creation of the simulation algorithm, 6.2) Creation of the website (write the story)
  
  
<p align="center">
  <img src="https://user-images.githubusercontent.com/77831063/202671376-6a4ebd1e-e6d2-4096-af15-e275b3d00cd3.png" />
</p>

Inspiration for our team name [**Les_Trois_Mousquetaires**](https://en.wikipedia.org/wiki/Les_Trois_Mousquetaires)

