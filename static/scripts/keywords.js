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
	var fuentes = [];
	$('.source-tag input[type="checkbox"]:checked').each(function(){
		fuentes.push($(this).next('span').text().trim());
	});
	$("#lst-tendencias").html("<div class='loading'>cargando</div>");
	$("#lst-tendencias").load("/proyectos/view-cards",{fuentes: fuentes});
}
function loadPapelera(){
	var buscar = $("#txt_buscar").val();
	$("#lst-tendencias-papelera").html("<div class='loading'>cargando</div>");
	$("#lst-tendencias-papelera").load("/proyectos/papelera-ajax",{buscar:buscar});
}
function loadListaKeywords(){
	var pid = $("#txt_pid").val();
	var fuentes = [];
	$('.source-tag input[type="checkbox"]:checked').each(function(){
		fuentes.push($(this).val());
		//fuentes.push($(this).next('span').text().trim());
	});
	$("#load_keywords_rows").html("<div class='loading'>cargando</div>");
	$("#load_keywords_rows").load("view-table",{fuentes: fuentes,pid:pid});
}
function selectKeyword() {
	var v01 = validaSelect("#cbo_keyword");
	var total = v01;
	if(total==0){
		//Datos
		var data_keyword = $("#cbo_keyword").val();
		$("#txt_keyword").val(data_keyword);
	}
}
function selectFuente() {
	var v01 = validaSelect("#cbo_fuente");
	var total = v01;
	if(total==0){
		const $inputTitle = $("#cbo_keyword");
		const $loadContainer = $("#load-selectkeyword");
		//Limpiar
		$inputTitle.show();
		$(".loading").remove();
		//Mostrar loading
		$inputTitle.hide(); 
		const loadingHtml = "<div class='loading' id='loader-temp'><div class='lds-ellipsis'><div></div><div></div><div></div><div></div></div></div>";
		$loadContainer.append(loadingHtml);
		//Datos
		var data_fuente = $("#cbo_fuente").val();
		$.ajax({
			url: "select-fuente",
			type: 'GET',
			data: {
				fuente: data_fuente
			},
			success: function(data) {
				$inputTitle.val(data).show();
				$("#load-cbo-keyword").html(data);
				$(".loading").remove();
			},
			error: function(xhr, status, error) {
				console.error('Error al obtener el contenido AJAX:', error);
			}
		});
	}
}
function addKeyword(){
	var v01 = validaSelect("#txt_keyword");
	var total = v01;
	if(total==0){
		//Datos
		var data_pid = $("#txt_pid").val();
		var data_keyword = $("#txt_keyword").val();
		$.ajax({
			url: "addkeyword",
			type: 'POST',
			data: {
				pid: data_pid,
				keyword: data_keyword
			},
			success: function(data) {
				loadListaKeywords();
			},
			error: function(xhr, status, error) {
				console.error('Error al obtener el contenido AJAX:', error);
			}
		});
	}
}
loadListaKeywords();
$(".source-tag").click(loadListaKeywords);
$("#btn-filtrar-papelera").click(loadPapelera);
$("#form-proyecto-save").on("submit",saveProyecto);
$("#form-proyecto-update").on("submit",updateProyecto);
$("#main").on("change","#cbo_fuente",selectFuente);
$("#main").on("change","#cbo_keyword",selectKeyword);
$("#main").on("click","#btn_addkeyword",addKeyword);