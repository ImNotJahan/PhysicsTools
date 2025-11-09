grammar Expr;

prog:   block EOF ;

block:  (stat|expr|ctrl)* ;

stat:   var ':=' expr
    |   var ':~' expr
    |   var '[' expr '] :=' expr
    |   'if' expr 'then' block ('else if' expr 'then' block)* ('else' block)? 'end if'
    |   'while' expr 'loop' block 'end loop'
    |   'for' var 'in' expr 'loop' block 'end loop'
    |   'for' var 'from' expr 'to' expr 'loop' block 'end loop'
    |   'define' var '(' params ')' 'as' block 'end' var
    |   'import' package
    |   'from' package 'import' symbol (',' symbol)*
    ;

ctrl:   'break'
    |   'continue'
    |   'return' expr
    |   'return'
    |   'goto' var
    ;

expr:   '#' expr
    |   expr '[' expr ']'
    |   expr '`'? '(' args ')'
    |   expr '^' expr
    |   expr ('*'|'/') expr
    |   expr ('+'|'-') expr
    |   expr '|' expr
    |   expr ('='|'!='|'>'|'>='|'<'|'<=') expr
    |   expr ('and'|'or') expr
    |   expr '|>' expr
    |   expr '.' symbol
    |   '(' params ') ->' expr
    |   num
    |   str
    |   list
    |   '(' expr ')'
    |   var
    ;

symbol: SYMBOL ;
package: SYMBOL ('.' SYMBOL)* ;

list:    '[' (expr (',' expr)*)? ']' ;

args:    (expr (',' expr)*)? ;
params:  (var (',' var)*)? ;

num:    FLOAT
   |    FLOAT '~' FLOAT
   |    FLOAT SYMBOL
   |    FLOAT '~' FLOAT SYMBOL
   ;

str:    STRING ;

var:    SYMBOL ;

NEWLINE : [\r\n]+ -> skip;
SPACE   : [ \t]+ -> skip;

FLOAT   : '-'? DIGIT+ '.' DIGIT*
        | '-'? DIGIT+
        | '-'? '.' DIGIT+
        ;

SYMBOL  : (LOWER|UPPER|'_') (LOWER|UPPER|'_'|DIGIT)* ;
STRING  : '"' ~('"')* '"' ;

fragment DIGIT : [0-9] ;
fragment LOWER : [a-z] ;
fragment UPPER : [A-Z] ;
