function display_grid(size) {
    // TODO: Move this grid to an HTML template and have the Python generate the page and pass it
    //       back to be filled into the inner HTML.

    let grid = "<form id='grid_form' name='grid_form'>";

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

    for (let row = 0; row < size; row++) {
        let row_val = document.getElementById("grid_row_entry_" + row).value;

		  horizontal[row] = [];

		  if (row_val) {
            row_val.split(",").forEach(val => horizontal[row].push(parseInt(val)));
		  }

		  solved[row] = [];

		  for (let col = 0; col < size; col++) {
				// Fill out the solved array.

				let cell = document.getElementById("grid_cell_" + row + "_" + col);
	         let cell_val = window.getComputedStyle(cell, "").backgroundColor;

				if (cell_val == "rgb(255, 255, 255)") {
					 solved[row].push(0);
				}
				else {
					 solved[row].push(1);
				}
		  }
    }

    for (let col = 0; col < size; col++) {
        let col_val = document.getElementById("grid_col_entry_" + col).value;

		  vertical[col] = [];

		  if (col_val) {
            col_val.split(",").forEach(val => vertical[col].push(parseInt(val)));
		  }
    }

	 // TODO: The Python solver does not accept a partially filled out grid yet.
	 pywebview.api.solve(parseInt(size), horizontal, vertical).then(solved_callback);

	 // TODO: Display the number of passes to the user.
}

function solved_callback(response) {
	 solved = response[0];
	 empty = response[1];

	 for (let row = 0; row < solved.length; row++) {
		  for (let col = 0; col < solved.length; col++) {
				let cell = document.getElementById("grid_cell_" + row + "_" + col);

		      if (solved[row][col] == 1) {
					 cell.style.backgroundColor = "#000000";
		      }
		      else {
		          cell.style.backgroundColor = "#FFFFFF";
		      }
		  }
	 }
}
