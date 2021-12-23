function display_grid(size) {
	 var grid = "<form id='grid_form' name='grid_form'>";

	 grid += "<table id='grid_table' name='grid_table'>";
	 grid += "<tr id='entry_row'><td />";

	 for (let col = 0; col < size; col++) {
		  grid += "<td class='entry_col'><input id='grid_col_entry_" + col + "' class='grid_col_entry' type='text' /></td>";
	 }

	 grid += "</tr>";
	 
    for (let row = 0; row < size; row++) {
		  grid += "<tr id='grid_row_'" + row + "'>";
		  grid += "<td><input id='grid_row_entry_" + row + "' type='text' /></td>";

        for (let col = 0; col < size; col++) {
				grid += "<td id='grid_cell_" + row + "_" + col + "'>0</td>";
        }
		  grid += "</tr>";
    }

	 grid += "</form></table>";

    document.getElementById("nonogram_grid").innerHTML = grid;
    document.getElementById("solve_button").style.visibility = "visible";
}

function submit_puzzle() {
}
