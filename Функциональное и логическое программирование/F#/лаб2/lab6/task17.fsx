System.Console.OutputEncoding <- System.Text.Encoding.UTF8
System.Console.InputEncoding  <- System.Text.Encoding.UTF8
let isPrime n =
    let rec loop i =
        match i * i > n with
        | true  -> true
        | false ->
            match n % i = 0 with
            | true  -> false
            | false -> loop (i + 1)
    match n < 2 with
    | true  -> false
    | false -> loop 2
let rec gcd a b =
    match b with
    | 0 -> a
    | _ -> gcd b (a % b)
let digits n =
    string n |> Seq.map (fun c -> int c - int '0') |> Seq.toList
let readList () =
    System.Console.ReadLine().Split(' ')
    |> Array.map int
    |> Array.toList
let task1 () =
    printfn "Даны две последовательности, найти наибольшую по длине общую подпоследовательность"
    printfn "Введите первую последовательность:"
    let a = readList ()
    printfn "Введите вторую последовательность:"
    let b = readList ()
    let m = List.length a
    let n = List.length b
    let arrA = Array.ofList a
    let arrB = Array.ofList b
    let dp =
        [0..m] |> List.map (fun _ -> Array.create (n + 1) 0)
        |> Array.ofList
    [1..m] |> List.iter (fun i ->
        [1..n] |> List.iter (fun j ->
            dp.[i].[j] <-
                match arrA.[i-1] = arrB.[j-1] with
                | true  -> dp.[i-1].[j-1] + 1
                | false -> max dp.[i-1].[j] dp.[i].[j-1]))
    let rec backtrack i j acc =
        match i = 0 || j = 0 with
        | true -> acc
        | false ->
            match arrA.[i-1] = arrB.[j-1] with
            | true  -> backtrack (i-1) (j-1) (arrA.[i-1] :: acc)
            | false ->
                match dp.[i-1].[j] >= dp.[i].[j-1] with
                | true  -> backtrack (i-1) j acc
                | false -> backtrack i (j-1) acc

    let lcs = backtrack m n []
    printfn "LCS длина=%d: %A" (List.length lcs) lcs
let task2 () =
    printfn "Дан список, построить кортежи"
    printfn "Введите список:"
    let src = readList ()
    let list1 = src |> List.filter (fun x -> x % 2 = 0) |> List.map (fun x -> x / 2)
    let list2 = list1 |> List.filter (fun x -> x % 3 = 0) |> List.map (fun x -> x / 3)
    let list3 = list2 |> List.map (fun x -> x * x)
    let list4 = list3 |> List.filter (fun x -> List.contains x list1)
    let list5 = list2 @ list3 @ list4 |> List.distinct
    printfn "list1 (Чётные / 2):           %A" list1
    printfn "list2 (делятся на 3, / 3):    %A" list2
    printfn "list3 (квадраты list2):        %A" list3
    printfn "list4 (list3 ∩ list1):         %A" list4
    printfn "list5 (list2 ∪ list3 ∪ list4): %A" list5
    printfn "Кортеж: %A" (list1, list2, list3, list4, list5)
let task3 () =
    printfn "Для введенного числа N построить список неповторяющихся кортежей"
    printfn "Введите N:"
    let n = System.Console.ReadLine() |> int
    List.allPairs [1..n] [1..n]
    |> List.filter (fun (x, y) -> x * y = n)
    |> List.map (fun (x, y) ->
        let d = gcd x y
        (x / d, y / d))
    |> List.distinct
    |> printfn "Результат: %A"
let task4 () =
    printfn "Для введенного списка построить новый с элементами вида (a,b,c), где a<b<c образуют Пифагорову тройку"
    printfn "Введите список:"
    let src = readList ()
    List.allPairs src src
    |> List.collect (fun (a, b) -> src |> List.map (fun c -> (a, b, c)))
    |> List.filter (fun (a, b, c) -> a < b && b < c && a*a + b*b = c*c)
    |> List.distinct
    |> printfn "Тройки: %A"
let task5 () =
    printfn "Для введенного списка построить список из элементов, для которых в данном списке встречаются все простые делители"
    printfn "Введите список:"
    let src = readList ()
    let primeDivisors n =
        [2..n] |> List.filter (fun d -> n % d = 0 && isPrime d)
    src
    |> List.filter (fun x ->
        primeDivisors x |> List.forall (fun d -> List.contains d src))
    |> printfn "Результат: %A"
