var row_num = function(cell_num) {
    return Math.floor(cell_num / 9)
}
var col_num = function(cell_num) {
    return cell_num % 9
}
var box_num = function(cell_num) {
    return Math.floor(col_num(cell_num) / 3) + 3 * Math.floor(row_num(cell_num / 3))
}

var solve_sudoku = function(puzzle_string) {

    var possibles = [];
    var rows = [];

    // build arrays for rows, columns, and boxes
    for (i = 0; i < 9; i++) {
        rows.push(".........")
    }

    var columns = rows.slice()
    var boxes = rows.slice()

    for (i = 0; i < 81; i++) {
        val = puzzle_string[i]
        if (val != ".") {
            r = row_num(i)
            c = col_num(i)
            rows[r][c] = val
            columns[c][r] = val
            boxes[box_num(i)][c % 3 + 3 * (r % 3)] = val
        }
        possibles.push(val)


    }

    for (i = 0;i < 81; i++) {
        if (possibles[i] == ".") {

        }
    }
    return possibles
}

test = ".................85.7.1..2...........3...6.....9..523..6...3.1...18...54.4.69...7"
console.log(solve_sudoku(test))