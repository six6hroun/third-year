let task1 arr =
    Array.rev arr
let task2 a (b: int[]) =
    let result = Array.copy a
    result.[a.Length - 1] <- b.[b.Length - 1]
    result
let task3 a b =
    Array.append a b

let task4 =
    [|1..12|] |> Array.filter (fun x -> x % 3 = 0)
let task5 =
    let readArr () = System.Console.ReadLine().Split() |> Array.map int
    let a = readArr ()
    let b = readArr ()
    let toNum arr = Array.fold (fun acc x -> acc * 10 + x) 0 arr
    printfn "%d" (toNum a - toNum b)
let task6 =
    let readArr () = System.Console.ReadLine().Split() |> Array.map int
    let a = readArr ()
    let b = readArr ()
    Array.append a b |> Array.distinct |> Array.sort |> printfn "%A"
let task7 =
    let readArr () = System.Console.ReadLine().Split() |> Array.map int
    let a = readArr ()
    let b = readArr ()
    a |> Array.filter (fun x -> Array.contains x b) |> printfn "%A"
let task8 =
    let readArr () = System.Console.ReadLine().Split() |> Array.map int
    let a = readArr ()
    let b = readArr ()
    let onlyInA = a |> Array.filter (fun x -> not (Array.contains x b))
    let onlyInB = b |> Array.filter (fun x -> not (Array.contains x a))
    Array.append onlyInA onlyInB |> Array.sort |> printfn "%A"
let task9 =
    [|1..1000|]
    |> Array.filter (fun x -> x % 13 = 0 || x % 17 = 0)
    |> Array.truncate 100
    |> printfn "%A"
let task10 =
    let coeffs = System.Console.ReadLine().Split() |> Array.map int
    let n = coeffs.Length - 1
    let eval x =
        coeffs |> Array.mapi (fun i c -> c * pown x (n - i)) |> Array.sum
    let last = abs coeffs.[n]
    let first = abs coeffs.[0]
    [|-last..last|]
    |> Array.filter (fun x ->
        x <> 0 && last % x = 0 && first % x = 0 && eval x = 0)
    |> Array.distinct
    |> printfn "%A"