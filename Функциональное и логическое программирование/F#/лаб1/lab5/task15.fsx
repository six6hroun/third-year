System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let rec gcd a b =
    match b with
    | 0 -> a
    | _ -> gcd b (a%b)
let rec traverseIf n f init cond i =
    match i with
    | 0 -> init
    | _ ->
        match gcd n i, cond i with
        | 1, true -> traverseIf n f (f init i) cond (i-1)
        | _       -> traverseIf n f init cond (i-1)
let coprimeIf n f init cond = traverseIf n f init cond (n-1)
let main _ =
    coprimeIf 25 (fun a b -> a + b) 0 (fun d -> d > 8)
    |> printfn "Сумма взаимно простых с 25 > 8: %d"
    coprimeIf 42 (fun a _ -> a + 1) 0 (fun d -> d % 2 = 0)
    |> printfn "Кол-во чётных взаимно простых с 42: %d"
    coprimeIf 16 (fun a b -> match a > b with true -> a | false -> b) 0 (fun d -> d < 6)
    |> printfn "Максимум взаимно простых с 16 < 6: %d"
    coprimeIf 14 (fun a b -> a * b) 1 (fun d -> d % 2 <> 0)
    |> printfn "Произведение нечётных взаимно простых с 14: %d"
main ()