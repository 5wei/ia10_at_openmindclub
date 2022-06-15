# 假设 data frame M 已经有 DI 字段了

if(!isTRUE(require("readr"))){install.packages("readr")}
if(!isTRUE(require("stringr"))){install.packages("stringr")}
if(!isTRUE(require("dplyr"))){install.packages("dplyr")}
if(!isTRUE(require("RCurl"))){install.packages("RCurl")}
if(!isTRUE(require("magrittr"))){install.packages("magrittr")}
if(!isTRUE(require("jsonlite"))){install.packages("jsonlite")}
library(readr)
library(stringr)
library(dplyr)
library(magrittr)
library(RCurl)
library(jsonlite)

getAltmetricScore <- function(doi, api = "https://api.altmetric.com/v1/doi/") {
	Sys.sleep(runif(n= 1, min = 0, max = 1))
	httpGET(paste0(api,doi)) %>% 
		parse_json() %>% 
		extract2("score")
}

df_with_score <- M %>% select(DI) %>% 
    mutate(altmetric_score = lapply(DI, function(z) try(getAltmetricScore(z)))) %>% 
    mutate(altmetric_score = str_replace(altmetric_score,"Error ",replacement = ""))

df_with_score_desc <- df_with_score %>% filter(!grepl('Error', altmetric_score) && !grepl('Not Found', altmetric_score)) %>% left_join(M, by = "DI") %>% select(DI, TI, altmetric_score) %>% arrange(desc(altmetric_score))

# 输出成 csv
write.csv(df_with_score_desc ,"altmetric_score_desc.csv")
