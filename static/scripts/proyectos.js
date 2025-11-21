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
function saveProyecto(){
	var v01 = validaSelect("#proyecto_name");
	var total = v01+v02;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function updateProyecto(){
	var v01 = validaSelect("#proyecto_name");
	var total = v01+v02;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function loadLista(){
	var buscar = $("#txt_buscar").val();
	$("#lst-proyecto").html("<div class='loading'></div>");
	$("#lst-proyecto").load("listado-ajax",{buscar:buscar});
}
function loadPapelera(){
	var buscar = $("#txt_buscar").val();
	$("#lst-proyecto-papelera").html("<div class='loading'></div>");
	$("#lst-proyecto-papelera").load("papelera-ajax",{buscar:buscar});
}
loadLista();
loadPapelera();
$("#btn-filtrar").click(loadLista);
$("#btn-filtrar-papelera").click(loadPapelera);
$("#form-proyecto-save").on("submit",saveProyecto);
$("#form-proyecto-update").on("submit",updateProyecto);
