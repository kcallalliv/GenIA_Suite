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
function savePermisosCampaigns(){
	$("#form-permisos").submit();
}
function updateUser(){
	var v01 = validaSelect("#usu_usuario");
	var v02 = validaSelect("#usu_email");
	var total = v01+v02;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function loadListaUsuariosCampagins(){
	var buscar = $("#txt_buscar").val();
	$("#lst-users").html("<div class='loading'></div>");
	$("#lst-users").load("/permisos/listado-ajax",{buscar:buscar});
}
function loadListaUsuariosCampaginsAjax(){
	var buscar = $("#txt_buscar").val();
	var invitado_id = $("#user_id").val();
	$("#lst-campaignsusers").html("<div class='loading'></div>");
	$("#lst-campaignsusers").load("/permisos/campaigns-listado-ajax",{buscar:buscar,invitado_id:invitado_id});
}
loadListaUsuariosCampagins();
loadListaUsuariosCampaginsAjax();
$("#btn-filtrar").click(loadListaUsuariosCampagins);
$("#btn-save").click(savePermisosCampaigns);
$("#form-usuario-update").on("submit",updateUser);
