System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let response lang =
    match lang with
    | "F#"     -> "подлиза"
    | "Prolog" -> "подлиза"
    | "JavaScript"   -> "фу"
    | _        -> "чел ты кто?"

printf "Какой у тебя любимый язык? "
let lang = System.Console.ReadLine()
response lang |> printfn "%s"