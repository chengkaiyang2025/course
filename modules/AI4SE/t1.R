# Titanic EDA in R

# Load necessary libraries
library(readr)
library(dplyr)
library(ggplot2)

# Read the Titanic dataset
# Adjust the path if running from a different working directory
titanic <- read_csv("../../assignments/slides/titanic.csv")

# Show the first few rows
glimpse(titanic)

# Descriptive statistics
summary(titanic)

# Count of survivors vs non-survivors
print(table(titanic$Survived))

# Survival rate by sex
titanic %>%
  group_by(Sex) %>%
  summarise(SurvivedRate = mean(Survived, na.rm=TRUE),
            Count = n()) %>%
  print()

# Plot: Survival rate by class
p1 <- ggplot(titanic, aes(x = factor(Pclass), fill = factor(Survived))) +
  geom_bar(position = "fill") +
  labs(x = "Pclass", y = "Proportion", fill = "Survived", title = "Survival Rate by Class")
print(p1)

# Plot: Age distribution by survival
p2 <- ggplot(titanic, aes(x = Age, fill = factor(Survived))) +
  geom_histogram(binwidth = 5, position = "identity", alpha = 0.6) +
  labs(x = "Age", y = "Count", fill = "Survived", title = "Age Distribution by Survival")
print(p2) 