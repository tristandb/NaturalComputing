# 
detect <- function(dataset){
  ## Predict event as random guess with 50% probability
  probability <- runif(1)
  event <- probability > 0.5
  
  ## return prediction
  return(event)
}

destruct <- function(){
  ## remove global variables
  
  ## delete files
}

getOutline <- function(){
  competitor.name <- "Max Muster"
  competitor.institution <- "Muster Uni"
  
  return (list(NAME=competitor.name, INSTITUTION=competitor.institution));
}

binFunction <- function(row) {
  return (round(((row - minimums) / maximums * numberbins),0))
}


trainingData <- readRDS(file = "../Data/waterDataTraining.RDS")
trainingData <- trainingData[complete.cases(trainingData), ]

numberbins <- 128
maximums = apply(trainingData[, c(2:10)], 2, max)
minimums = apply(trainingData[, c(2:10)], 2, min)
range <- (maximums - minimums) / numberbins

formattedData <- t(apply(trainingData[, c(2:10)], 1, binFunction))


