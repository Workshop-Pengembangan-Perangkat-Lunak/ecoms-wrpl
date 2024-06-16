function addRow(user, address, date, status) {
	const table = document.getElementById('orders-table').getElementsByTagName('tbody')[0];
	const newRow = table.insertRow();

	const userCell = newRow.insertCell(0);
	const addressCell = newRow.insertCell(1);
	const dateCell = newRow.insertCell(2);
	const statusCell = newRow.insertCell(3);

	userCell.innerHTML = `<img src="img/people.png"><p>${user}</p>`;
	addressCell.textContent = address;
	dateCell.textContent = date;
	statusCell.innerHTML = `<span class="status ${status.toLowerCase()}">${status}</span>`;
}

// Handle form submission
document.getElementById('add-order-form').addEventListener('submit', function (e) {
	e.preventDefault();

	const user = document.getElementById('user').value;
	const address = document.getElementById('address').value;
	const date = document.getElementById('order-date').value;
	const status = document.getElementById('status').value;

	addRow(user, address, date, status);

	// Reset the form
	e.target.reset();

	// Close the modal
	document.getElementById('order-modal').style.display = 'none';
});

// Modal functionality
const modal = document.getElementById('order-modal');
const addOrderIcon = document.getElementById('add-order-icon');
const closeButton = document.getElementsByClassName('close')[0];

addOrderIcon.onclick = function() {
	modal.style.display = 'block';
}

closeButton.onclick = function() {
	modal.style.display = 'none';
}

window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = 'none';
	}
}
