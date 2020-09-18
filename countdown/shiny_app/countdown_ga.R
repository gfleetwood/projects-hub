library(tidyr)

setup <- function(){
  target <- sample(100:999, 1)
  num_big_nums <- sample(1:4,1)
  nums <- c(sample(10:99, num_big_nums),
            sample(1:9, 6-num_big_nums))
  ops <- c('+', '-', '/', '*')
  return(list('target' = target, 'nums' = nums, 'ops' = ops))
}

create.individual <- function(nums, ops){
  pop.member <- seq(1,11,1)
  pop.member[seq(1,11,2)] <- sample(nums, size = 6)
  pop.member[seq(2,10,2)] <- sample(ops, 
                                    size = 5, 
                                    replace = T)
  return(pop.member)
}

create.population <- function(nums, ops, size){
  indivs <- lapply(1:size, (function(x) create.individual(nums, ops)))
  return(indivs)
}

result <- function(individual){
  return(eval(parse(text = paste0(individual, collapse = ''))))
}

fitness.indiv <- function(indiv, target){
  
  target.produced <- result(indiv)
  digits <- grep("^[[:digit:]]*$", indiv)
  
  #A decimal or negative number gets a fitness score of 10**6 
  if ((abs(target.produced - as.integer(target.produced)) > 0) || (target.produced < 0)){
    return(10^6)
  }
  
  #So does an individual with repeated digits
  if(length(unique(digits)) < length(digits)){
    return(10^6)
  }
  
  return (abs(as.integer(target.produced) - target)) 
}

fitness.population <- function(pop, target){
  fitness.indivs <- c()
  for(i in 1:length(pop)){
    fitness.indivs <- c(fitness.indivs, 
                        fitness.indiv(pop[[i]], target))
  }
  return(mean(fitness.indivs))
}

evolution <- function(pop, nums, ops, target, retain, 
                      random.select, mutate){
  
  grades <- sapply(pop, 
                   (function(x) fitness.indiv(x, target)))

  pop.grades <- data.frame(matrix(unlist(pop), 
                                  nrow = 10, 
                                  byrow = T),
                           stringsAsFactors = FALSE)

  pop.grades$grades <- grades
  pop.grades <- pop.grades[order(pop.grades$grades),]
  best.individual <- as.character(pop.grades[1,1:11])
  
  parents <- pop.grades[1:as.integer(nrow(pop.grades)*retain), 1:11]

  random.selection.df <- pop.grades[(as.integer(nrow(pop.grades)*retain)+1):nrow(pop.grades), 1:11]
  for(i in 1:nrow(random.selection.df)){
    if(random.select > runif(1)){
      parents <- rbind(parents, random.selection.df[i,])
    }
  }
  
  for(i in 1:nrow(parents)){
    if(mutate > runif(1)){
      pos.to.mutate <- sample(1:11,1)
      if(pos.to.mutate%%2==0){
        parents[i, pos.to.mutate] <- sample(ops, 1)
      }
    }
  }

  parents.len.initial <- nrow(parents)
  while(nrow(parents) < length(pop)){
    parent.1.2 <- sample(seq(1,5,1), 2)
    parent.1 <- as.character(parents[parent.1.2[1],])
    parent.2 <- as.character(parents[parent.1.2[2],])
    child <- c(parent.1[1:6], parent.2[7:11])
    parents <- rbind(parents, child)
  }
  
  parents <- as.list(as.data.frame(t(parents), 
                                   stringsAsFactors = F))
  return(list(parents, best.individual))
}

run.countdown <- function(nums, ops, target, times.to.run){
  pop <- create.population(nums, ops, 10)
  fitness.history <- c(fitness.population(pop, target))
  start.time <- Sys.time()
  for(i in 1:times.to.run){
    results <- evolution(pop, nums, ops, target, .5, .05, .01)
    pop <- results[[1]]
    best.individual <- results[[2]]
  }
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  return(list(fitness.history, best.individual, time.taken))
}


