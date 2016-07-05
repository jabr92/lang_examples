### Problems

* Web server  
  * Authentication  
  * B
  * Endpoints for puzzle solvers  
  
* Puzzle solvers  
 * Sudoku  

### Web servers

Language 	| Framework
:---:	 	| :---:
Haskell		| Yesod
Javascript  | Node
PHP			| Laravel
Python		| Flask
Ruby		| Rails

### Sudoku

A solver and solution checker for each language.

Functions take input strings which are 81 charcters long, serialized from left to right, top to bottom 
with periods for blank spaces and no separator for rows. The `sudoku_puzzles.txt` file contains 17,444 such strings.

The following board and string are equivalent:

`1 2 3 | 4 _ 6 | 7 8 9`  
`4 5 6 | 7 8 9 | 1 _ 3`  
`7 _ 9 | 1 2 3 | 4 5 6`  
  
`2 3 _ | _ 6 7 | 8 _ 1`  
`5 6 7 | 8 9 1 | 2 3 4`  
`_ 9 1 | _ 3 4 | _ 6 7`  
    
`3 _ _ | _ 7 _ | 9 _ _`  
`_ _ 8 | _ 1 2 | _ 4 _`  
`_ _ _ | _ _ _ | _ _ 8`  
  
"1234.67894567891.37.912345623..678.1567891234.91.34.673...7.9....8.12.4.........8"
