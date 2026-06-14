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

let method1 n =
    traverseDivisors n (fun acc i ->
        match i % 2 = 0 && not (areCoprime i n) with
        | true  -> acc + 1
        | false -> acc) 0

let main _ =
    printfn "Количество четных чисел не взаимно простых с данным"
    method1 12  |> printfn "  12  -> %d"
main ()