System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let response lang =
    match lang with
    | "F#"     -> "подлиза"
    | "Prolog" -> "подлиза"
    | "JavaScript"   -> "фу"
    | _        -> "чел ты кто?"
let main _ =
    let readFromConsole = fun () -> System.Console.ReadLine()
    let writeToConsole = printfn "%s"
    let ask =readFromConsole >> response
    let fullPipeline = ask >> writeToConsole
    printf "Какой любимый язык?"
    fullPipeline()
    let printResponse = printfn "%s"
    let getResponse   = response
    printf "Какой любимый язык?"
    System.Console.ReadLine() 
    |>getResponse
    |>printResponse
main ()