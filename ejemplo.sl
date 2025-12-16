# Función recursiva factorial
function factorial(n)
    # Caso base
    if n <= 1
        return 1
    end
    
    # Caso recursivo
    return n * factorial(n - 1)
end

# Probar factorial recursivo
print "=== Testing recursive factorial ==="
set fact5 = factorial(5)
print "factorial(5) = " + fact5

set fact0 = factorial(0)
print "factorial(0) = " + fact0

set fact10 = factorial(10)
print "factorial(10) = " + fact10

# Función recursiva Fibonacci
function fibonacci(n)
    if n <= 0
        return 0
    end
    if n == 1
        return 1
    end
    return fibonacci(n - 1) + fibonacci(n - 2)
end

# Probar Fibonacci recursivo
print "=== Testing recursive fibonacci ==="
set fib6 = fibonacci(6)
print "fibonacci(6) = " + fib6

# Función recursiva con concatenación (invertir string)
function reverse_string(s, index)
    if index < 0
        return ""
    end
    set char = substring(s, index, index + 1)
    return char + reverse_string(s, index - 1)
end

# Función auxiliar para longitud de string (asumiendo que existe)
function string_length(s)
    set len = 0
    while substring(s, len, len + 1) != ""
        set len = len + 1
    end
    return len
end

# Probar reverse_string
print "=== Testing recursive string reverse ==="
set original = "hello"
set reversed = reverse_string(original, string_length(original) - 1)
print "Reversed of 'hello' = " + reversed