System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8

let indicesDescending1 arr =
    arr
    |> List.mapi (fun i x -> (i, x))
    |> List.sortByDescending snd
    |> List.map fst

let indicesDescending2 arr =
    let rec insertSorted x lst =
        match lst with
        | [] -> [x]
        | (i, v) :: tail ->
            match snd x > v with
            | true -> x :: lst
            | false -> (i, v) :: insertSorted x tail

    let rec sort lst =
        match lst with
        | [] -> []
        | head :: tail -> insertSorted head (sort tail)

    let rec buildIndexed lst idx acc =
        match lst with
        | [] -> acc
        | head :: tail -> buildIndexed tail (idx + 1) ((idx, head) :: acc)

    let indexed = buildIndexed arr 0 []
    sort indexed |> List.map fst





let countInInterval1 arr a b =
    arr
    |> List.filter (fun x -> x >= a && x <= b)
    |> List.length

let countInInterval2 arr a b =
    let rec loop lst acc =
        match lst with
        | [] -> acc
        | head :: tail ->
            match head >= a && head <= b with
            | true -> loop tail (acc + 1)
            | false -> loop tail acc
    loop arr 0






let twoLargest1 arr =
    match List.sortDescending arr with
    | first :: second :: _ -> [first; second]
    | first :: [] -> [first]
    | [] -> []

let twoLargest2 arr =
    let rec findTwo lst max1 max2 =
        match lst with
        | [] -> [max1; max2]
        | head :: tail ->
            match head > max1 with
            | true -> findTwo tail head max1
            | false ->
                match head > max2 with
                | true -> findTwo tail max1 head
                | false -> findTwo tail max1 max2

    match arr with
    | [] -> []
    | first :: second :: rest ->
        let (m1, m2) =
            match first > second with
            | true -> (first, second)
            | false -> (second, first)
        findTwo rest m1 m2
    | [single] -> [single]






let elementsInSegment1 arr a b =
    arr
    |> List.filter (fun x -> x >= a && x <= b)

let elementsInSegment2 arr a b =
    let rec loop lst acc =
        match lst with
        | [] -> acc
        | head :: tail ->
            match head >= a && head <= b with
            | true -> loop tail (head :: acc)
            | false -> loop tail acc
    loop arr [] |> List.rev






let alternateIntFloat1 (arr: float list) =
    let isInt x = x = floor x

    match arr with
    | [] -> true
    | first :: rest ->
        let rec check lst expectedInt =
            match lst with
            | [] -> true
            | head :: tail ->
                match (expectedInt, isInt head) with
                | (true, true) -> check tail false
                | (false, false) -> check tail true
                | _ -> false
        check rest (isInt first)

let alternateIntFloat2 (arr: float list) =
    let isInt x = x = floor x

    let rec loop lst prevIsInt =
        match lst with
        | [] -> true
        | head :: tail ->
            let currIsInt = isInt head
            match prevIsInt = currIsInt with
            | true -> false
            | false -> loop tail currIsInt

    match arr with
    | [] -> true
    | first :: rest -> loop rest (isInt first)






let frequentMoreThan3Times1 arr =
    arr
    |> List.groupBy id
    |> List.filter (fun (_, group) -> List.length group > 3)
    |> List.map fst

let frequentMoreThan3Times2 arr =
    let rec countOccurrences lst target acc =
        match lst with
        | [] -> acc
        | head :: tail ->
            match head = target with
            | true -> countOccurrences tail target (acc + 1)
            | false -> countOccurrences tail target acc

    let rec contains lst x =
        match lst with
        | [] -> false
        | h :: t ->
            match h = x with
            | true -> true
            | false -> contains t x

    let rec collectUnique lst seen acc =
        match lst with
        | [] -> acc
        | head :: tail ->
            match contains seen head with
            | true -> collectUnique tail seen acc
            | false -> collectUnique tail (head :: seen) (head :: acc)

    let rec filterFrequent lst acc =
        match lst with
        | [] -> acc
        | head :: tail ->
            match countOccurrences arr head 0 > 3 with
            | true -> filterFrequent tail (head :: acc)
            | false -> filterFrequent tail acc

    let unique = collectUnique arr [] []
    filterFrequent unique [] |> List.rev

let printList label lst =
    let s = lst |> List.map string |> String.concat "; "
    printfn "%s: [%s]" label s

printfn "1.4 "
let arr4 = [5; 2; 8; 1; 9; 3]
printList "  исходный список" arr4
printList "  лямбда-версия" (indicesDescending1 arr4)
printList "  рекурсивная версия" (indicesDescending2 arr4)

printfn "\n1.14"
let arr14 = [10; 25; 3; 18; 7; 42; 15]
printfn "  исходный список: %A" arr14
printfn "  лямбда (10..20): %d" (countInInterval1 arr14 10 20)
printfn "  рекурсия (10..20): %d" (countInInterval2 arr14 10 20)

printfn "\n1.24"
let arr24 = [7; 2; 9; 4; 9; 1; 6]
printList "  исходный список" arr24
printList "  лямбда-версия" (twoLargest1 arr24)
printList "  рекурсивная версия" (twoLargest2 arr24)

printfn "\n1.34"
let arr34 = [5; 12; 3; 18; 7; 2; 20; 15]
printfn "  исходный список: %A" arr34
printfn "  лямбда (5..15): %A" (elementsInSegment1 arr34 5 15)
printfn "  рекурсия (5..15): %A" (elementsInSegment2 arr34 5 15)

printfn "\n1.44"
let arr44a = [1.0; 2.5; 3.0; 4.2; 5.0]
let arr44b = [1.0; 2.0; 3.1; 4.0; 5.5]
printfn "  чередуются A: %A -> %b" arr44a (alternateIntFloat1 arr44a)
printfn "  чередуются B: %A -> %b" arr44b (alternateIntFloat1 arr44b)

printfn "\n1.54 "
let arr54 = [1; 2; 2; 3; 2; 4; 2; 5; 2; 6; 7; 7; 7; 7; 7]
printList "  исходный список" arr54
printList "  лямбда-версия" (frequentMoreThan3Times1 arr54)
printList "  рекурсивная версия" (frequentMoreThan3Times2 arr54)