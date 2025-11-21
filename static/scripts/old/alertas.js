function validaSelect(name) {
	var val = document.querySelector(name).value;
	var ok = 0;
	document.querySelector(name).classList.remove("is-invalid");
	if (val === "") {
			ok = 1;
			document.querySelector(name).classList.add("is-invalid");
	}
	return ok;
}
function validaInput(name) {
	var val = $(name).val(); // Obtener el valor del input usando jQuery
	var ok = 0;
	$(name).removeClass("is-invalid"); // Remover la clase is-invalid si existe
	if (val === null || val === "null"  || val === "") {
		ok = 1;
		$(name).addClass("is-invalid"); // Agregar la clase is-invalid si el valor está vacío
	}
	return ok;
}
function addRegla() {
	// Realizar la solicitud AJAX para obtener el contenido de la página
	$.ajax({
		url: '/alertas/select-regla-ajax',
		type: 'GET',
		success: function(data) {
			// Crear un elemento div para el contenido recuperado
			const divFragment = $('<div class="card"></div>').html(data.select_html);
			// Agregar el elemento div al contenedor lstReglas usando jQuery
			$('#lst-reglas').append(divFragment);
		},
		error: function(xhr, status, error) {
			console.error('Error al obtener el contenido AJAX:', error);
		}
	});
}
$("#btn-add-regla").click(addRegla);

function delRegla(){
	const nodoEliminar = event.target.closest('.card');
	if (nodoEliminar) {
		nodoEliminar.remove();
	}
}
function saveRegla(){
	console.log("save");
}

function sendForm(){
	var form = document.getElementById('contactForm');
	form.addEventListener('submit', function(event) {
		var nameInput = document.getElementById('name');
		var emailInput = document.getElementById('email');
		var messageInput = document.getElementById('message');

		// Validar que los campos estén llenos antes de enviar el formulario
		if (!nameInput.value || !emailInput.value || !messageInput.value) {
			alert('Por favor, complete todos los campos.');
			event.preventDefault(); // Evitar que se envíe el formulario
		}
	});
}

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
});

