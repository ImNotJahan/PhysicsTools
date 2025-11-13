# Scripting

`physics_utils` features a builtin scripting language for streamlined usage of the module. 
Prominent features are writing uncertainties on any number by just putting `~` after it, and
star notation, which allows for easily doing calculations on large sets of data.

Here's an example of using it:

```
velocities := [0.312249, 0.343593, 0.365498, 0.688140, 0.205810]
mass := 235.4~0.05

define calc_ke(mass, velocity) as
    return mass * velocity ^ 2
end calc_ke

kinetic_energies := calc_ke*(mass, *velocities)

print(kinetic_energies)
"This would then output the following:"
"[22.951±0.005, 27.79±0.006, 31.447±0.007, 111.47±0.02, 9.971±0.002]"
```

## Using the interpreter
If you've already installed the `physics_utils` module (if not, see [getting started](https://physics-utils.readthedocs.io/en/latest/getting-started.html)), then you'll already have this ready to use as well.

To start an interactive session, run `python3 -m physics_utils.script`, which will start a REPL you can type code into and see the results of immediately. For example:
```
>>> x := 3.5~0.1 / 7~0.3
>>> sin(x)
0.48±0.02
```

To run a file, just append the filename to the previous command. I.e., `python3 -m physics_utils.script <filename>`

## Expressions
Expressions are code you write which returns something. For instance, comparisons, function calls, or numbers. We'll go over all the types of expressions here.

### Numbers
All numbers are stored as `MeasuredData`s. Creation of a number is as you'd expect: just writing the number, with an optional decimal.
You can, however, also add an uncertainty to a number by writing `~` followed by the uncertainty, after any number. For instance:
```
>>> 3
3.0
>>> 10~0.5
10.0±0.5
```

### Arithmetic
All the arithmetic operators work about how you'd expect, used in the form `expression operator expression`, where expression is assumed to be evaluated to a number.
Addition, subtraction, multiplication, and division are all the standard `+`, `-`, `*`, and `/`. Exponentation is `^`. Here are some examples:

```
>>> 3 + 2
5.0
>>> 5 * 2 + 3
13.0
>>> 7.5~0.1^2
56.0±2.
```

### Comparisons
Equality checks are done with `=`, and not equal `!=`. For greater than, less than, greater than or equal, and less than or equal, use `>`, `<`, `>=`, or `<=`.

### Logical operators
To check if two expressions are true, you can do `expression and expression`. To check if either expression is true, use `expression or expression`.

### Function calls
There are a few ways to call a function, which will all be gone over here.

#### Normal calls
To do a standard function call, just write the function's name followed by any arguments in parenthesis, seperated by commas, like so: `some_function(3, 10)`.

#### Star notation
Any function which does some operation on data can instead do that operation on collections of data, or collections of collections of collections ... of data, using star notation.

For example, if you had a function which calculated a number, you could instead have it calculate a bunch of numbers. When doing so, at least one of the arguments must also be a collection of the standard input, to the same depth as the expected output. The other arguments, however, can be collections up to or less than the depth of the output, or not be collections at all, and just the standard input. 

To do this, you put a stars `*` after the function name, equaling the depth of output you would like, and you also put stars before any argument, equaling the depth of input. 

This all can sound a bit arcane, so here are some examples:

```
define calc_momentum(mass, velocity) as
    return mass * velocity
end calc_momentum

"If I gathered the mass and velocity of a bunch of different objects," 
"I could calculate the momentum for all of them like so:"
masses := [100, 120, 50]
velocities := [5, 4, 7.5]

calc_momentum*(*masses, *velocities) "would return the following: [500, 480, 375]"

"If, instead, I gathered a bunch of velocities in various trials for an object"
"of constant mass, I could calculate it's momentum for each run like so:"
mass := 70
velocities := [10, 7, 11]

calc_momentum*(mass, *velocities) "would return [700, 490, 770]"

"If I gathered multiple runs for multiple objects of differing masses,"
"I could calculate the momentum for all of them also:"
masses := [3, 4, 5]
velocities := [[5, 10, 3], [2, 10], [12, 7, 9, 15]]

calc_momentum**(*masses, **velocities) "returns [[15, 30, 9], [8, 40], [60, 35, 45, 75]]"
```

#### Prime notation
Prime notation is the less useful cousin of star notation, but which is shorter in some scenarios. It is written like so: ``fn`(arg1, arg2, ...)``,
and is equivalent to writing `fn*(*arg1, *arg2, ...)`.

### Strings
Strings can be made by wrapping any text around double quotation marks. Strings are also used as comments, and can be multiline comments as well,
since newlines have no effect on parsing. For example: `"hello world!"`.

### Lists
Lists are created by writting square brackets, like so: `[]`. Any default elements in the list can be placed inside the brackets, seperated by commas. For example,

```
[] "an empty list"

[1, 2, 5] "a list with some elements"

[[5, 2, "Hi!"], 12] "a list with a list inside it"
```

Methods which are available on python lists, such as `.append`, `.pop`, `.insert`, etc. can all be used.

### Accessing list elements
List elements can be accessed by wrapping the index of the element you'd like in brackets after the list. For example:

```
>>> list := [10, 20, 30]
>>> list[0]
10.0
>>> list[2]
30.0
```

### Append operator
Along with doing `list.append(x)`, there is also a dedicated append operator, which adds an element to a list, and also returns the list afterwards. It's denoted by `|`, and used in the format `list | element`. Because this returns the list after, successive appends can be easily done like so: `list | 1 | 2 | 3` to add `1`, `2`, and `3` to the list, in that order.

### Length operator
You can get the length of a list by putting `#` before the list. For example:

