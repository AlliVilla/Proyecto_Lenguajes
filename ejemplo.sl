# Comprehensive lexer/parser test script

# Variable assignments and arithmetic (now supports '+', '-', '*', '/')
set a = 5
set b = 3
set sum = a + b
# Using newly supported operators
set product = a * b   # '*' now recognized by lexer
set diff = a - b      # '-' now recognized by lexer
set quotient = b / a  # '/' now recognized by lexer
set expr = (a + b) * 2  # parentheses for grouping

print "Assignments and arithmetic:"
print "sum = " + sum
print "product = " + product
print "diff = " + diff
print "quotient = " + quotient
print "expr = " + expr

# String literals and concatenation
print "Testing string concatenation: " + "hello" + " " + "world"

# Logging
log "This is a log message."

# Conditional statements with all comparison operators (these are supported)
if a < b
    log "a < b"
end
if a > b
    log "a > b"
end
if a <= b
    log "a <= b"
end
if a >= b
    log "a >= b"
end
if a == b
    log "a == b"
end
if a != b
    log "a != b"
end

# Logical operators
if a < b and b > 0
    log "Logical AND works"
end
if a == 5 or b == 5
    log "Logical OR works"
end

# Nested if-else
if a == 5
    if b == 3
        log "Nested condition true"
    else
        log "Nested else branch"
    end
else
    log "Outer else branch"
end

# While loop (assuming language supports it)
set counter = 0
while counter < 3
    print "Loop iteration " + counter
    set counter = counter + 1
end

#function greet(name)
#   print "Hello, " + name
#end
#greet("Alice")
