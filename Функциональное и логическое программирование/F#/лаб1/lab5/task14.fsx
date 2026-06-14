System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let rec gcd a b =
    match b with
    | 0 -> a
    | _ -> gcd b (a%b)
let rec traverse n f init i =
    match i with
    | 0 -> init
    | _ ->
        match gcd n i with
        | 1 -> traverse n f (f init i) (i-1)
        | _ -> traverse n f init (i-1)

let coprime n f init = traverse n f init (n-1)
let eulerFunction n = coprime n (fun a _ -> a + 1) 0
let main _ =
    printfn "Результаты:"
    eulerFunction 1  |> printfn "φ(1)  = %d"  
    eulerFunction 2  |> printfn "φ(2)  = %d"  
    eulerFunction 3  |> printfn "φ(3)  = %d" 
    eulerFunction 4  |> printfn "φ(4)  = %d"
    eulerFunction 5 |> printfn "φ(5) = %d" 
    eulerFunction 6 |> printfn "φ(6) = %d" 
    eulerFunction 7 |> printfn "φ(7) = %d" 

main ()