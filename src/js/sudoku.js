total_cells = 81;
possible_vals = ["1", "2", "3", "4", "5", "6", "7", "8", "9"];

var row_num = function(cell_num) {
    return Math.floor(cell_num / 9);
}
var col_num = function(cell_num) {
    return cell_num % 9;
}
var box_num = function(cell_num) {
    return Math.floor(col_num(cell_num) / 3) + 3 * Math.floor(row_num(cell_num / 3));
}

var solve_sudoku = function(puzzle_string) {

    // build arrays for all units (rows, columns, and boxes)
    var rows = [];
    for (i = 0; i < 9; i++) {
        rows.push(".........");
    }
    var columns = rows.slice();
    var boxes = rows.slice();

    var set_val = function(cell_num, val) {
        r = row_num(cell_num);
        c = col_num(cell_num);
        rows[r][c] = val;
        columns[c][r] = val;
        boxes[box_num(cell_num)][c % 3 + 3 * (r % 3)] = val;
    }

    // add known values to units
    for (i = 0; i < total_cells; i++) {
        val = puzzle_string[i];
        if (val != ".") {
            set_val(i, val);
        }
    }

    var get_val = function(cell_num){
        r = row_num(cell_num);
        c = col_num(cell_num);
        return rows[r][c];
    }

    var get_units = function(cell_num){
        r = row_num(cell_num);
        c = col_num(cell_num);
        b = box_num(cell_num);
        return [rows[r], columns[c], boxes[b]];
    }

    var scan_values = function() {
        for (i = 0; i < total_cells; i++) {
            if (get_val(i) == ".") {
                possible_vals.forEach(function checkDetermined(val){

                })
            }
        }
    }



}

test = ".................85.7.1..2...........3...6.....9..523..6...3.1...18...54.4.69...7"
console.log(solve_sudoku(test))