###############################################################################
#                                                                             # 
#      GECCO 2018 Industrial Challenge - Main Evaluation                      #
#                                                                             #  
#      Run this file to test and evaluate your Detector                       #
#                                                                             #
###############################################################################

###############################################################################
### initialize workspace ######################################################
rm(list=ls());
set.seed(2);

baseDir <- getwd()
dataDir  <- paste(baseDir, "Data", sep="/")
submissionDir <- paste(baseDir, "Detectors", sep="/")
librariesDir  <- paste(baseDir, "Lib", sep="/")

setwd(librariesDir)
source("f1score.R")


###############################################################################
### read training data  #######################################################
#timeSeriesData <- data.frame(X1=(runif(n = 100)*100), X2=(runif(n = 100)*100), X3=(runif(n = 100)*100), EVENT=(runif(n = 100)+0.03)>=1, Prediction=NA)
setwd(dataDir)
trainingData <- readRDS(file = "waterDataTraining.RDS")

###############################################################################
### execute and evaluate all detectors ########################################
setwd(submissionDir)
allDetectors <- dir(pattern = "*.R")

completeResult <- NULL

for (submission in allDetectors){ # submission <- allDetectors[6]
  ## Load detector
  source(submission)
  submissionOutline <- getOutline()
  cat(paste("\nRunning Submission: ", submissionOutline$NAME))
  
  ## Run detector
  predictionResult <- rep(NA, nrow(trainingData)) # empty result array
  for (rowIndex in 1:nrow(trainingData)){
    predictionResult[rowIndex] <- detect(dataset = trainingData[rowIndex, -11])
  }
  
  ## Evaluate prediction using F1 score
  result <- calculateScore(observations = trainingData$EVENT, predictions = predictionResult)
  
  ## Write evaluation result to result table
  SubmissionResult <- data.frame(SUBMISSION=submissionOutline$NAME, TP=result$TP, FP=result$FP, TN=result$TN, FN=result$FN, RESULT=result$SCORE, stringsAsFactors = FALSE)
  if (is.null(completeResult)){
    completeResult <- SubmissionResult
  } else {
    completeResult <- rbind(completeResult, SubmissionResult)  
  }
}
cat("\nEvaluation finished:\n")
setwd(baseDir)

###############################################################################
### show results ##############################################################

## Largest value for result wins
winningIndex <- which(max(completeResult$RESULT) == completeResult$RESULT)
cat(paste("\nSubmission: *", completeResult$SUBMISSION[winningIndex], "* wins.\nSee data.frame: completeResult for more Details.", sep="" ))

completeResult








