library(officer)
library(glue)
library(readr)

save_slide <- function(slide, slides, file, file_name){
  
  to_remove = purrr::discard(slides, ~ .x == slide)
  
  temp = officer::read_pptx(file)
  temp <- move_slide(temp, index = slide, to = 1)
  garbage = purrr::map(to_remove, ~ officer::remove_slide(temp, 2))
  
  fname = glue("~/../Documents/projects/slides/intermediate/{name}/slides/{name}_slide_{slide}.pptx")
  df = slide_summary(temp, index = 1)[,c("type", "ph_label", "text")]
  print(temp, target = fname) 
  write_csv(glue("~/../Documents/projects/slides/intermediate/{name}/meta_data/{name}_slide_{slide}.csv"))
  
  return('Done')
  
}

name = "test"
ppt = glue("~/../Desktop/me/slides/input/{name}.pptx")

pp = officer::read_pptx(ppt)
slide_nums = seq(1, length(pp), 1)
temp = purrr::map_chr(slide_nums, ~ save_slide(.x, slide_nums, ppt, name))
