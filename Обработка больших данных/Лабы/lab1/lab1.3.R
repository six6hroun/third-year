metro <- data.frame(color = c("красная", "синяя", "зеленая", "оранжевая", "фиолетовая", "желтая", "черная"), length = c(10, 20, 30, 40, 50, 60, 70))

maxlenght <- max(metro$length)
minlenght <- min(metro$length)

maxcolor <- metro$color[metro$length == maxlenght]
mincolor <- metro$color[metro$length == minlenght]

print (paste(maxcolor, "ветка Московского метро — самая длинная. Ее протяженность составляет", maxlenght, "км."))
print (paste(mincolor, "ветка Московского метро — самая короткая. Ее протяженность составляет", minlenght, "км."))