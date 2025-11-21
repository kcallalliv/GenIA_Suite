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
function saveUser(){
	var v01 = validaSelect("#usu_usuario");
	var v02 = validaSelect("#usu_email");
	var v03 = validaSelect("#usu_password");
	var v04 = validaSelect("#cbo_permiso");
	var total = v01+v02+v03+v04;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function updateUser(){
	var v01 = validaSelect("#usu_usuario");
	var v02 = validaSelect("#cbo_permiso");
	var v03 = validaSelect("#usu_email");
	var total = v01+v02+v03;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function updatePerfil(){
	var v01 = validaSelect("#usu_usuario");
	var v02 = validaSelect("#usu_email");
	var total = v01+v02;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function loadLista(){
	var buscar = $("#txt_buscar").val();
	$("#lst-users").html("<div class='loading'></div>");
	$("#lst-users").load("/sistema/users/listado-ajax",{buscar:buscar});
}
function loadPapelera(){
	var buscar = $("#txt_buscar").val();
	$("#lst-users-papelera").html("<div class='loading'></div>");
	$("#lst-users-papelera").load("/sistema/users/papelera-ajax",{buscar:buscar});
}
loadLista();
loadPapelera();
$("#btn-filtrar").click(loadLista);
$("#btn-filtrar-papelera").click(loadPapelera);
$("#form-usuario-save").on("submit",saveUser);
$("#form-usuario-update").on("submit",updateUser);
$("#form-usuario-perfil").on("submit",updatePerfil);
