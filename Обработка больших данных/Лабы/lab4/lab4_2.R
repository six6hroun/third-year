library(rvest)
library(dplyr)
library(stringr)
library(purrr)

# 1. Загрузка главной страницы со списком экскурсий

base_url <- "https://www.sputnik8.com"
main_page_url <- paste0(base_url, "/ru/moscow")

cat("Загрузка главной страницы...\n")
main_page <- read_html(main_page_url, encoding = "UTF-8")

# 2. Извлечение ссылок на страницы отдельных экскурсий

all_links <- main_page %>% html_nodes("a") %>% html_attr("href")
all_links <- unique(all_links[!is.na(all_links)])

tour_links <- all_links[grepl("^/ru/moscow/[a-z0-9-]+$", all_links)]

tour_urls <- paste0(base_url, tour_links)
tour_urls <- unique(tour_urls)

cat("Найдено экскурсий:", length(tour_urls), "\n")

if (length(tour_urls) == 0) {
  cards <- main_page %>% html_nodes(".tour-card, .excursion-card, [class*='tour'], [class*='card']")
  tour_links <- cards %>% html_nodes("a") %>% html_attr("href")
  tour_links <- unique(tour_links[!is.na(tour_links)])
  tour_links <- tour_links[grepl("^/ru/moscow/", tour_links)]
  tour_urls <- paste0(base_url, tour_links)
  tour_urls <- unique(tour_urls)
  cat("Альтернативный поиск. Найдено экскурсий:", length(tour_urls), "\n")
}

max_tours <- 20
if (length(tour_urls) > max_tours) {
  cat("Слишком много экскурсий, ограничиваем первыми", max_tours, "\n")
  tour_urls <- tour_urls[1:max_tours]
}

# 3. Функция извлечения данных со страницы экскурсии

extract_tour_info <- function(tour_url, delay = 1) {
  Sys.sleep(delay)  # вежливая пауза
  cat("Обрабатывается:", tour_url, "\n")
  
  tryCatch({
    tour_page <- read_html(tour_url, encoding = "UTF-8")
    
    # Название — обычно в h1
    title <- tour_page %>% 
      html_nodes("h1") %>% 
      html_text() %>% 
      .[1] %>% 
      str_trim()
    
    # Описание — первый параграф с текстом (может быть несколько)
    description <- tour_page %>% 
      html_nodes("div[class*='description'], div[class*='about'], p") %>% 
      html_text() %>% 
      paste(collapse = " ") %>% 
      str_trim() %>% 
      str_replace_all("\\s+", " ") %>% 
      substr(1, 500)  # ограничим длину
    
    # Адрес (место встречи) — часто в блоке с иконкой "location" или в атрибуте
    address <- "Адрес не указан"
    # Поиск по тексту: "Место встречи:", "Адрес:"
    address_elem <- tour_page %>% 
      html_nodes(xpath = "//*[contains(text(), 'Место встречи')]/following-sibling::*")
    if (length(address_elem) > 0) {
      address <- address_elem %>% html_text() %>% .[1] %>% str_trim()
    } else {
      address_elem <- tour_page %>% 
        html_nodes(xpath = "//*[contains(text(), 'Адрес')]/following-sibling::*")
      if (length(address_elem) > 0) {
        address <- address_elem %>% html_text() %>% .[1] %>% str_trim()
      }
    }
    # Если не нашли, пробуем искать по классам
    if (address == "Адрес не указан") {
      loc <- tour_page %>% html_nodes("[class*='location'], [class*='address']") %>% html_text()
      if (length(loc) > 0) address <- loc[1] %>% str_trim()
    }
    
    # Длительность — обычно в часах/минутах
    duration <- "Не указана"
    duration_elem <- tour_page %>% 
      html_nodes(xpath = "//*[contains(text(), 'Длительность')]/following-sibling::*")
    if (length(duration_elem) > 0) {
      duration <- duration_elem %>% html_text() %>% .[1] %>% str_trim()
    } else {
      # Поиск по классам
      dur <- tour_page %>% html_nodes("[class*='duration']") %>% html_text()
      if (length(dur) > 0) duration <- dur[1] %>% str_trim()
    }
    
    # Цена — ищем числа с валютой
    price <- "Не указана"
    price_elem <- tour_page %>% 
      html_nodes(xpath = "//*[contains(text(), 'Цена')]/following-sibling::*")
    if (length(price_elem) > 0) {
      price <- price_elem %>% html_text() %>% .[1] %>% str_trim()
    } else {
      # Поиск по классам, часто в элементе с классом price
      pr <- tour_page %>% html_nodes("[class*='price']") %>% html_text()
      if (length(pr) > 0) price <- pr[1] %>% str_trim()
    }
    start_time <- "Не указано"
    start_elem <- tour_page %>% 
      html_nodes(xpath = "//*[contains(text(), 'Начало')]/following-sibling::*")
    if (length(start_elem) > 0) {
      start_time <- start_elem %>% html_text() %>% .[1] %>% str_trim()
    }
    if (start_time == "Не указано") {
      start_text <- tour_page %>% html_text() %>% str_extract("Начало в \\d{1,2}:\\d{2}")
      if (!is.na(start_text)) start_time <- start_text
    }
    
    end_time <- "Не указано"
    if (start_time != "Не указано" && duration != "Не указана") {
      # Попытка извлечь число часов из duration
      hours <- str_extract(duration, "\\d+(?=\\s*ч)")
      if (!is.na(hours)) {
        start_hour <- as.numeric(str_extract(start_time, "\\d{1,2}"))
        if (!is.na(start_hour)) {
          end_hour <- start_hour + as.numeric(hours)
          end_time <- paste0(end_hour, str_extract(start_time, ":\\d{2}"))
        }
      }
    }
    
    data.frame(
      Название = ifelse(length(title) == 0, "Не указано", title),
      Адрес = address,
      Описание = description,
      Ссылка = tour_url,
      Время_начала = start_time,
      Окончание = end_time,
      Длительность = duration,
      Цена = price,
      stringsAsFactors = FALSE
    )
  }, error = function(e) {
    cat("Ошибка при загрузке", tour_url, ":", e$message, "\n")
    data.frame(
      Название = "Ошибка загрузки",
      Адрес = "",
      Описание = paste("Ошибка:", substr(e$message, 1, 100)),
      Ссылка = tour_url,
      Время_начала = "",
      Окончание = "",
      Длительность = "",
      Цена = "",
      stringsAsFactors = FALSE
    )
  })
}

# 4. Сбор данных по всем экскурсиям

tours_list <- list()
for (i in seq_along(tour_urls)) {
  tours_list[[i]] <- extract_tour_info(tour_urls[i], delay = 1)  # 1 секунда между запросами
}

tours_df <- bind_rows(tours_list)

tours_df <- tours_df %>% distinct(Название, .keep_all = TRUE)

output_file <- "moscow_tours.csv"
write.csv2(tours_df, output_file, row.names = FALSE, fileEncoding = "UTF-8")
cat("\n✅ Собрано экскурсий:", nrow(tours_df), "\n")
cat("✅ Файл сохранен:", output_file, "\n")

print(head(tours_df))