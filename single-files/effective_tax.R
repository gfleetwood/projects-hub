df = data.frame(
  tax_rate = c(.1, .12, .22, .24, .32, .35, .37),
  income_top_range = c(9875, 40125, 85525, 163300, 207350, 518400, 1e1000)
)

income = 80000

df %>% 
  tibble::rownames_to_column() %>% 
  mutate(lag_income = lag(income_top_range, default = 0)) %>% 
  mutate(income_bracket = map2_lgl(lag_income, income_top_range, ~ between(income, .x, .y))) %>% 
  filter(rowname <= rowname[income_bracket == TRUE]) %>% 
  mutate(income_diff = map2_dbl(lag_income, income_top_range, ~ ifelse(.y > income, income - .x, .y - .x) )) %>% 
  select(-income_bracket, -rowname) %>% 
  mutate(tax_per_bracket = tax_rate * income_diff) %>% 
  summarize(tax_owed = sum(tax_per_bracket)) %>%
  mutate(effective_tax_rate = round(tax_owed/income, 2)) %>%
  mutate(income = income) %>% 
  View()
