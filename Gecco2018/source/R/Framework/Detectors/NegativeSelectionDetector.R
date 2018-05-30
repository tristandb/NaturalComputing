library(parallel)

detect <- function(dataset){
  loadRepertoire()
  
  row <- binFunction(dataset[, c(2:10)])

  return (detectorApplication(repertoire, row))
}

binFunction <- function(row) {
  return (floor(((row - minimums) / maximums * numberbins)))
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
# Returns whether the detector and row match
detectorMatch <- function(detector, row, r) {
  return (sum(row == detector) >= r)
}


# Continguous match
detectorMatchContinguous <- function(detector, row, r) {
  for (i in 1:(length(detector) - r + 1)) {
    match = TRUE
    for (j in 1:r) {
      if(detector[i+j-1] != row[i+j-1]) {
        match = FALSE
        break
      }
    }
    if (match)
      return (TRUE)
  }
  return (FALSE)
}

# Generates and returns a random detector
# This detector is a vector whose values are in [0, numberbins)
randomDetector <- function() {
  return(as.integer(runif(9, 0, numberbins)))
}


# Generates a repertoire of nr detectors that don't match on selfData
detectorGeneration <- function(selfData, nr=100000) {
  repertoire <- list()
  while (length(repertoire) < nr) {
    detector <- randomDetector()
    flag = FALSE
    for (i in 1:nrow(selfData[, ])) {
      entry <- selfData[i, ]
      if (detectorMatchContinguous(detector, entry, 4)) {
        flag = TRUE
        break
      }
    }
    if (flag == FALSE) {
      repertoire[[length(repertoire)+1]] <- detector
      print(length(repertoire))
    }
  }
  return(repertoire)
}

# Applies all detectors in the repertoire to the row
# Returns TRUE if any of the detectors match. FALSE otherwise
detectorApplication <- function(repertoire, row) {
  for (detector in repertoire) {
    if (detectorMatchContinguous(detector, as.numeric(as.vector(row)), 4)) {
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

# Generates a repertoire consisting of nr detectors
# then saves this repertoire to disk and returns the repertoire
createAndStoreRepertoire <- function(selfData, nr=100000, filename="Data/detectors.RData") {
  repertoire <- unlist(mclapply(1:detectCores(),
    FUN=function(i) detectorGeneration(binnedSelfData, as.integer(nr/detectCores())),
    mc.cores=detectCores()), recursive=FALSE)
  save(repertoire, file=filename)
  return (repertoire)
}

# Loads the repertoire from disk and returns it
loadRepertoire <- function(filename="../Data/detectors.RData") {
  load(filename, .GlobalEnv)
}

if (TRUE) {
trainingData <- readRDS(file = "../Data/waterDataTraining.RDS")
#Delete rows where any column is NA.
#Surprisingly this does not include any rows where EVENT is TRUE
trainingData <- trainingData[complete.cases(trainingData), ]

numberbins <- 32
maximums = apply(trainingData[, c(2:10)], 2, max)
minimums = apply(trainingData[, c(2:10)], 2, min)
range <- (maximums - minimums) / numberbins

binnedData <- t(apply(trainingData[, c(2:10)], 1, binFunction))

selfData <- trainingData[trainingData$EVENT == FALSE,]
nonSelfData <- trainingData[trainingData$EVENT == TRUE,]

binnedSelfData <- t(apply(selfData[, c(2:10)], 1, binFunction))
binnedNonSelfData <- t(apply(nonSelfData[, c(2:10)], 1, binFunction))

#loadRepertoire()
#detectorApplicationDataset(repertoire, binnedNonSelfData)
#detectorApplicationDataset(repertoire, binnedSelfData)

tmp <- createAndStoreRepertoire(binnedSelfData, 100, "../Data/contDetectors.RData")
}