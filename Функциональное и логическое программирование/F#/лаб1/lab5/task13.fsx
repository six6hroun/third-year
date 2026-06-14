System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let rec gcd a b =
    match b with
    |0 -> a
    |_ -> gcd b (a%b)
let rec travers n f init i =
    match i with
    |0 -> init
    |_ ->
        match gcd n i with
        |1 -> travers n f (f init i) (i-1)
        |_ -> travers n f init (i-1)
let coprime n f init= travers n f init (n-1)
let main _ =
    printf "введите число: "
    let input = System.Console.ReadLine()
    let number = int input  
    coprime number (fun a b-> a+b) 0
    |> printfn "сумма: %d"

    coprime number (fun a b -> a * b) 1
    |> printfn "произведение: %d"

    coprime number (fun a b -> match a < b with true -> a | false -> b) (number - 1)
    |> printfn "минимум: %d"

    coprime number (fun a b -> match a > b with true -> a | false -> b) 0
    |> printfn "максимум: %d"

    coprime number (fun a _ -> a + 1) 0
    |> printfn "количество: %d"
main ()