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
	var v02 = validaSelect("#proyecto_description");
	var total = v01+v02;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function updateProyecto(){
	var v01 = validaSelect("#proyecto_name");
	var v02 = validaSelect("#proyecto_description");
	var total = v01+v02;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function loadLista(){
	var buscar = $("#txt_buscar").val();
	var pid = $("#txt_pid").val();
	$("#lst-link").html("<div class='loading'></div>");
	$("#lst-link").load("listado-ajax",{buscar:buscar,pid:pid});
}
function loadPapelera(){
	var buscar = $("#txt_buscar").val();
	var pid = $("#txt_pid").val();
	$("#lst-link-papelera").html("<div class='loading'></div>");
	$("#lst-link-papelera").load("papelera-ajax",{buscar:buscar,pid:pid});
}
loadLista();
loadPapelera();
$("#btn-filtrar").click(loadLista);
$("#btn-filtrar-papelera").click(loadPapelera);
$("#form-link-save").on("submit",saveProyecto);
$("#form-link-update").on("submit",updateProyecto);
