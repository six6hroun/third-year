System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let referenceFrequencies =
    [
        ('о', 0.1097); ('е', 0.0845); ('а', 0.0801); ('и', 0.0735)
        ('н', 0.0670); ('т', 0.0626); ('с', 0.0547); ('р', 0.0547)
        ('в', 0.0453); ('л', 0.0434); ('к', 0.0349); ('м', 0.0321)
        ('д', 0.0298); ('п', 0.0281); ('у', 0.0262); ('я', 0.0201)
        ('ы', 0.0190); ('ь', 0.0174); ('г', 0.0170); ('з', 0.0165)
        ('б', 0.0159); ('ч', 0.0144); ('й', 0.0121); ('х', 0.0097)
        ('ж', 0.0094); ('ш', 0.0073); ('ю', 0.0064); ('ц', 0.0048)
        ('щ', 0.0036); ('э', 0.0032); ('ф', 0.0026); ('ъ', 0.0004)
        ('ё', 0.0004)
    ]
    |> Map.ofList

let getReferenceFreq c =
    referenceFrequencies
    |> Map.tryFind (System.Char.ToLower c)
    |> Option.defaultValue 0.0

let mostFrequentChar (str: string) =
    let total = float str.Length
    
    str
    |> Seq.filter System.Char.IsLetter
    |> Seq.countBy id
    |> Seq.map (fun (c, count) -> (c, float count / total))
    |> Seq.maxBy snd

let deviation (str: string) =
    match str with
    | "" -> infinity
    | _ ->
        let (ch, freq) = mostFrequentChar str
        let refFreq = getReferenceFreq ch
        (freq - refFreq) * (freq - refFreq)

let sortByDeviation strings =
    strings
    |> List.sortBy deviation


printfn "Введите строки (пустая строка - конец ввода):"
let rec readLines acc =
    let line = System.Console.ReadLine()
    match line with
    | null -> List.rev acc
    | "" -> List.rev acc
    | _ -> readLines (line :: acc)

let inputLines = readLines []
printfn "\nИсходные строки:"
inputLines |> List.iter (printfn "  %s")
let sorted = sortByDeviation inputLines
printfn "\nСтроки после сортировки по квадратичному отклонению:"
sorted |> List.iter (printfn "  %s")

printfn "\nОтклонения для каждой строки:"
sorted |> List.iter (fun s ->
    let d = deviation s
    let (ch, freq) = mostFrequentChar s
    let refFreq = getReferenceFreq ch
    printfn "  «%s» → самый частый: '%c' (%.3f), эталон: %.3f, отклонение: %.6f" s ch freq refFreq d
)