function recuperaSelect(){
	var data = []; // Array para almacenar los datos de los select e inputs
	var vtotal = 0;
	$('.sys-reglas .card').each(function() { // Recorrer cada card dentro de sys-reglas
		var metrica = $(this).find('select[name="cbo_metrica"]').val(); // Obtener el valor del select de metrica
		var operador = $(this).find('select[name="cbo_operador"]').val(); // Obtener el valor del select de operador
		var cantidad = $(this).find('input[name="cantidad"]').val(); // Obtener el valor del input de cantidad
		// Crear un objeto con los datos recuperados
		var regla = {
			"metrica": metrica,
			"operador": operador,
			"cantidad": cantidad
		};
		data.push(regla); // Agregar el objeto al array data
	});
	var jsonData = JSON.stringify(data); // Convertir el array data a formato JSON
	console.log(jsonData); // Mostrar el array JSON en la consola para verificar
	return jsonData;
}
function recuperaSelectValida(){
	var vtotal = 0;
	$('.sys-reglas .card').each(function() { // Recorrer cada card dentro de sys-reglas
		//valida
		var fmetrica = $('select[name="cbo_metrica"]');
		var foperador = $('select[name="cbo_operador"]');
		var fcantidad = $('input[name="cantidad"]');
		var vmetrica = validaInput(fmetrica);
		var voperador = validaInput(foperador);
		var vcantidad = validaInput(fcantidad);
		vtotal+= vmetrica+voperador+vcantidad;
	});
	return vtotal;
}
function loadSelectCampaign(){
	var plataforma = $("#cbo_plataforma").val();
	$.ajax({
		url: '/alertas/select-campaign-ajax',
		type: 'GET',
		data: {plataforma: plataforma},
		success: function(data) {
			// Agregar el elemento div al contenedor lstReglas usando jQuery
			$('#load-cbo-campaign').html(data.select_html);
			$('.select-filter').selectize({sortField: 'text'});
		},
		error: function(xhr, status, error) {
			console.error('Error al obtener el contenido AJAX:', error);
		}
	});
	//console.log("campaign: "+plataforma);
}
function loadLista(){
	var plataforma 	= $("#cbo_plataforma").val();
	var src_camp 	= $("#txt_camp").val();
	var src_regla 	= $("#txt_regla").val();
	$("#lst-alerts").html("<div class='loading'></div>");
	$("#lst-alerts").load("/alertas/listado-ajax",{plataforma:plataforma,src_camp:src_camp,src_regla:src_regla});
}
function loadListaPapelera(){
	var plataforma 	= $("#cbo_plataforma").val();
	var src_camp 	= $("#txt_camp").val();
	var src_regla 	= $("#txt_regla").val();
	$("#lst-alerts-papelera").html("<div class='loading'></div>");
	$("#lst-alerts-papelera").load("/alertas/papelera-ajax",{plataforma:plataforma,src_camp:src_camp,src_regla:src_regla});
}
function saveAlerta(){
	var vname = validaInput('input[name="txt_name"]');
	var vplataform = validaInput('select[name="cbo_plataforma"]');
	var vcampaign = validaInput('select[name="cbo_campaign"]');
	var vreglas = recuperaSelectValida();
	var vhidden = validaInput('input[name="txt_reglas"]');
	var total = vname+vplataform+vcampaign+vreglas;
	console.log(total);
	if(total==0){
		var freglas = recuperaSelect();
		$("#txt_reglas").val(freglas);
	}else{
		return false;
	}
}
function changeSymbol(){
	var symbol = $(event.target).find('option:selected').attr('data-symbol');
	var mySymbolElement = $(event.target).closest('.card').find('.my-symbol');
	if(symbol=="None" || symbol==""){
		symbol = "";
	}
	mySymbolElement.html(symbol);
	console.log(symbol);
}
$(document).ready(function() {
	function createEmailTag(email) {
		return $('<div class="email-tag"></div>')
			.append($('<span></span>').text(email))
			.append($('<span class="remove">&times;</span>'));
	}
	$(document).on('click', '#tags-email .remove', function() {
	    $(this).parent().remove();
		updateEmailList();
	});
	$('#emailInput').on('keydown', function(e) {
		if (e.key === 'Enter' || e.key === ',') {
			e.preventDefault();
			var email = $(this).val().trim();
			if (email && validateEmail(email)) {
				var emailTag = createEmailTag(email);
				$('.email-input-container').append(emailTag);
				$(this).val('');
				updateEmailList();
			}
		}
	});
	function validateEmail(email) {
		var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		return re.test(email);
	}
	function updateEmailList() {
		var emails = [];
		$('.email-tag span:first-child').each(function() {
			emails.push($(this).text());
		});
		$('#emailList').val(JSON.stringify(emails));
	}
	//Phone
	function createPhoneTag(email) {
		return $('<div class="phone-tag"></div>')
			.append($('<span></span>').text(email))
			.append($('<span class="remove">&times;</span>'));
	}
	$(document).on('click', '#tags-phone .remove', function() {
	    $(this).parent().remove();
		updatePhoneList();
	});
	$('#phoneInput').on('keydown', function(e) {
		if (e.key === 'Enter' || e.key === ',') {
			e.preventDefault();
			var email = $(this).val().trim();
			if (email && validatePhone(email)) {
				var phoneTag = createPhoneTag(email);
				$('.phone-input-container').append(phoneTag);
				$(this).val('');
				updatePhoneList();
			}
		}
	});
	function validatePhone(phone) {
		var re = /^\+?[1-9]\d{1,14}$/;
		return re.test(phone);
	}
	function updatePhoneList() {
		var emails = [];
		$('.phone-tag span:first-child').each(function() {
			emails.push($(this).text());
		});
		$('#phoneList').val(JSON.stringify(emails));
	}
});
//[{"metrica":"CPA","operador":"Igual que [=]","cantidad":"15"},{"metrica":"Consumo","operador":"Igual que [=]","cantidad":"250"}]
//$("#btn-save-alerta").click(saveAlerta);
loadLista();
loadListaPapelera();
$("#btn-filtrar").click(loadLista);
$("#btn-filtrar-papelera").click(loadListaPapelera);
$("#cbo_plataforma").change(loadSelectCampaign);
$("#lst-reglas").on("change","select[name='cbo_metrica']",changeSymbol);
$("#form-alert").on("submit",saveAlerta);
//$('.select-filter').selectize({sortField: 'text'});
$(function() {
	var dateFormat = "yy-mm-dd",
		from = $( "#txt_fecini" ).datepicker({
			defaultDate: "+1w",
			dateFormat: dateFormat,
			changeMonth: true,
			numberOfMonths: 2
		}).on( "change", function() {
			to.datepicker( "option", "minDate", getDate( this ) );
		}),
		to = $( "#txt_fecfin" ).datepicker({
			defaultDate: "+1w",
			dateFormat: dateFormat,
			changeMonth: true,
			numberOfMonths: 2
		}).on( "change", function() {
			from.datepicker( "option", "maxDate", getDate( this ) );
		});
 
	function getDate( element ) {
		var date;
		try {
			date = $.datepicker.parseDate( dateFormat, element.value );
		} catch( error ) {
			date = null;
		}
		return date;
	}
});