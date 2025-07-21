# 1. 读取数据
ai <- read.csv("D:/GITHUB/course/modules/early-problems/ai_bug_fixing_times.csv")
no_ai <- read.csv("D:/GITHUB/course/modules/early-problems/no_ai_bug_fixing_times.csv")

# 2. 添加分组标签
ai$Group <- "AI"
no_ai$Group <- "No_AI"

# 3. 合并数据
data <- rbind(
  ai[, c("Time..minutes.", "Bug.Type", "Group")],
  no_ai[, c("Time..minutes.", "Bug.Type", "Group")]
)
colnames(data) <- c("Time", "BugType", "Group")

# 4. 描述性统计
library(dplyr)
summary_stats <- data %>%
  group_by(Group) %>%
  summarise(
    count = n(),
    mean_time = mean(Time),
    median_time = median(Time),
    sd_time = sd(Time)
  )
print(summary_stats)

# 5. 可视化
library(ggplot2)
ggplot(data, aes(x=Group, y=Time, fill=Group)) +
  geom_boxplot() +
  labs(title="Bug Fixing Time: AI vs No AI", y="Time (minutes)") +
  theme_minimal()

# 6. 按Bug类型分组统计
by_type_stats <- data %>%
  group_by(Group, BugType) %>%
  summarise(
    count = n(),
    mean_time = mean(Time),
    median_time = median(Time),
    sd_time = sd(Time)
  )
print(by_type_stats)

# 7. 按Bug类型分组可视化
ggplot(data, aes(x=BugType, y=Time, fill=Group)) +
  geom_boxplot(position=position_dodge(0.8)) +
  labs(title="Bug Fixing Time by Bug Type", y="Time (minutes)") +
  theme_minimal()

# 8. 统计检验（t检验）
t_test_result <- t.test(
  Time ~ Group,
  data = data
)
print(t_test_result)

# 9. 按Bug类型分别做t检验
for (bug_type in unique(data$BugType)) {
  cat("\nBug Type:", bug_type, "\n")
  sub_data <- subset(data, BugType == bug_type)
  print(t.test(Time ~ Group, data = sub_data))
}