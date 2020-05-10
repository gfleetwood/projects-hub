library(magick)
library(magrittr)  

c <- magick::image_read("pic.png") 

c %>% 
  image_annotate("Words", size = 16, color = "white", location = "+45+160") %>% 
  image_write("pic2.png")
