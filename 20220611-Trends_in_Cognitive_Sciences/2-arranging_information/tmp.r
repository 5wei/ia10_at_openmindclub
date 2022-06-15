
tics_path = "D:/INFO_SPACE/1/20220611-Trends_in_Cognitive_Sciences/2/TiCS_articles_metadata.bib"
tics_doi_path = "D:/INFO_SPACE/1/20220611-Trends_in_Cognitive_Sciences/2/TiCS_doi.csv"

if(!isTRUE(require("bibliometrix"))){install.packages("bibliometrix")}
if(!isTRUE(require("dplyr"))){install.packages("dplyr")}
library(bibliometrix)
library(dplyr)

df_tics <- convert2df(file = tics_path, dbsource = "wos", format = "bibtex")

df_doi <- df_tics %>%
    select(DI)

# 为什么 DI 会分成两个字段？
write.csv(df_doi , tics_doi_path)