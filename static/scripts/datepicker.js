function initDatePicker(containerId) {
	const container = document.getElementById(containerId);
	if (!container) return;

	const dateInput = container.querySelector('.datepicker-input');
	const calendarCard = container.querySelector('.calendar-card');
	const monthDisplay = container.querySelector('.current-month');
	const calendarGrid = container.querySelector('.calendar-grid');
	const prevBtn = container.querySelector('.prev-month');
	const nextBtn = container.querySelector('.next-month');

	let currentDate = new Date();
	let selectedDate = null;

	const months = [
		"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
		"Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
	];

	const dayNames = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];

	const renderCalendar = () => {
		const year = currentDate.getFullYear();
		const month = currentDate.getMonth();

		monthDisplay.textContent = `${months[month]} ${year}`;
		calendarGrid.innerHTML = '';

		// Renderizar nombres de días
		dayNames.forEach(day => {
			const dayElem = document.createElement('div');
			dayElem.className = 'day-name';
			dayElem.textContent = day;
			calendarGrid.appendChild(dayElem);
		});

		const firstDayOfMonth = new Date(year, month, 1).getDay();
		const daysInMonth = new Date(year, month + 1, 0).getDate();

		// Espacios vacíos
		for (let i = 0; i < firstDayOfMonth; i++) {
			const emptyElem = document.createElement('div');
			emptyElem.className = 'calendar-day empty';
			calendarGrid.appendChild(emptyElem);
		}

		// Días del mes
		const today = new Date();
		for (let i = 1; i <= daysInMonth; i++) {
			const dayElem = document.createElement('div');
			dayElem.className = 'calendar-day';
			dayElem.textContent = i;

			if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
				dayElem.classList.add('today');
			}

			if (selectedDate && 
				i === selectedDate.getDate() && 
				month === selectedDate.getMonth() && 
				year === selectedDate.getFullYear()) {
				dayElem.classList.add('selected');
			}

			dayElem.addEventListener('click', () => {
				const newDate = new Date(year, month, i);
				selectedDate = newDate;
				
				const d = String(newDate.getDate()).padStart(2, '0');
				const m = String(newDate.getMonth() + 1).padStart(2, '0');
				const y = newDate.getFullYear();
				
				dateInput.value = `${d}/${m}/${y}`;
				calendarCard.classList.remove('active');
				renderCalendar();
			});

			calendarGrid.appendChild(dayElem);
		}
	};

	// Eventos
	dateInput.addEventListener('click', (e) => {
		// Cerrar otros calendarios abiertos si fuera necesario
		document.querySelectorAll('.calendar-card').forEach(card => {
			if (card !== calendarCard) card.classList.remove('active');
		});
		calendarCard.classList.toggle('active');
		e.stopPropagation();
	});

	prevBtn.addEventListener('click', (e) => {
		e.stopPropagation();
		currentDate.setMonth(currentDate.getMonth() - 1);
		renderCalendar();
	});

	nextBtn.addEventListener('click', (e) => {
		e.stopPropagation();
		currentDate.setMonth(currentDate.getMonth() + 1);
		renderCalendar();
	});

	// Cerrar al hacer click fuera
	document.addEventListener('click', (e) => {
		if (!container.contains(e.target)) {
			calendarCard.classList.remove('active');
		}
	});

	renderCalendar();
}