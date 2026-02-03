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