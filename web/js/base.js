function display_grid(size) {
    // TODO: Move this grid to an HTML template and have the Python generate the page and pass it
    //       back to be filled into the inner HTML.

    var grid = "<form id='grid_form' name='grid_form'>";

    grid += "<table id='grid_table' name='grid_table'>";
    grid += "<tr id='entry_row'><td />";

    for (let col = 0; col < size; col++) {
        grid += "<td class='entry_col'><input id='grid_col_entry_" + col + "' class='grid_col_entry' type='text' /></td>";
    }

    grid += "</tr>";
    
    for (row = 0; row < size; row++) {
        grid += "<tr id='grid_row_'" + row + "'>";
        grid += "<td><input id='grid_row_entry_" + row + "' type='text' /></td>";

        for (let col = 0; col < size; col++) {
            grid += "<td class='grid_cell' id='grid_cell_" + row + "_" + col + "' onClick='toggle_cell(this);'> </td>";
        }

        grid += "</tr>";
    }

    grid += "</form></table>";

    document.getElementById("nonogram_grid").innerHTML = grid;
    document.getElementById("solve_button").style.visibility = "visible";
}

function toggle_cell(cell) {
    if (window.getComputedStyle(cell, "").backgroundColor == "rgb(255, 255, 255)") {
        cell.style.backgroundColor = "#000000";
    }
    else {
        cell.style.backgroundColor = "#FFFFFF";
    }
}

function submit_puzzle() {
    var horizontal = [];
    var vertical = [];
    var solved = [];

    var size = document.getElementById("size_entry").value;

    for (row = 0; row < size; row++) {
        var row_val = document.getElementById("grid_row_entry_" + row).value;

		  horizontal[row] = [];

		  if (row_val) {
            row_val.split(",").forEach(val => horizontal[row].push(parseInt(val)));
		  }
    }

	 alert(horizontal);

    for (col = 0; col < size; col++) {
        var col_val = document.getElementById("grid_col_entry_" + col).value;

		  vertical[col] = [];

		  if (col_val) {
            col_val.split(",").forEach(val => vertical[col].push(parseInt(val)));
		  }
    }
}
