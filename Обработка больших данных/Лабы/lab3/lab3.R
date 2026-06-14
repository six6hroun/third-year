library(learningtower)
student_data <- load_student("all")
countries <- c("USA", "DEU", "URY", "RUS", "TUR", "GEO", "CHN")
country_filter <- subset(student_data, country %in% countries & !is.na(math) & !is.na(read) & !is.na(science) & !is.na(computer))
View(country_filter)

mean_scores <- aggregate(cbind(math, read, science) ~ country + year, data = country_filter, FUN = mean, na.rm = TRUE)
print(mean_scores)

rus_scores <- mean_scores[mean_scores$country == "DEU", ]
plot(rus_scores$year, rus_scores$math, type = "b",pch = 16, col = "red", xlab = "Год", ylab = "Средний балл", main = "Динамика средних баллов PISA (Германия)", ylim = c(400, 550))
lines(rus_scores$year, rus_scores$read, type = "b", pch = 17,col = "blue")
lines(rus_scores$year, rus_scores$science, type = "b", pch = 18, col = "green")
legend("bottomright", legend = c("Математика", "Чтение", "Наука"), col = c("red", "blue", "green"), pch = c(16, 17, 18), lty = 1, title = "Предмет")


max_year <- max(mean_scores$year)
country_last <- mean_scores[mean_scores$country == "DEU" & mean_scores$year == max_year, ]
scores <- c(country_last$math, country_last$read, country_last$science)
names(scores) <- c("Математика", "Чтение", "Наука")
barplot(scores, col = c("red", "blue", "green"), main = paste("Средние баллы PISA в", max_year, "году (Германия)"), ylab = "Средний балл", ylim = c(0, 600))
text(x = 1:3, y = scores + 10, labels = round(scores, 1))


deu_filter <- aggregate(cbind(math, read, science) ~ country + year + gender, data = country_filter, FUN = mean, na.rm = TRUE)
deu_man <- deu_filter[deu_filter$country == "DEU" & deu_filter$gender == "male" & deu_filter$year == 2022,]
deu_wife <- deu_filter[deu_filter$country == "DEU" & deu_filter$gender == "female" & deu_filter$year == 2022,]
scores_man <- c(deu_man$math, deu_man$read, deu_man$science)
scores_wife <- c(deu_wife$math, deu_wife$read, deu_wife$science)

scores_man_percent <- round(scores_man / sum(scores_man) * 100, 1)
scores_wife_percent <- round(scores_wife / sum(scores_wife) * 100, 1)

labels_man <- paste(c("Математика", "Чтение", "Наука"), "\n", scores_man_percent, "%")
labels_wife <- paste(c("Математика", "Чтение", "Наука"), "\n", scores_wife_percent, "%")

colors_man <- c("red", "blue", "green")
colors_wife <- c("pink", "lightblue", "lightgreen")

par(mfrow = c(1,2))

pie(scores_man_percent, labels = labels_man, col = c("red", "blue", "green"), main = "Мужчины (Германия, 2022)")
legend("topright", legend = c("Математика","Чтение","Наука"), fill = colors_man, cex = 0.8)
pie(scores_wife_percent, labels = labels_wife, col = c("pink", "lightblue", "lightgreen"), main = "Женщины (Германия, 2022)")
legend("topright", legend = c("Математика","Чтение","Наука"), fill = colors_wife, cex = 0.8)

math_male <- subset(country_filter, country == "DEU" & gender == "male" & year == 2022)$math
hist(math_male, main = "Распределение оценок по математике (Мужчины, Германия, 2022)", xlab = "Баллы по математике", ylab = "Количество учеников", col = "lightblue", breaks = 10)
math_female <- subset(country_filter, country == "DEU" & gender == "female" & year == 2022)$math
hist(math_female, main = "Распределение оценок по математике (Женщины, Германия, 2022)", xlab = "Баллы по математике", ylab = "Количество учеников", col = "pink", breaks = 10)

par(mfrow = c(1,1))


deu <- mean_scores[mean_scores$country == "DEU", ]
usa <- mean_scores[mean_scores$country == "USA", ]
rus <- mean_scores[mean_scores$country == "RUS", ]
tur <- mean_scores[mean_scores$country == "TUR", ]
ury <- mean_scores[mean_scores$country == "URY", ]
geo <- mean_scores[mean_scores$country == "GEO", ]
chn <- mean_scores[mean_scores$country == "CHN", ]

plot(deu$year, deu$math, type = "b", pch = 16, col = "red", xlab = "Год", ylab = "Средний балл", main = "Динамика средних баллов PISA (Математика, 7 стран)", ylim = c(400, 550))
lines(usa$year, usa$math, type = "b", pch = 17, col = "blue")
lines(rus$year, rus$math, type = "b", pch = 18, col = "green")
lines(tur$year, tur$math, type = "b", pch = 19, col = "orange")
lines(ury$year, ury$math, type = "b", pch = 20, col = "purple")
lines(geo$year, geo$math, type = "b", pch = 21, col = "brown")
lines(chn$year, chn$math, type = "b", pch = 22, col = "pink")
legend("bottomright", legend = c("DEU","USA","RUS","TUR","URY","GEO","CHN"), col = c("red","blue","green","orange","purple","brown","pink"), pch = 16:22, lty = 1)



country_filter$computer_num <- ifelse(country_filter$computer == "yes", 1, 0)
years <- sort(unique(country_filter$year))
first_year <- years[1]
last_year <- years[length(years)]
middle_year <- years[ceiling(length(years)/2)]

mean_computers_first <- mean(country_filter$computer_num[country_filter$year == first_year], na.rm = TRUE)
mean_computers_middle <- mean(country_filter$computer_num[country_filter$year == middle_year], na.rm = TRUE)
mean_computers_last <- mean(country_filter$computer_num[country_filter$year == last_year], na.rm = TRUE)

computer_means <- c(mean_computers_first, mean_computers_middle, mean_computers_last)
names(computer_means) <- c(paste("Первый год", first_year), paste("Средний год", middle_year), paste("Последний год", last_year))

computer_percent <- round(computer_means / sum(computer_means) * 100, 1)

pie(computer_percent, labels = paste(names(computer_percent), "\n", computer_percent, "%"), col = c("red", "blue", "green"), main = "Доля учеников с компьютером по годам")

legend("topright", legend = names(computer_means), fill = c("red", "blue", "green"), cex = 0.8)