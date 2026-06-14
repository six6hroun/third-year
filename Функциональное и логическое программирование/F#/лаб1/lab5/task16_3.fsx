System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let rec gcd a b =
    match b with
    | 0 -> a
    | _ -> gcd b (a % b)

let areCoprime a b = gcd a b = 1
let traverseDivisors n f init =
    let rec loop i acc =
        match i > n with
        | true  -> acc
        | false ->
            match n % i = 0 with
            | true  -> loop (i + 1) (f acc i)
            | false -> loop (i + 1) acc
    loop 1 init
let traverseDigits n f init =
    let rec loop n acc =
        match n with
        | 0 -> acc
        | _ -> loop (n / 10) (f acc (n % 10))
    loop n init

// ── Метод 1 

let method1 n =
    traverseDivisors n (fun acc i ->
        match i % 2 = 0 && not (areCoprime i n) with
        | true  -> acc + 1
        | false -> acc) 0

// ── Метод 2
let method2 n =
    traverseDigits n (fun acc d ->
        match d % 3 <> 0 with
        | true  -> max acc d
        | false -> acc) 0

// ── Метод 3
let smallestDivisor n =
    traverseDivisors n (fun acc i ->
        match i > 1 && (acc = 0 || i < acc) with
        | true  -> i
        | false -> acc) 0

let digitSumLessThan5 n =
    traverseDigits n (fun acc d ->
        match d < 5 with
        | true  -> acc + d
        | false -> acc) 0

let method3 n =
    let minDiv = smallestDivisor n
    let maxNotCoprimNotDivByMinDiv =
        traverseDivisors n (fun acc i ->
            match not (areCoprime i n) && i % minDiv <> 0 with
            | true  -> max acc i
            | false -> acc) 0
    let digSum = digitSumLessThan5 n
    match maxNotCoprimNotDivByMinDiv with
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