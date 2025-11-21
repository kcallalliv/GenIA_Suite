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
function savecoleccion(){
	var v01 = validaSelect("#coleccion_name");
	var v02 = validaSelect("#coleccion_description");
	var total = v01+v02;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function updatecoleccion(){
	var v01 = validaSelect("#coleccion_name");
	var v02 = validaSelect("#coleccion_description");
	var total = v01+v02;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function loadLista(){
	/*var fuentes = [];
	$('.source-tag input[type="checkbox"]:checked').each(function(){
		fuentes.push($(this).next('span').text().trim());
	});*/
	var pid = $("#txt_pid").val();
	$("#lst-colecciones").html("<div class='loading'>cargando</div>");
	$("#lst-colecciones").load("view-cards",{pid:pid});
}
function loadPapelera(){
	var buscar = $("#txt_buscar").val();
	$("#lst-colecciones-papelera").html("<div class='loading'>cargando</div>");
	$("#lst-colecciones-papelera").load("papelera-ajax",{buscar:buscar});
}
loadLista();
loadPapelera();
$(".source-tag").click(loadLista);
$("#btn-filtrar-papelera").click(loadPapelera);
$("#form-coleccion-save").on("submit",savecoleccion);
$("#form-coleccion-update").on("submit",updatecoleccion);
