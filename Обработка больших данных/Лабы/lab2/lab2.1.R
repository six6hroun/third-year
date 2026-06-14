df <- read.csv("Lab2/ОтветыНаФорму.csv", stringsAsFactors = FALSE, na.strings = c("", "NA"))
df[, 2:11] <- df[, 2:11] / 10

print("Исходные данные:")
print(df)

Среднее <- sapply(df[2:11], mean, na.rm = TRUE)
статистика <- data.frame(
  Максимум = sapply(df[2:11], max, na.rm = TRUE),
  Минимум = sapply(df[2:11], min, na.rm = TRUE),
  Среднее = sapply(df[2:11], mean, na.rm = TRUE)
)
print("Статистика")
print(статистика)


предпочтения <- data.frame(
  больше_07 = colSums(df[2:11] > 0.7, na.rm = TRUE),
  меньше_03 = colSums(df[2:11] < 0.3, na.rm = TRUE)
)
print("Предпочтения")
print(предпочтения)


средние <- colMeans(df[2:11], na.rm = TRUE)
Рейтинг <- data.frame(
  рейтинг = sort(средние, decreasing = TRUE)
)
print("Рейтинг")
print(Рейтинг)

dfzero <- df
dfzero[is.na(dfzero)] <- 0
print("Замена NA на 0")
print(dfzero)

df_mean <- df
for (i in 2:11) {
  df_mean[is.na(df_mean[, i]), i] <- mean(df_mean[, i], na.rm = TRUE)
}
print("Замена NA на среднее арифметическое")
print(df_mean)


спортсмены <- df[df$Спорт >= 0.7 & !is.na(df$Спорт), ]
print("Выбор заядлых спорстменов")
print(спортсмены[,c(1,5)])

книги_сон <- df[df$Книги >= 0.5 & df$Сон <= 0.5 & !is.na(df$Книги) & !is.na(df$Сон),]
print("Выбор бодрых чтецов")
print(книги_сон[,c(1,4,6)])

#Столбчатая диаграмма
barplot(Среднее,
        main = "Средняя оценка времяпрепровождения",
        col = "grey",
        las = 2,
        ylim = c(0, 1))


library(ggplot2)
df_plot <- data.frame(
  Занятие = names(Среднее),
  среднее = Среднее
)

print(
  ggplot(df_plot, aes(x = Занятие, y = среднее)) +
    geom_bar(stat = "identity", fill = "grey") +
    ylim(0, 1) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    labs(title = "Средняя оценка Времяпрепровождения",
         x = "Занятия",
         y = "Средняя оценка")
)
