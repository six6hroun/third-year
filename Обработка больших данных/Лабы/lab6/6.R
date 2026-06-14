file_name <- "C:/POCAMESSD/RStudio/Db/Lab6/athlete_events (2).csv"

con <- file(file_name, open = "r", encoding = "latin1")
fields <- count.fields(con, sep = ",", quote = "\"")
close(con)

con <- file(file_name, open = "r", encoding = "latin1")
lines <- readLines(con, warn = FALSE)
close(con)

good_lines <- lines[!is.na(fields) & fields == 15]

data <- read.csv(
  text = good_lines,
  stringsAsFactors = FALSE,
  na.strings = c("NA", "")
)

data$Age <- as.numeric(data$Age)
data$Height <- as.numeric(data$Height)
data$Weight <- as.numeric(data$Weight)
data$Year <- as.numeric(data$Year)


alpha <- 0.05
sport1 <- "Archery"
sport2 <- "Shooting"
sex_to_compare <- "F"
mu0 <- 70


cat("\nЗадание 1: Дескриптивный анализ\n")
print(summary(data))

# Данные по выбранному виду спорта для задания 3
sport_data <- data[data$Sport == sport1 & !is.na(data$Weight), ]
weight1 <- sport_data$Weight


cat("\nЗадание 2: Проверка на нормальность и дисперсию\n")

# Подготовка данных для проверки нормальности (вес спортсменов)
weight_data <- na.omit(sport_data$Weight)

set.seed(123)
weight_sample <- sample(weight_data, min(5000, length(weight_data)))

# Тест Шапиро-Уилка на нормальность
shapiro_test <- shapiro.test(weight_sample)

# Визуализация распределения
hist(weight_sample,
     main = "Распределение веса спортсменов",
     xlab = "Вес, кг",
     col = "blue",
     border = "black")

qqnorm(weight_sample, main = "QQ-график веса спортсменов")
qqline(weight_sample, col = "red", lwd = 2)

# Проверка дисперсий для двухвыборочного теста (сравнение мужчин и женщин в Archery)
male_weight <- na.omit(sport_data$Weight[sport_data$Sex == "M"])
female_weight <- na.omit(sport_data$Weight[sport_data$Sex == "F"])

# F-тест для проверки равенства дисперсий
var_test <- var.test(male_weight, female_weight)


cat("\nРезультаты проверки нормальности\n")
if (shapiro_test$p.value > 0.05) {
  cat("Распределение можно считать нормальным (p-value =", shapiro_test$p.value, ")\n")
} else {
  cat("Распределение НЕ является нормальным (p-value =", shapiro_test$p.value, ")\n")
}

cat("\nРезультаты проверки дисперсий\n")
if (var_test$p.value > 0.05) {
  cat("Дисперсии можно считать равными (p-value =", var_test$p.value, ")\n")
} else {
  cat("Дисперсии различаются (p-value =", var_test$p.value, ")\n")
}

print(shapiro_test)
print(var_test)


cat("\nВывод о требуемом тесте для двухвыборочного сравнения\n")
if (shapiro_test$p.value > alpha) {
  if (var_test$p.value > alpha) {
    cat("Данные нормальны, дисперсии равны → используем классический t-тест\n")
  } else {
    cat("Данные нормальны, дисперсии НЕ равны → используем t-тест Уэлча\n")
  }
} else {
  cat("Данные НЕ нормальны → используем непараметрический критерий Уилкоксона\n")
}


cat("\nЗадание 3: Одновыборочный критерий\n")
cat("ОГ: средний вес спортсменов", sport1, "равен", mu0, "кг\n")

if (shapiro_test$p.value >= alpha) {
  result <- t.test(weight1, mu = mu0)
  cat("Используем t-тест (данные нормальны)\n")
} else {
  result <- wilcox.test(weight1, mu = mu0, exact = FALSE)
  cat("Используем критерий Уилкоксона (данные ненормальны)\n")
}

print(result)

if (result$p.value < alpha) {
  cat("ОГ отвергается. Средний вес статистически отличается от", mu0, "кг\n")
} else {
  cat("ОГ не отвергается. Нет оснований считать, что средний вес отличается от", mu0, "кг\n")
}


cat("\nЗадание 4: Двухвыборочный критерий\n")
cat("Сравнение веса спортсменок пола", sex_to_compare, "в видах спорта:", sport1, "и", sport2, "\n")
cat("ОГ: средний вес одинаков в двух видах спорта\n")

two_data <- data[
  data$Sport %in% c(sport1, sport2) &
    data$Sex == sex_to_compare &
    !is.na(data$Weight),
]
two_data$Sport <- factor(two_data$Sport)

# Проверка нормальности и дисперсий для двух выборок
w_archery <- two_data$Weight[two_data$Sport == sport1]
w_second <- two_data$Weight[two_data$Sport == sport2]

shapiro_archery <- shapiro.test(w_archery[1:min(5000, length(w_archery))])
shapiro_second <- shapiro.test(w_second[1:min(5000, length(w_second))])
var_test_two <- var.test(w_archery, w_second)

if (shapiro_archery$p.value > alpha & shapiro_second$p.value > alpha) {
  if (var_test_two$p.value > alpha) {
    cat("Используем t-тест\n")
    result2 <- t.test(Weight ~ Sport, data = two_data, var.equal = TRUE)
  } else {
    cat("Используем Уэлча\n")
    result2 <- t.test(Weight ~ Sport, data = two_data, var.equal = FALSE)
  }
} else {
  cat("Используем Уилкоксона\n")
  result2 <- wilcox.test(Weight ~ Sport, data = two_data, exact = FALSE)
}

print(result2)

if (result2$p.value < alpha) {
  cat("ОГ отвергается. Вес спортсменов в двух видах спорта статистически различается\n")
} else {
  cat("ОГ не отвергается. Статистически значимого различия веса не обнаружено\n")
}