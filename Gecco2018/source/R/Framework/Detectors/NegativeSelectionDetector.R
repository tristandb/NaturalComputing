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

# Matches 1 detector on 1 row
# Returns if the detector and row match
detectorMatch <- function(detector, row, r) {
  matches = sum(row == detector)
  if (matches >= r)
    return (TRUE)
  #}
  return (FALSE)
}

# Generates and returns a random detector
# This detector is a vector whose values are in [0, numberbins)
randomDetector <- function() {
  return(as.integer(runif(9, 0, numberbins)))
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

# Applies all detectors in the repertoire to the row
# Returns TRUE if any of the detectors match. FALSE otherwise
detectorApplication <- function(repertoire, row) {
  for (detector in repertoire) {
    if (detectorMatch(detector, row, 4)) {
      return (TRUE)
    }
  }
  return (FALSE)
}

# Wrapper that calls detectorApplication for each row in the dataset
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
