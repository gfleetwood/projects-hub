# https://www.reddit.com/r/rstats/comments/evx6f6/r_coding_for_coin_toss_need_help/

#Initially 1 person had the virus. If the coin is tossed and is heads,
#the initial person spreads it to 1 person. If the coin is tails the 
#initial spreads it to 2 people. These people infected would be the
#1st generation. Now here is the problem, what code can continue its
#function ( h=1, t=2) on the NEWLY INFECTED. As in if the first toss
#was tails, two other people would be infected. 

library(tidyverse)

infection_spread <- function(infected){
  
  possibilities <- c(2,1)
  new_infections <- possibilities %>% 
    sample(., length(infected), replace = TRUE) %>% 
    sum() %>% 
    rep(1, .)
  
  result <- c(infected, new_infections)
  
  return(result)
  
}

infected <- c(1)
generations <- 1:10

reduce(
  .x = generations,
  .f = function(infected, generation) infection_spread(infected),
  .init = infected
)