```
>>> #[1, 2, 3]
3
```

### Parenthesis
Any expression can be wrapped in parenthesis. This has no effect, but is useful for forcing an order of operations.

### Anonymous functions
You can create a function without naming it by writing `(parameters) -> expression`, where expression is returned when the function is ran. For example:

```
>>> my_fn := (x, y) -> x + y * 2
>>> my_fn(2, 3)
8.0
>>> ((num) -> num ^ 2) (3)
9.0
```

### Variables
If you write a variable name, its value will be returned:

```
>>> x := 10
>>> x
10.0
```

There are three built-in variables (counted seperately from built-in functions,) which are `true` and `false`, as booleans, and `nil`, a
none/null type which is inheritly returned by many functions and statements.

## Statements
Statements are code which do not return anything (that is, immediately), such as if statements, function declarations, and loops. 

### Variable definitions
To define or change variables, the `:=` operator is used, in the format `variable_name := expression`. Note that the variable name can consist of letters, numbers, and underscores, but cannot start with a number. For example:

```
>>> x := 10
>>> x
10.0
```

### Uncertainty setting
If at any point you want to change the uncertainty on a variable, you can do so using the `:~` operator. For example:

```
>>> x := 3~0.5
>>> x
3.0±0.5
>>> x :~ 1
>>> x
3.0±1.
```

### List element setting
You can set the element of a list by wrapping the index of the element in brackets after the list name, and then putting that before the `:=` operator,
followed by the expression to set that value too. For example:

```
>>> numbers := [1, 2, 3, 4, 5]
>>> numbers
[1.0, 2.0, 3.0, 4.0, 5.0]
>>> numbers[2] := 100
>>> numbers
[1.0, 2.0, 100.0, 4.0, 5.0]
```

### While loops
While loops will execute some code as long as some expression is true. They are written in the format `while expression loop block end loop`,
where as long as expression is true, block is executed. For example:

```
x := 0

while x < 10 loop
    print(x)
    x := x + 1
end loop

"This code, when ran, would print the numbers 0 to 9"
```

### For loops
There are two types of for loops. The first type loops through a range, and the second type loops through elements in a list.

#### Range for loop
This type of for loop is written in the structure `for variable from left_bound to right_bound loop block end loop`, where variable is the
name of a variable which loops through the range, left_bound is the least value of the range (inclusive), right_bound is the greatest value
of the range (also inclusive), and block is the code ran. For example:

```
for i from 1 to 10 loop
    print(i)
end loop

"This code would print out the numbers 1 to 10"
```

#### List for loop
This type of for loop is written as `for variable in list loop block end loop`, where variable is the current element of the list, list is the list being looped through, and block is the code executed each iteration of the loop. For example,

```
my_list := [10, 35, 0.5, 12]
sum := 0

for x in my_list loop
    sum := sum + x
end loop

"This code sums up all the elements in my_list"

print(sum) "Would output 57.5"
```

### If statements
An if statement executes code on a given condition. It can also feature multiple conditions, which only run code if they are true and all previous conditions were false.
They can also run code on the case that all conditions ended up being false.

For just running code on a given condition, they are written `if expression then block end if`, where expression is the condition that must be true for the code block to execute.

For adding other coditions, which could execute if the previous condiitons were false, you add `else if expression then block` before the `end if`. To add a condition which
is executed on the case that no conditions were true, add `else block` right before the `end if`.

Here are some examples:

```
if 2 + 3 = 5 then
    print("Arithmetic is real!")
end if

age := 20

if age >= 19 then
    print("You can drink!")
else
    print("You can't drink")
end if

if age < 13 then
    print("You're a child")
else if age < 18 then
    print("You're a teenager")
else if age < 20 then
    print("You're both a teenager and an adult")
else
    print("You're an adult")
end if;
```

### Function declarations
Functions can be declared by writing `define name(parameters) as block end name`, where name is the name
of the function, containing letters, numbers, or underscores, but without a number as the first character; parameters
is an optional list of variable names seperated by commas, which will be passed to the function's code as arguments
when called; and where block is the code of the function.

A function may also contain return statements, which will exit the function when reached. A return statement may also have an expression after it, to
have the function return the value of that expression when that return statement is reached.

Some examples:

```
define avg_list(list) as
    sum := 0

    for x in list loop
        sum := sum + x
    end loop

    return sum / #list
end avg_list

print(avg_list([3, 5, 10])) "outputs 6.0"

define say_hi() as
    print("Hi there!")
end say_hi()

say_hi() "outputs 'Hi there!'"
```

### Import statements
Import statements can be used to import python modules in your code. They are written either `import module` or `from module import symbols`.

## Built-in functions
There are a number of built-in functions which can be used without import. They can also be overwritten, if wished.

### Trigonometric functions
`sin`, `cos`, `tan`, `arcsin`, and `arctan` are all builtin functions which perform their respective trigonometric operation
on some radian value provided to them.

### print
Same as the normal python print. Outputs any arguments provided to it.

### exit
Stops the interpreter.

### Standard deviation
`std` can be used to find the standard deviation on elements in a list.