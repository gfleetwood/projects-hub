library(shiny)
library(rhandsontable)
library(shinyAce)
library(markdown)
library(knitr)

df <- read.csv("test.csv", stringsAsFactors = FALSE)