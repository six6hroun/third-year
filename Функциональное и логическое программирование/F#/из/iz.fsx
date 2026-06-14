let rec powMod (a: bigint) (b: bigint) (m: bigint) (acc: bigint) : bigint =
    if b = 0I then 
        acc % m
    elif b % 2I = 0I then 
        powMod ((a * a) % m) (b / 2I) m acc
    else 
        powMod ((a * a) % m) (b / 2I) m ((acc * a) % m)

let isDivisor (p: int) : bool =
    let pBig = bigint p
    p <> 3 && (powMod 10I 1000000000I pBig 1I = 1I)

let sieveOfEratosthenes (limit: int) : int list =
    if limit < 2 then []
    else
        let sieve = Array.create (limit + 1) true
        sieve.[0] <- false
        sieve.[1] <- false
        
        let sqrtLimit = int(sqrt(float limit))
        for i in 2 .. sqrtLimit do
            if sieve.[i] then
                for j in i * i .. i .. limit do
                    sieve.[j] <- false
        
        let rec collectPrimes current acc =
            if current > limit then 
                acc
            elif sieve.[current] then
                collectPrimes (current + 1) (current :: acc)
            else
                collectPrimes (current + 1) acc
        
        List.rev (collectPrimes 2 [])

let rec selectFirstNDivisors (primes: int list) (n: int) (acc: int list) (count: int) : int list =
    if count = n then
        List.rev acc
    else
        match primes with
        | [] -> failwith "Недостаточно простых чисел"
        | p :: rest ->
            if isDivisor p then
                selectFirstNDivisors rest n (p :: acc) (count + 1)
            else
                selectFirstNDivisors rest n acc count

printfn "Задача 132"
printfn "Генерация простых чисел и поиск первых 40 делителей"
let allPrimes = sieveOfEratosthenes 2000000
let divisors = selectFirstNDivisors allPrimes 40 [] 0

printfn "\nНайденные простые делители:"
divisors |> List.iter (fun p -> printf "%d " p)

let sum = List.sum divisors
printfn "\n\nСумма = %d" sum
printfn "\nВсего найдено делителей: %d" (List.length divisors)