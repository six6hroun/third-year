library(rvest)
library(dplyr)
library(ggplot2)
library(tidyr)
library(stringr)

folder_path <- "C:/POCAMESSD/RStudio/Db/Lab4/numbeo_pages/"
html_files <- list.files(folder_path, pattern = "\\.html$", full.names = TRUE)

print(paste("Найдено HTML-файлов:", length(html_files)))
if (length(html_files) > 0) {
  print("Первые 3 файла:")
  print(head(basename(html_files), 3))
}

extract_numbeo_data <- function(file_path) {
  year <- as.numeric(str_extract(basename(file_path), "\\d{4}"))
  if (is.na(year)) return(NULL)
  
  page <- read_html(file_path)
  tables <- page %>% html_nodes("table")
  
  if (length(tables) < 2) return(NULL)
  
  suppressWarnings({
    df <- tables[[2]] %>% html_table(fill = TRUE) %>% as.data.frame()
    colnames(df) <- as.character(df[1, ])
    df <- df[-1, ]
    
    if (ncol(df) >= 11) {
      names(df)[1:11] <- c("Rank", "Country", "Quality_of_Life_Index", 
                           "Purchasing_Power_Index", "Safety_Index", 
                           "Health_Care_Index", "Cost_of_Living_Index", 
                           "Property_Price_to_Income_Ratio", 
                           "Traffic_Commute_Time_Index", 
                           "Pollution_Index", "Climate_Index")
    } else {
      names(df)[1:min(11, ncol(df))] <- c("Rank", "Country", "Quality_of_Life_Index", 
                                          "Purchasing_Power_Index", "Safety_Index")[1:min(5, ncol(df)-1)]
    }
    
    df$Year <- year
    
    # Преобразуем числовые столбцы
    numeric_cols <- names(df)[grepl("Index|Ratio", names(df))]
    for (col in numeric_cols) {
      if (col %in% names(df)) {
        df[[col]] <- suppressWarnings(as.numeric(as.character(df[[col]])))
      }
    }
  })
  return(df)
}

target_countries <- c("United States", "Germany", "Uruguay", "Russia", "China")

all_data <- data.frame()

for (file in html_files) {
  df <- extract_numbeo_data(file)
  if (!is.null(df) && nrow(df) > 0) {
    df_filtered <- df %>% filter(Country %in% target_countries)
    if (nrow(df_filtered) > 0) {
      cat("Найдены данные для", unique(df_filtered$Country), "в файле", basename(file), "\n")
      all_data <- bind_rows(all_data, df_filtered)
    }
  }
}

if (nrow(all_data) == 0) {
  stop("Не удалось загрузить данные. Проверьте названия стран в HTML-файлах.")
}

all_data <- all_data %>%
  mutate(Country_Ru = case_when(
    Country == "United States" ~ "США",
    Country == "Germany" ~ "Германия",
    Country == "Uruguay" ~ "Уругвай",
    Country == "Russia" ~ "Россия",
    Country == "China" ~ "Китай",
    TRUE ~ Country
  ))

all_data$Year <- as.numeric(all_data$Year)

write.csv2(all_data, "numbeo_my_variant.csv", row.names = FALSE, fileEncoding = "UTF-8")
cat("\n Данные сохранены в numbeo_my_variant.csv\n")

# 2. Визуализация: динамика индекса качества жизни

p1 <- ggplot(all_data, aes(x = Year, y = Quality_of_Life_Index, 
                           color = Country_Ru, group = Country_Ru)) +
  geom_line(size = 1.2) +
  geom_point(size = 2.5) +
  labs(title = "Динамика индекса качества жизни (2014-2026)",
       subtitle = "Страны: США, Германия, Уругвай, Россия, Китай",
       x = "Год", y = "Индекс качества жизни", color = "Страна") +
  theme_minimal() +
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5))

ggsave("quality_of_life_comparison.png", p1, width = 10, height = 6)
cat("✅ График сохранен: quality_of_life_comparison.png\n")
# 3. Фасетный график: все показатели

