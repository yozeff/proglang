# programming language (need to change this)

## Abstract

"programming language" is a functional programming language inspired by the lambda calculus - a syntax for describing computations with functions that was developed by Alonzo Church in the 1930s. Unlike Church's lambda calculus, "programming language" also allows for the assignment of variables. This allows programs to contain an evolving 'state' during runtime.

## Functions

### Function Application Syntax

All functions in "programming language" take their arguments with postfix (reverse polish) notation and no parenthesis. For example, to apply the binary function, f, to two arguments, a and b, one would do the following:

`a b f; //equivalent to f(a, b)`

### Functions with _Atoms_

Atoms are the basic functions for which all programmer defined functions are derived. In the default implementation, there are five atoms:

`a b +; a b -; a b *; //addition, subtraction and multiplication  
a b /; a b %; //quotient of a and b, a modulo b`

New atoms can be implemented by programmers as Python 3 functions. The function's source as well as an integer representing the function's arity should be placed within the atom dictionary as a tuple.

### Functions with _Lambda Abstractions_

Lambda abstractions are "programming language"'s method of implementing user defined functions. As the name suggests, they are able to create abstractions for routines that are implemented using atoms. Lambda abstractions can be assigned to an identifier and used many times in a program. Here is an example:

`f := λ x . 3 x *;`

Here, a lambda abstraction is introduced via the λ symbol, followed by its single argument, x, a fullstop and then the body of the lambda abstraction. The body of a lambda abstraction consists of an expression that may contain literals, or any defined identifiers. We say that the arguments are bound in the lambda abstraction. In this example, the lambda abstraction is then assigned to the identifier, f. Once a lambda abstraction is defined, it may be used elsewhere in the program, for example:

`2 f; //outputs 6  
3 f 4 f +; //outputs 21`

When a lambda abstraction is applied to some arguments, the arguments are simply substituted in for the bound variables in the body. The following are examples of how one may define lambda abstractions to act on two and three arguments respectively:

`g := λ a . λ b . b b * a +;  
h := λ p . λ q . λ r . p q + r + p *;`

### _Anonymous Lambda Abstractions_

In addition to being assigned to identifiers, lambda abstactions can also be used without assignment, in an expression. For example:

`3 2 ( λ x . x 3 + ); - //outputs -2`

These anonymous lambda abstractions can even be nested inside each other, for example:

`1 ( λ x . 3 ( λ y . y ( λ z . z y * ) 2 + ) x + ); //outputs 12  
f := λ x . λ y . x ( λ z . z y + ) x *; //produces valid lambda abstraction`

It is worth noting, however, that "programming language" is not a higher-order language. Therefore the following would not be valid.

`( λ x . 3 x * ) ( λ y . y 2 - );`

The anonymous lambda abstraction cannot be substituted into the next lambda abstraction.

## Variables

Variables in "programming language" can be defined as in the following example:

`x := 3;  
y := 3 2 +; //variables may assigned to the value of an expression`

These variables are what Church calls 'free-variables' in the lambda calculus. If the identifier associated with a free-variable in a lambda abstraction body is the same as one of the bound variables, the free-variable will also have its value substituted when the lambda abstraction is applied. For example:

`x := 2;  
f := λ x . x x +; //free-variable and bound-variable identifiers clash  
3 f; //this expression equals 6 (3 3 +)`

## _Branches_

The branch is "programming language"'s only control structure. It resembles the if statement used in other programming languages, however branches are actually expressions that can be used to emulate the basic if, then, else pattern present in those languages. Despite a seemingly contrived implementation, the rammifications implied by the branch over "programming language" are very remarkable - an example of the syntax follows:

`? x -> y ! z : ;`

Here, x, y and z represent the condition, success and failure expressions, respectively. The question mark is used to introduce the branch, whilst the arrow shows how the success expression follows from the condition expression, and the exclamation mark shows that the following expression is the result of 'not' the condition expression. Finally, the branch is concluded with the colon. The logic for the branch consists of a branching rule: _if the condition expression > 0 then output the success expression, otherwise output the failure expression_. For example:

`? 5 -> 3 ! 10 : ; //outputs 3`

Since branches are expressions, we can place them in as any other expression and even nest them. It is this nesting that allows for the if, else if, ..., else pattern to be imitated by "programming language". The following shows how nested branches may be used to produce an equality lambda abstraction:

`= := λ x . λ y . ? x y - -> 0 ! ? 0 x y - - -> 0 ! 1 : : ;`

Here, an output of 1 denotes a true result and a value of zero denotes a false one. Perhaps the most significant consequence of the branch is that it allows the use of recursive lambda abstractions. While recursion is possible without branches, since there is no way to effect 'how' a function is applied, recursive functions will recur indefinitely. This is obviously not hugely useful. Branches now allow us to apply a function if a condition is satisfied, according to the branching rule. The following is a lambda abstraction to sum the natural numbers between 0 and n:

`sum := λ n . ? n -> n 1 - sum n + ! 0 : ;  
6 sum; //outputs 21`

With branches one can emulate the while and for patterns used by other languages. This pattern can be used to implement a program to generate Fibonacci numbers:

`//helper also passes two last fibonacci numbers (a and b) and the amount of numbers calculated so far (i)  
fibonacci_helper := λ n . λ i . λ a . λ b . ? i n - -> b ! n i 1 + b a b + fibonacci_helper : ;  

//this is the lambda abstraction used by users  
fibonacci := λ n . n 2 - 0 1 1 fibonnaci_helper;`
