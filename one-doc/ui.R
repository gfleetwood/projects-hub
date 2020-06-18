# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Shiny: Sheets | Docs | Slides"),
  
  tabsetPanel(type = "tabs",
              tabPanel("Spreadsheet", rHandsontableOutput("hot")),
              tabPanel("Document", 
                       sidebarLayout(
                           sidebarPanel(
                               aceEditor("rmd", mode="markdown", value='
### Sample knitr Doc

This is some markdown text. It may also have embedded R code
which will be executed.
```{r}
rnorm(5)
```
It can even include graphical elements.
```{r}
head(df)
```
')
                               ,
                               actionButton("eval", "Update")
                           ), 
                           mainPanel(htmlOutput("knitDoc"))
                           )
                             ),
                    tabPanel("Slides", 
                             sidebarLayout(
                                 sidebarPanel(
                                     aceEditor("rmd2", mode="markdown", value='

# In the morning

## Getting up

- Turn off alarm
- Get out of bed
                                       
## Breakfast
                                       
- Eat eggs
- Drink coffee
')
                                     ,
                                     actionButton("eval2", "Update")
                                 ), 
                                 mainPanel(htmlOutput("knitDoc2"))
                             )
                             

                             ) #tab panel
        )
    )
  )
