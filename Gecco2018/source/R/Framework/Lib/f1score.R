calculateScore <- function(observations, predictions){
  TruePositive <- sum(observations & predictions)
  FalsePositive <- sum(!observations & predictions)
  TrueNegative <- sum(!observations & !predictions)
  FalseNegative <- sum(observations & !predictions)
  
  PositivePredictiveValue <- TruePositive / sum(predictions)
  TruePositiveRate <- TruePositive / sum(observations)
  
  F1score <- (2 * PositivePredictiveValue * TruePositiveRate) / (PositivePredictiveValue + TruePositiveRate)
  
  if (is.nan(F1score)) F1score <- 0
  
  return(list(TP=TruePositive, FP=FalsePositive, TN=TrueNegative, FN=FalseNegative, SCORE= F1score))
}