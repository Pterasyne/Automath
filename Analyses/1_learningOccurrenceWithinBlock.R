library(lme4) 
library(lattice)
library(tidyverse) #or simply library(dplyr)
data <- read.csv("production_final.csv")

data <- data %>%
  mutate(
    participant_code = as.factor(participant_code),
    problem = as.factor(problem),
    seance = as.integer(seance),
    block_id = floor(seance / 6) #+5% more "hard" (sum>10) problems
  )

data <- data %>%
  arrange(participant_code, problem, date_fr) %>%
  group_by(participant_code, problem, block_id) %>%
  mutate(occurrence = row_number()) %>%
  ungroup()

model <- lmer(
  reaction_time ~ occurrence * block_id +
    (1 | participant_code) + 
    (1 | problem),
  data = data
)

print(summary(model))
anova(model)
dotplot(ranef(model, condVar=TRUE))



dataType <- data %>%
  mutate(type = if_else(pmax(num1, num2) <= 4, 0, 1))  %>% #small=0 and big=1
  filter((num1 != 1 & num2 != 1) & (num1 != num2))

modelType <- lmer(
  reaction_time ~ occurrence * block_id * type  +
    (1 | participant_code),
  data = dataType
)

print(summary(modelType))
anova(modelType)
dotplot(ranef(modelType, condVar=TRUE))



dataWithAuto <- data %>%
  mutate(type = if_else(pmax(num1, num2) <= 4, 0, 1))  %>% #small=0 and big=1
  filter((num1 != 1 & num2 != 1) & (num1 != num2) & (stillAutomatized==1|stillNonAutomatized==0))

modelWithAuto <- lmer(
  reaction_time ~ occurrence * block_id * stillAutomatized +
    (1 | participant_code) + 
    (1 | problem),
  data = dataWithAuto
)

print(summary(modelWithAuto))
anova(modelWithAuto)
dotplot(ranef(modelWithAuto, condVar=TRUE))
