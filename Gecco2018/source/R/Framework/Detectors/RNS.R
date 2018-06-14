detect <- function(dataset){
  loadRepertoire()
  means <- c(8.521414e+00, 1.654820e-01, 8.366415e+00, 7.528990e+02, 2.095210e+02, 1.977803e-02, 1.060988e-01, 1.534209e+03, 9.277287e+02)
  stdev <- c(1.28131547, 0.01020692, 0.10162474, 12.94532958, 7.74751512, 0.00549167, 0.00713156, 208.17169991, 147.44776979)
  dataset[, c(2:10)] <- scale(dataset[, c(2:10)], center=means, scale=stdev)
  r <- 0.6
  for (detector in repertoire) {
    print(detector)
    distance <- euc.dist(dataset[, c(2:10)], detector)
    if (distance < r) {
      print("True")
      return (TRUE)
    }
  }
  
  print("False")
  return (FALSE)
}

# Loads the repertoire from disk and returns it
loadRepertoire <- function(filename="../Data/RNS.RData") {
  load(filename, .GlobalEnv)
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

getRandomDetector <- function(min = -3.5, max = 3.5) {
  return(runif(9, min, max))
}

getRnormDetector <- function() {
  return (rnorm(9))
}

generateInitialRepertoire <- function(nr = 400) {
  repertoire <- list()
  while (length(repertoire) < nr) {
    detector = getRnormDetector()
    detector.age = 1
    repertoire[[length(repertoire)+1]] <- detector
  }
  return (repertoire)
}

generateInitialAge <- function(nr = 400) {
  repertoire.age <- list()
  while (length(repertoire.age) < nr) {
    repertoire.age[[length(repertoire.age)+1]] <- 0
  }
  return (repertoire.age)
}

euc.dist <- function(x1, x2) sqrt(sum((x1 - x2) ^ 2))

knn.get <- function(selfData, detector, n = 10) {
  distances <- apply(selfData[, c(2:10)], 1, function (x) euc.dist(x, detector))
  closest_distances <- sort(distances, index.return=TRUE)$ix[1:10]
  return (selfData[closest_distances, ])
}

mu.d <- function(x, detector, r) {
  return (-1 * (euc.dist(detector, x) ^ 2) / (2 * (r ^ 2)))
}

if (TRUE) {
  # Run Training
  
  # Load Training data
  trainingData <- readRDS(file = "../Data/waterDataTraining.RDS")
  
  #Delete rows where any column is NA.
  #Surprisingly this does not include any rows where EVENT is TRUE
  trainingData <- trainingData[complete.cases(trainingData), ]
  
  # Normalize Training data
  trainingData[, c(2:10)] <- scale(trainingData[, c(2:10)])

  selfData <- trainingData[trainingData$EVENT == FALSE,]
  nonSelfData <- trainingData[trainingData$EVENT == TRUE,]
  
  detectors = 500
  repertoire <- generateInitialRepertoire(detectors)
  repertoire.age <- generateInitialAge(detectors)
  num_iter = 1
  knn = 10
  r = 1
  t = 2.5
  j = 0
  i = 0
  tau = 100
  eta = 1

  while (j < num_iter) {
    print(j)
    
    pb <- txtProgressBar(min = 1, max = detectors, style = 3)
    for (i in seq_along(repertoire)) {
      setTxtProgressBar(pb, i)
      # NearCells = Get k-nearest neighbours of detector,  order with respect to distance
      NearCells <- knn.get(selfData, repertoire[[i]], knn)
      
      # NearestSelf = median of NearCells
      NearestSelf <- colMeans(NearCells[, c(2:10)])
      
      # If distance(d, NearestSelf) < r
      if (euc.dist(repertoire[[i]], NearestSelf) < r) {
        dir <- rowSums(apply(NearCells[, c(2:10)], 1, function(c) repertoire[[i]] - c)) / knn
        
        if (repertoire.age[[i]] > t) {
          # If detector is old enough.
          repertoire[[i]] <- getRandomDetector()
          repertoire.age[[i]] <- 0
        } else {
          # Detector is not old enough, increment age.
          repertoire.age[[i]] <- repertoire.age[[i]] + 1
          repertoire[[i]] <- repertoire[[i]] + eta * dir
        }
      } else {
        repertoire.age[[i]] <- 0
        numerator <- Reduce('+', lapply(repertoire, function(d) mu.d(d, repertoire[[i]], r) * (repertoire[[i]] - d)))
        denominator <- Reduce('+', lapply(repertoire, function(d) mu.d(d, repertoire[[i]], r)))
        dir <- numerator / denominator
        repertoire[[i]] <- repertoire[[i]] + eta * dir
      }
    }
    eta <- eta * exp(-1*i / tau)
    j <- j + 1
    # Save Repertoire
    save(repertoire, file='../Data/RNS.RData')
  }
}
