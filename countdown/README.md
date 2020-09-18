# Countdown's Numbers Round With Genetic Algorithms

[Countdown](https://en.wikipedia.org/wiki/Countdown_(game_show)) is a famous British game show which I discovered through the crossover show, [8 Out of 10 Cats Does Countdown](https://en.wikipedia.org/wiki/8_Out_of_10_Cats_Does_Countdown). I especially found myself enjoying the Numbers Round. This portion of the shows asks contestants to use simple mathematical operations with selected numbers to get as close to a three digit target as possible. When I wanted to learn more about genetic algorithms, I decided to use this arena as my playground. 

I first planned to build a game pitting human against machine. That went well with my choice of the [REMI](https://github.com/dddomodossola/remi) Python library. Unfortunately, the deployment phase failed utterly. This forced me to rewrite everything in R in order to leverage the power of Shiny. In the course of retracing my steps, I decided to move the Shiny app away from a reproduction of the game itself to a testing ground for the algorithm. 

You can play against the algorithm by cloning this repo, installing REMI (and its dependencies), and running "python ga_remi.py". The game will open in your browser. The Shiny testing ground is available [here](https://gfleetwood.shinyapps.io/countdown_ga_app/).
