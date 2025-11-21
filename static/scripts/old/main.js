
/*function addRegla() {
	const lstReglas = document.getElementById("lst-reglas");
	const htmlFragment = `
		<div class="card-header">Regla</div>
		<div class="card-body">
			<div class="row">
				<div class="col-lg-2">
					<select class="form-select" id="exampleSelect1">
						<option>CPA</option>
						<option>Consumo</option>
						<option>Conversiones</option>
						<option>4</option>
						<option>5</option>
					</select>
				</div>
				<div class="col-lg-2">
					<select class="form-select" id="exampleSelect1">
						<option>Igual que [=]</option>
						<option>Mayor o igual que (>=)</option>
						<option>=</option>
						<option>/=</option>
					</select>
				</div>
				<div class="col-lg-2">
					<input type="number" class="form-control" placeholder="cantidad" id="inputDefault" min="1" step="10">
				</div>
				<div class="col-lg-3">
					<button type="submit" class="btn btn-danger btn-del-regla">Eliminar Regla</button>
				</div>
			</div>
		</div>
	`;

	// Crear un elemento div para el fragmento HTML
	const divFragment = document.createElement('div');
	divFragment.classList.add("card")
	divFragment.innerHTML = htmlFragment;

	// Agregar el elemento div al div lstReglas
	lstReglas.appendChild(divFragment);
}
function delRegla(){
	const nodoEliminar = event.target.closest('.card');
	if (nodoEliminar) {
        nodoEliminar.remove();
    }
}
function saveRegla(){
	console.log("save");
}

const btn = document.getElementById("btn-add-regla");
btn.addEventListener("click", addRegla);

var loadMain = document.getElementById('lst-reglas');
loadMain?.addEventListener("click", function(event) {
	const enlaceDelete = event.target.closest('.btn-del-regla');
	if (enlaceDelete) {
		delRegla();
	}
	const enlaceAdd = event.target.closest('.btn-save-regla');
	if (enlaceAdd) {
		saveRegla();
	}
});*/