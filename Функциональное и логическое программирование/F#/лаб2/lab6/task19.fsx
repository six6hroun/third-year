System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8

let word =
    printf "Введите строку для проверки: "
    let str = System.Console.ReadLine()
    let letters = str |> Array.ofSeq
    let reversed = Array.rev letters
    let isPalindrome = letters = reversed
    match isPalindrome with
    | true  -> printfn "«%s» → палиндром" str
    | false -> printfn "«%s» → НЕ палиндром" str