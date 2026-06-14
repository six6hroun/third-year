System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let isEven n             = n % 2 = 0
let isOdd n              = not (isEven n)
let isDivisibleBy d n    = n % d = 0
let isNotDivisibleBy d n = not (isDivisibleBy d n)
let isGreaterThan min n  = n > min
let isLessThan max n     = n < max
let rec gcd a b =
    match b with
    | 0 -> a
    | _ -> gcd b (a % b)
let areCoprime a b    = gcd a b = 1
let areNotCoprime a b = not (areCoprime a b)
let traverseDivisors n f init =
    let rec loop i acc =
        match i > n with
        | true  -> acc
        | false ->
            match isDivisibleBy i n with
            | true  -> loop (i + 1) (f acc i)
            | false -> loop (i + 1) acc
    loop 1 init
let traverseDigits n f init =
    let rec loop n acc =
        match n with
        | 0 -> acc
        | _ -> loop (n / 10) (f acc (n % 10))
    loop n init
let accumulateIf pred f acc x =
    match pred x with
    | true  -> f acc x
    | false -> acc
let countIf pred acc x =
    match pred x with
    | true  -> acc + 1
    | false -> acc
let takeMax acc x = match acc > x with | true -> acc | false -> x
let takeMin acc x = match acc < x with | true -> acc | false -> x
let maxDivisorWhere pred n   = traverseDivisors n (accumulateIf pred takeMax) 0
let minDivisorWhere pred n   = traverseDivisors n (accumulateIf pred (fun acc x ->
                                    match acc = 0 with
                                    | true  -> x
                                    | false -> takeMin acc x)) 0
let countDivisorsWhere pred n = traverseDivisors n (countIf pred) 0
let digitSumWhere pred n  = traverseDigits n (accumulateIf pred (fun acc d -> acc + d)) 0
let maxDigitWhere pred n  = traverseDigits n (accumulateIf pred takeMax) 0
let isEvenDivisor       n i = isEven i
let isNotCoprimeTo      n i = areNotCoprime i n
let isEvenNotCoprimeTo  n i = isEven i && areNotCoprime i n
let isDigitNotDivBy3 d = isNotDivisibleBy 3 d
let isDigitLessThan5 d = isLessThan 5 d
let smallestDivisorGt1 n = minDivisorWhere (isGreaterThan 1) n
let isNotCopimeAndNotDivBySmallest n i =
    areNotCoprime i n && isNotDivisibleBy (smallestDivisorGt1 n) i
let method1 n = countDivisorsWhere (isEvenNotCoprimeTo n) n
let method2 n = maxDigitWhere isDigitNotDivBy3 n
let maxNotCoprimeNotDivBySmallest n =
    maxDivisorWhere (isNotCopimeAndNotDivBySmallest n) n
let digitSumLessThan5 n = digitSumWhere isDigitLessThan5 n
let method3 n =
    let d      = maxNotCoprimeNotDivBySmallest n
    let digSum = digitSumLessThan5 n
    match d with
    | 0 -> 0
    | x -> x * digSum
let main _ =
    printfn "Количество четных чисел не взаимно простых с данным"
    method1 12  |> printfn "  12  -> %d"

    printfn "\nНайти максимальную цифры числа, не делящуюся на 3"
    method2 123456789 |> printfn "  123456789 -> %d"

    printfn "\nНайти произведение максимального числа, не взаимно простого
    с данным, не делящегося на наименьший делитель исходно числа, и
    суммы цифр числа, меньших 5"
    method3 12  |> printfn "  12  -> %d"
main ()