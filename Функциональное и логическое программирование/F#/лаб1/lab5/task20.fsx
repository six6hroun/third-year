System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let isEven n             = n % 2 = 0
let isDivisibleBy d n    = n % d = 0
let isNotDivisibleBy d n = not (isDivisibleBy d n)
let isGreaterThan min n  = n > min
let isLessThan max n     = n < max
let rec gcd a b =
    match b with
    | 0 -> a
    | _ -> gcd b (a % b)

let areNotCoprime a b = gcd a b > 1
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
let minDivisorWhere pred n =
    traverseDivisors n (accumulateIf pred (fun acc x ->
        match acc = 0 with
        | true  -> x
        | false -> match acc < x with | true -> acc | false -> x)) 0
let smallestDivisorGt1 n = minDivisorWhere (isGreaterThan 1) n
let method1 n =
    traverseDivisors n (countIf (fun i -> isEven i && areNotCoprime i n)) 0
let method2 n =
    traverseDigits n (accumulateIf (isNotDivisibleBy 3) takeMax) 0
let method3 n =
    let minDiv = smallestDivisorGt1 n
    let maxD =
        traverseDivisors n
            (accumulateIf (fun i -> areNotCoprime i n && isNotDivisibleBy minDiv i) takeMax) 0
    let digSum =
        traverseDigits n (accumulateIf (isLessThan 5) (fun acc d -> acc + d)) 0
    match maxD with
    | 0 -> 0
    | x -> x * digSum
let selectMethod num =
    match num with
    | 1 -> method1
    | 2 -> method2
    | 3 -> method3
    | _ -> fun _ -> -1
let readLine ()        = System.Console.ReadLine()
let parseTuple (s: string) =
    let parts = s.Split(' ')
    (int parts.[0], int parts.[1])
let applyMethod (num, arg) = selectMethod num arg
let printResult result     = printfn "Результат: %d" result
let mainCurrying _ =
    printfn "Введите номер метода и аргумент"
    readLine ()
    |> parseTuple
    |> applyMethod
    |> printResult
let pipeline = parseTuple >> applyMethod >> printResult
let mainComposition _ =
    printfn "Введите номер метода и аргумент через пробел:"
    (readLine >> pipeline) ()
printfn "С оператором каррирования"
mainCurrying ()
printfn ""
printfn "С оператором суперпозиции"
mainComposition ()