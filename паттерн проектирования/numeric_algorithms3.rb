def max_prime_factor(a)
    max_prime = 0
    for i in 1..a do
        if a % i == 0 then
            count = 0
            for j in 1..i do
                if i % j == 0 then
                    count += 1
                end
            end
            if count == 2 then
                if i > max_prime then 
                    max_prime = i
                end
            end
        end
    end
    return max_prime
end

def non_five_product (a)
    products = 1
    while a > 0
        digits = a % 10
        if digits % 5 != 0 then
            products *= digits
        end
        a /= 10
    end
    return products
end

def gcd_odd_composite_product(a)
    max = 1
    has_odd_composite = false
    for i in 1..a do
        if a % i == 0 and i % 2 == 1 then
            count=0
            for j in 1..i do
                if i % j == 0 then
                    count += 1
                end
            end
            if count != 2 then
                if i > max then 
                max = i
                has_odd_composite = true
                end
            end
        end
    end
    return nil unless has_odd_composite

    product = 1
    clon = a
    while clon > 0
        digit = clon % 10
        product *= digit
        clon /= 10
    end

    maximum = 1
    if product < max then
        for i in 1..product do
        if product % i == 0 and max % i == 0 then
            if i > maximum then
            maximum = i
            end
        end
        end
    else
        for i in 1..max do
        if product % i == 0 and max % i == 0 then
            if i > maximum then
            maximum = i
            end
        end
        end
    end
    return maximum
end

number_metod = ARGV[0].to_i
source = ARGV[1]

if source == "keyboard" then
    ARGV.clear
    print "Введите число - "
    value = gets.chomp.to_i
elsif source == "file"
    print "Укажите путь к файлу: "
    file_value = ARGV[2]
    value = File.read(file_value).to_i
else
    puts "Неизвестно, откуда считывать данные."
end
    
case number_metod
when 1
    puts "Максимальный простой делитель числа #{value}"
    puts "Ответ - #{max_prime_factor(value)}"
when 2
    puts "Произведение цифр числа #{value} не делящихся на 5"
    puts "Ответ - #{non_five_product(value)}"
when 3
    puts "НОД максимального нечетного непростого делителя числа и произведение цифр числа #{value}"
    puts "Ответ - #{gcd_odd_composite_product(value)}"
end