let task6 () =
    printfn "Отсортировать введенный список кортежей длины 5 по возрастанию в лексико-графическом порядке..."
    printfn "Введите кортежи (каждый — 5 чисел через пробел, пустая строка — конец):"

    let rec readTuples acc =
        let line = System.Console.ReadLine()
        match line with
        | "" -> List.rev acc
        | _  ->
            let parts = line.Split(' ') |> Array.map int
            readTuples ((parts.[0], parts.[1], parts.[2], parts.[3], parts.[4]) :: acc)
    let tuples = readTuples []
    tuples
    |> List.sort
    |> List.map (fun (a,b,c,d,e) ->
        [a;b;c;d;e]
        |> List.map string
        |> String.concat ""
        |> int)
    |> printfn "Результат: %A"
let task7 () =
    printfn "Для введенного списка построить новый список, который получен из начального"
    printfn "Введите список:"
    let src = readList ()

    let avg = float (List.sum src) / float (List.length src)
    let evenPosElements =
        src
        |> List.mapi (fun i x -> (i, x))
        |> List.filter (fun (i, _) -> i % 2 = 0)
        |> List.map snd
    let divisorsOfEvenPos =
        evenPosElements
        |> List.collect (fun x -> [1..x] |> List.filter (fun d -> x % d = 0))
        |> List.distinct
    let belowAvg = src |> List.filter (fun x -> float x < avg)
    let pValue a =
        [1..a]
        |> List.filter (fun d ->
            a % d = 0
            && List.contains d divisorsOfEvenPos
            && belowAvg |> List.forall (fun x -> x % d <> 0))
        |> List.sum
    src
    |> List.sortBy pValue
    |> printfn "Результат: %A"
let task8 () =
    printfn "Для введенного списка построить список, где каждый элемент – это среднее арифметическое тех цифр соответствующего числа из исходного списка, которые встречаются в списке чаще, чем половина всех остальных цифр"
    printfn "Введите список:"
    let src = readList ()
    let allDigits = src |> List.collect digits
    let total = List.length allDigits
    let freqOf d = allDigits |> List.filter (fun x -> x = d) |> List.length
    let result =
        src
        |> List.map (fun n ->
            let ds = digits n |> List.distinct
            let frequent =
                ds |> List.filter (fun d ->
                    let f = freqOf d
                    f * 2 > total)
            match frequent with
            | [] -> 0.0
            | fs -> float (List.sum fs) / float (List.length fs))

    printfn "Результат: %A" result
let task9 () =
    printfn "Для введенного списка построить новый список, в который войдут лишь те элементы, которые"
    printfn "Введите список:"
    let src = readList ()

    let isPerfectSquareOf lst x = lst |> List.exists (fun e -> e * e = x)
    let divisibleByAll prev x =
        match prev with
        | [] -> true
        | _  -> prev |> List.forall (fun p -> p <> 0 && x % p = 0)

    src
    |> List.mapi (fun i x -> (x, List.take i src))
    |> List.filter (fun (x, prev) ->
        x > List.sum prev
        && isPerfectSquareOf src x
        && divisibleByAll prev x)
    |> List.map (fun (x, prev) ->
        let countMore = src |> List.filter (fun e -> e > x) |> List.length
        (x, List.sum prev, countMore))
    |> printfn "Результат (число, сумма_пред, кол-во_больших): %A"
let task10 () =
    printfn "Для введенного списка вывести кортеж списков"
    printfn "Введите список:"
    let src = readList ()
    let n = List.length src
    let indices = [0..n-1]
    let list2 =
        indices |> List.filter (fun i ->
            let x = List.item i src
            List.allPairs indices indices
            |> List.exists (fun (j, k) ->
                j <> i && k <> i && j <> k
                && List.item j src * List.item k src = x))
    let list3 =
        indices |> List.filter (fun i ->
            let x = List.item i src
            List.allPairs indices indices
            |> List.exists (fun (j, k) ->
                indices |> List.exists (fun l ->
                    l <> i && l <> j && l <> k && j <> k && j <> l && k <> l
                    && List.item j src + List.item k src + List.item l src = x)))
    let list4 =
        indices |> List.filter (fun i ->
            let x = List.item i src
            src |> List.filter (fun d -> d <> 0 && x % d = 0) |> List.length = 4)
    printfn "List2 (номера): %A" list2
    printfn "List3 (номера): %A" list3
    printfn "List4 (номера): %A" list4
    printfn "Кортеж: %A" (list2, list3, list4)
let main _ =
    task1 ()
    task2 ()
    task3 ()
    task4 ()
    task5 ()
    task6 ()
    task7 ()
    task8 ()
    task9 ()
    task10 ()
main ()