# Выбираем только те показатели, которые есть в данных
available_indicators <- names(all_data)[grepl("Index|Ratio", names(all_data))]

indicators_long <- all_data %>%
  select(Year, Country_Ru, all_of(available_indicators)) %>%
  pivot_longer(cols = -c(Year, Country_Ru), names_to = "Indicator", values_to = "Value") %>%
  filter(!is.na(Value))

indicator_names <- c(
  "Quality_of_Life_Index" = "Качество жизни",
  "Purchasing_Power_Index" = "Покупательная способность",
  "Safety_Index" = "Безопасность",
  "Health_Care_Index" = "Здравоохранение",
  "Cost_of_Living_Index" = "Стоимость жизни",
  "Property_Price_to_Income_Ratio" = "Цена жилья/доход",
  "Traffic_Commute_Time_Index" = "Время в пути",
  "Pollution_Index" = "Загрязнение",
  "Climate_Index" = "Климат"
)

indicators_long$Indicator_Ru <- indicator_names[indicators_long$Indicator]
indicators_long <- indicators_long %>% filter(!is.na(Indicator_Ru))

if (nrow(indicators_long) > 0) {
  facet_plot <- ggplot(indicators_long, aes(x = Year, y = Value, 
                                            color = Country_Ru, group = Country_Ru)) +
    geom_line() +
    geom_point(size = 0.8) +
    facet_wrap(~Indicator_Ru, scales = "free_y", ncol = 3) +
    labs(title = "Динамика показателей качества жизни (2014-2026)",
         x = "Год", y = "Значение индекса", color = "Страна") +
    theme_minimal() +
    theme(legend.position = "bottom",
          strip.text = element_text(size = 9),
          axis.text.x = element_text(angle = 45, hjust = 1))
  
  ggsave("all_indicators_facet.png", facet_plot, width = 14, height = 10)
  cat("✅ График сохранен: all_indicators_facet.png\n")
}

# 4. Статистика: средние значения за весь период

stats <- all_data %>%
  group_by(Country_Ru) %>%
  summarise(
    Качество_жизни = round(mean(Quality_of_Life_Index, na.rm = TRUE) / 10, 1),
    Покупательная_способность = round(mean(Purchasing_Power_Index, na.rm = TRUE) / 10, 1),
    Безопасность = round(mean(Safety_Index, na.rm = TRUE) / 10, 1),
    Здравоохранение = round(mean(Health_Care_Index, na.rm = TRUE) / 10, 1),
    Загрязнение = round(mean(Pollution_Index, na.rm = TRUE) / 10, 1),
    Климат = round(mean(Climate_Index, na.rm = TRUE) / 10, 1)
  ) %>%
  arrange(desc(Качество_жизни))

print("Средние значения показателей по странам (2014-2026):")
print(stats)

# 5. Динамика изменений (рост/падение)

min_year <- min(all_data$Year, na.rm = TRUE)
max_year <- max(all_data$Year, na.rm = TRUE)

changes <- all_data %>%
  filter(Year %in% c(min_year, max_year)) %>%
  group_by(Country_Ru) %>%
  filter(n() == 2) %>%
  summarise(
    Качество_жизни_рост = round((Quality_of_Life_Index[Year == max_year] - 
                                   Quality_of_Life_Index[Year == min_year]) / 
                                  Quality_of_Life_Index[Year == min_year] * 10, 1),
    Покупательная_способность_рост = round((Purchasing_Power_Index[Year == max_year] - 
                                              Purchasing_Power_Index[Year == min_year]) / 
                                             Purchasing_Power_Index[Year == min_year] * 10, 1),
    .groups = "drop"
  ) %>%
  arrange(desc(Качество_жизни_рост))

print("Изменение показателей за период (%):")
print(changes)

cat("\n Анализ завершен. Сохранены файлы:\n")
cat("- numbeo_my_variant.csv\n")
cat("- quality_of_life_comparison.png\n")
cat("- all_indicators_facet.png\n")
cat("- heatmap_countries.png\n")