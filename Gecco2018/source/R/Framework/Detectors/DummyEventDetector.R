
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