const table = document.getElementById('myTable');
const tbody = table.querySelector('tbody');
// Seleccionamos los th.sortable para los event listeners.
// Importante que el HTML de los THs tenga el icono <i> inicial.
const ths = table.querySelectorAll('th.sortable'); 
const itemsPerPageSelect = document.getElementById('itemsPerPage');
const prevPageBtn = document.getElementById('prevPage');
const nextPageBtn = document.getElementById('nextPage');
const paginationStatus = document.getElementById('paginationStatus');
let currentPage = 1;
let itemsPerPage = parseInt(itemsPerPageSelect.value);
let originalRows = Array.from(tbody.querySelectorAll('tr'));
let currentSortColumnIndex = -1;
let currentSortDirection = 'asc'; // 'asc' or 'desc'

const getCellValue = (tr, idx) => {
	const cell = tr.children[idx];
	return cell ? cell.innerText || cell.textContent : '';
};

const comparer = (idx, asc) => (a, b) => {
	const v1 = getCellValue(asc ? a : b, idx);
	const v2 = getCellValue(asc ? b : a, idx);
	// Intenta convertir a número si es posible (ignorando comas para Search Volume)
	const isNumericCol = table.querySelector('thead th:nth-child(' + (idx + 1) + ')').classList.contains('numeric');
	if (isNumericCol) {
		const num1 = parseFloat(v1.replace(/,/g, ''));
		const num2 = parseFloat(v2.replace(/,/g, ''));
		if (!isNaN(num1) && !isNaN(num2)) {
			return num1 - num2;
		}
	}
	return v1.toString().localeCompare(v2.toString());
};

function updatePaginationStatus() {
	const totalItems = originalRows.length;
	const startIndex = (currentPage - 1) * itemsPerPage + 1;
	const endIndex = Math.min(currentPage * itemsPerPage, totalItems);
	paginationStatus.textContent = `${startIndex} - ${endIndex} of ${totalItems}`;
	prevPageBtn.disabled = currentPage === 1;
	nextPageBtn.disabled = currentPage * itemsPerPage >= totalItems;
}

function renderTable() {
	tbody.innerHTML = ''; // Limpiar el cuerpo de la tabla
	const sortedRows = [...originalRows]; // Crear una copia para ordenar
	if (currentSortColumnIndex !== -1) {
		sortedRows.sort(comparer(currentSortColumnIndex, currentSortDirection === 'asc'));
	}
	const startIndex = (currentPage - 1) * itemsPerPage;
	const endIndex = startIndex + itemsPerPage;
	const paginatedRows = sortedRows.slice(startIndex, endIndex);
	paginatedRows.forEach((row, index) => {
		// Actualizar el número de ID en la primera columna visible
		row.children[0].textContent = startIndex + index + 1;
		tbody.appendChild(row);
	});

	updatePaginationStatus();
}

ths.forEach((th, index) => {
	th.addEventListener('click', () => {
		const headerRow = th.parentNode;
		const columnIndex = Array.from(headerRow.children).indexOf(th);
		const currentIcon = th.querySelector('.fas'); // Obtener el icono existente (fa-arrow-up o fa-arrow-down)

		// Determinar la nueva dirección de ordenamiento
		let newSortDirection = 'asc';
		if (currentSortColumnIndex === columnIndex) {
			newSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
		}

		// Limpiar clases de ordenamiento y restablecer iconos de todos los encabezados sortable
		ths.forEach(otherTh => {
			otherTh.classList.remove('asc', 'desc');
			const otherIcon = otherTh.querySelector('.fas');
			if (otherIcon) {
				// Resetear el icono a su estado por defecto (flecha hacia arriba, oculto por CSS)
				otherIcon.className = 'fas fa-arrow-up';
			}
		});

		// Añadir la clase de ordenamiento al encabezado clickeado
		th.classList.add(newSortDirection);

		// Actualizar la clase del icono del encabezado clickeado
		if (currentIcon) {
			currentIcon.className = `fas ${newSortDirection === 'asc' ? 'fa-arrow-up' : 'fa-arrow-down'}`;
		}

		currentSortColumnIndex = columnIndex;
		currentSortDirection = newSortDirection;
		currentPage = 1; // Volver a la primera página después de ordenar
		renderTable();
	});
});

itemsPerPageSelect.addEventListener('change', function() {
	itemsPerPage = parseInt(this.value);
	currentPage = 1;
	renderTable();
});

prevPageBtn.addEventListener('click', function() {
	if (currentPage > 1) {
		currentPage--;
		renderTable();
	}
});

nextPageBtn.addEventListener('click', function() {
	const totalPages = Math.ceil(originalRows.length / itemsPerPage);
	if (currentPage < totalPages) {
		currentPage++;
		renderTable();
	}
});
const initialSortColumn = document.querySelector('th[data-column="keyword"]');
if (initialSortColumn) {
	initialSortColumn.click();
} else {
	renderTable();
}