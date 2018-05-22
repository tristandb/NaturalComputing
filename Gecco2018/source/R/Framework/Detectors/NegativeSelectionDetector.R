

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
  competitor.name <- "Tristan de Boer & Tim van Dijk"
  competitor.institution <- "Radboud University"
  
  return(list(NAME=competitor.name, INSTITUTION=competitor.institution));
}

detectorMatch <- function(detector, selfData) {
    return(FALSE)
}

randomDetector <- function() {
  return(runif(5, 1, 100)) #Return list of 10 elements between 1 and 100
}

detectorGeneration <- function(selfData, nr=10000) {
  repertoire <- list()
  while (length(repertoire) < nr) {
    detector <- randomDetector()
    if (!detectorMatch(detector, selfData)) {
      repertoire[[length(repertoire)+1]] <- detector
    }
  }
  return(repertoire)
}

#Return TRUE in case input is non-self
detectorApplication <- function(repertoire, input) {
  for (detector in repertoire) {
    if (detectorMatch(detector, input)) {
      return(TRUE)
    }
  }
  return(FALSE)
}

trainingData <- readRDS(file = "../Data/waterDataTraining.RDS")
#Delete rows where any column is NA.
#Surprisingly this does not include any rows where EVENT is TRUE
trainingData <- trainingData[complete.cases(trainingData), ]


selfData <- trainingData[trainingData$EVENT == FALSE,]
nonSelfData <- trainingData[trainingData$EVENT == TRUE,]

means <- colMeans(trainingData[, c(2:10)])
sds <- apply(trainingData[, c(2:10)], 2 , sd)


selfEntry <- selfData[1231, 2:10]
nonSelfEntry <- nonSelfData[1235, 2:10]

cat("Self: \n")
for (i in 1:length(selfEntry)) {
	prob <- pnorm(selfEntry[1, i], means[i], sds[i])
	print(prob)
}

cat("\nNonself: \n")
for (i in 1:length(nonSelfEntry)) {
	prob <- pnorm(nonSelfEntry[1, i], means[i], sds[i])
	print(prob)
}
#pnorm(entry[0], 1, 1)

#repertoire <- detectorGeneration(selfData, 5)
#detectorApplication(repertoire, trainingData)\
#trainingData[trainingData$]