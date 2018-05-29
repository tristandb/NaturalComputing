detect <- function(row){
  return (detectorApplication(repertoire, row))
}

destruct <- function(){
  ## remove global variables
  
  ## delete files
}

getOutline <- function(){
  competitor.name <- "Tristan de Boer & Tim van Dijk"
  competitor.institution <- "Radboud University"
  
  return(list(NAME=competitor.name, INSTITUTION=competitor.institution));
}

detectorMatch <- function(detector, row, r) {
  #for (i in 1:nrow(data[, ])) {
  #  entry <- data[i, ]
  matches = sum(row == detector)
  if (matches >= r)
    return (TRUE)
  #}
  return (FALSE)
}

randomDetector <- function() {
  return(as.integer(runif(9, 0, numberbins))) #Return list of 10 elements between 1 and 100
}

detectorGeneration <- function(selfData, nr=100000) {
  repertoire <- list()
  while (length(repertoire) < nr) {
    detector <- randomDetector()
    flag = FALSE
    for (i in 1:nrow(selfData[, ])) {
      entry <- selfData[i, ]
      if (detectorMatch(detector, entry, 4)) {
        flag = TRUE
        break
      }
    }
    if (flag == FALSE) {
      repertoire[[length(repertoire)+1]] <- detector
    }
  }
  return(repertoire)
}

#Return TRUE in case input is non-self
detectorApplication <- function(repertoire, row) {
  for (detector in repertoire) {
    if (detectorMatch(detector, row, 4)) {
      return (TRUE)
    }
  }
  return (FALSE)
}

detectorApplicationDataset <- function(repertoire, dataset) {
  for (i in 1:nrow(dataset[, ])) {
    entry <- dataset[i, ]
    print(detectorApplication(repertoire, entry))
  }
}

trainingData <- readRDS(file = "../Data/waterDataTraining.RDS")
#Delete rows where any column is NA.
#Surprisingly this does not include any rows where EVENT is TRUE
trainingData <- trainingData[complete.cases(trainingData), ]

numberbins <- 30
maximums = apply(trainingData[, c(2:10)], 2, max)
minimums = apply(trainingData[, c(2:10)], 2, min)
range <- (maximums - minimums) / numberbins

binnedData <- t(apply(trainingData[, c(2:10)], 1, binFunction))

selfData <- trainingData[binnedTrainingData$EVENT == FALSE,]
nonSelfData <- trainingData[binnedTrainingData$EVENT == TRUE,]

binnedSelfData <- t(apply(selfData[, c(2:10)], 1, binFunction))
binnedNonSelfData <- t(apply(nonSelfData[, c(2:10)], 1, binFunction))

repertoire <- detectorGeneration(binnedSelfData[,], 100)

detectorApplicationDataset(repertoire, binnedSelfData)
detectorApplicationDataset(repertoire, binnedNonSelfData)
