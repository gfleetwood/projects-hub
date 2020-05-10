# https://mobile.twitter.com/Oilfield_Rando/status/1251478913064357889

library(tabulizer)
library(tidyverse)
library(glue)
library(janitor)

base <- file.path("home", "gordon", "Downloads")
cares_act_raw <- extract_tables("https://www2.ed.gov/about/offices/list/ope/allocationsforsection18004a1ofcaresact.pdf")
new_names <- c("opeid", "school", "total_allocation", "emergency_financial_aid_min")

cares_act_cleaned <- cares_act_raw %>% 
  map_df(
  ~ .x %>%
    # Convert from matrix
    as.data.frame() %>%
    # The first two rows consist of a header and an empty row.
    # Ignore those and keep the column headings and data
    slice(3:n()) %>%
    # Now remove the column headings row. It will be re-added later
    slice(-1)
  ) %>%
  # Remove the empty column
  select(-V5) %>%
  # Readd the column headings through renaming
  rename_all(~ new_names) %>%
  # These values are strings formatted as currencies: $1, 2345.45 for example
  # This casts them to numbers: 12345.45
  mutate(
    total_allocation = parse_number(total_allocation),
    emergency_financial_aid_min = parse_number(emergency_financial_aid_min)
  ) %>%
  # Remove summary from the bottom of the pdf
  slice(-5189:-n()) %>%
  mutate(
    non_financial_aid_money = total_allocation - emergency_financial_aid_min
  ) %>% 
  remove_empty(c("rows"))
