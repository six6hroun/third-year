install.packages("factoextra")
install.packages("cluster")
install.packages("parameters")
install.packages("NbClust")
install.packages("mclust")
install.packages("lattice")
install.packages("scatterplot3d")
install.packages("ggplot2")
install.packages("dplyr")
install.packages("tidyr")
install.packages("tibble")
install.packages("broom")

library(factoextra)
library(cluster)
library(parameters)
library(NbClust)
library(mclust)
library(lattice)
library(scatterplot3d)
library(ggplot2)
library(dplyr)
library(tidyr)
library(tibble)
library(broom)

data <- read.csv("C:/POCAMESSD/RStudio/Db/Lab5.1/Food_Preference.csv")

summary(data)

colSums(is.na(data))

data_clean <- data[, -c(1,2)]

# Преобразуем категориальные признаки в числа
data_clean[] <- lapply(data_clean, function(x) as.numeric(as.factor(x)))

# Нормализация данных
data_scaled <- scale(data_clean)

# Определение оптимального числа кластеров
set.seed(123)

# Метод локтя
fviz_nbclust(
  data_scaled,
  kmeans,
  method = "wss",
  k.max = 10
) +
  labs(
    title = "Метод локтя",
    x = "Количество кластеров",
    y = "WSS"
  )

# Метод силуэта
fviz_nbclust(
  data_scaled,
  kmeans,
  method = "silhouette",
  k.max = 10
) +
  labs(
    title = "Метод силуэта",
    x = "Количество кластеров",
    y = "Silhouette"
  )

# Gap statistic
gap_stat <- clusGap(
  data_scaled,
  FUN = kmeans,
  K.max = 10,
  B = 10
)

fviz_gap_stat(gap_stat) +
  labs(
    title = "Gap Statistic",
    x = "Количество кластеров",
    y = "Gap"
  )

# Консенсус
n_clust <- parameters::n_clusters(
  data_clean,
  package = c("NbClust", "mclust", "easystats"),
  standardize = TRUE
)

plot(n_clust)

# Иерархическая кластеризация
# Матрица расстояний
dist_data <- dist(data_scaled)

# Иерархическая кластеризаци
clust_data <- hclust(dist_data, method = "ward.D")

# Дендрограмма
plot(
  clust_data,
  main = "Дендрограмма",
  xlab = "Объекты",
  sub = "",
  cex = 0.6
)

# Выделение 3 кластеров
rect.hclust(clust_data, k = 3, border = "red")

# Разделение на 3 кластера
groups <- cutree(clust_data, k = 3)

# Добавим кластеры в датасет
data$Cluster <- as.factor(groups)

# Анализ кластеров
# Средние значения признаков
aggregate(data_clean, by = list(Cluster = groups), mean)

# Столбчатая диаграмма кластеров
cluster_means <- aggregate(data_clean, by = list(Cluster = groups), mean)

cluster_matrix <- as.matrix(cluster_means[, -1])
rownames(cluster_matrix) <- paste("Cluster", cluster_means$Cluster)

barplot(
  t(cluster_matrix),
  beside = TRUE,
  col = rainbow(ncol(cluster_matrix)),
  main = "Сравнение кластеров",
  legend.text = TRUE
)

# Boxplot
boxplot(
  Age ~ Cluster,
  data = data,
  main = "Возраст по кластерам",
  col = "lightblue"
)

# K-means кластеризация
set.seed(123)
km_res <- kmeans(data_scaled, centers = 3, nstart = 10)

# Визуализация кластеров
fviz_cluster(
  km_res,
  data = data_scaled,
  ellipse.type = "norm",
  main = "K-means кластеризация"
)

# Scatterplot
pairs(
  data_clean,
  main = "Матрица диаграмм рассеяния",
  col = groups
)

# Трехмерная визуализация
colors <- c("red", "green", "blue")
colors <- colors[groups]

s3d <- scatterplot3d(
  data_clean[,1:3],
  color = colors,
  pch = 16,
  main = "3D кластеризация"
)

legend(
  "topright",
  legend = c("Cluster 1", "Cluster 2", "Cluster 3"),
  col = c("red", "green", "blue"),
  pch = 16
)
