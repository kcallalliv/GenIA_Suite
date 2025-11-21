document.addEventListener('DOMContentLoaded', () => {
	const tabs = document.querySelectorAll('.tab');
	const tabContents = document.querySelectorAll('.tab-content');
	tabs.forEach(tab => {
		tab.addEventListener('click', () => {
			tabs.forEach(item => item.classList.remove('active'));
			tabContents.forEach(content => content.classList.remove('active'));
			tab.classList.add('active');
			const targetTabId = tab.dataset.tab;
			document.getElementById(targetTabId).classList.add('active');
		});
	});
});
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
function getResult(){
	var v01 = validaSelect("select[name='cbo_fuente']");
	var v02 = validaSelect("select[name='cbo_keyword']");
	var v03 = validaInput("input[name='txt_custom_keyword']");
	var v04 = validaSelect("select[name='cbo_tipo_articulo']");
	var v05 = validaInput("input[name='txt_article']");
	var total = v01+v04;
	if(total==0){
		var vfuente = document.querySelector("#cbo_fuente").value;
		var vkeyword = $("#cbo_keyword").val();
		var vtipo_articulo = document.querySelector("#cbo_tipo_articulo").value;
		var varticle = document.querySelector("#txt_article").value;
		var vcustom_keyword = document.querySelector("#txt_custom_keyword").value;
		var vkeyword;
        // Verifica si el checkbox está marcado
        if($('#chk_custom_keyword_toggle').is(':checked')){
            vkeyword = document.querySelector("#txt_custom_keyword").value;
        }else{
            vkeyword = $("#cbo_keyword").val();
        }
		$("#load_generate-content").html("<div class='loading'><div class='lds-ripple'><div></div><div></div></div></div>");
		$.ajax({
			url: '/generate-content/article-result',
			type: 'GET',
			data: {
				fuente: vfuente,
				keyword: vkeyword,
				tipo_articulo: vtipo_articulo,
				article: varticle,
				custom_keyword: vcustom_keyword
			},
			success: function(data) {
				$('#load_generate-content').html(data);
			},
			error: function(xhr, status, error) {
				console.error('Error al obtener el contenido AJAX:', error);
			}
		});
	}else{
		return false;
	}
}
function addSelectKeyword() {
	var cbo_fuente = $("#cbo_fuente").val();
	var furl = "";
	var ftable = "";
	if(cbo_fuente=="semrush"){
		furl = "/generate-content/select-semrush-keyword";
		ftable = "/generate-content/list-semrush";
	}else if(cbo_fuente=="search-console"){
		furl = "/generate-content/select-search-console-keyword";
		ftable = "/generate-content/list-search-console";
	}else{
		furl = "";
	}
	console.log("keyword"+cbo_fuente+"url:"+furl);
	$("#select-keyword").html("hola");
	$("#select-keyword").html("<div class='loading'><div class='lds-ellipsis'><div></div><div></div><div></div><div></div></div></div>");
	if(furl!=""){
		$.ajax({
			url: furl,
			type: 'GET',
			success: function(data) {
				const divFragment = data;
				$('#select-keyword').html(divFragment);
			},
			error: function(xhr, status, error) {
				console.error('Error al obtener el contenido AJAX:', error);
			}
		});
	}
	//Cargar tablas
	$("#genia-table").html("<div class='lds-ripple'><div></div><div></div></div>");
	$("#genia-table").load(ftable);
}
function addTipoArticulo() {
	$("#select-tipo-articulo").html("<div class='loading'><div class='lds-ellipsis'><div></div><div></div><div></div><div></div></div></div>");
	$.ajax({
		url: '/generate-content/select-tipo-contenido',
		type: 'GET',
		success: function(data) {
			const divFragment = data;
			$('#select-tipo-articulo').html(divFragment);
		},
		error: function(xhr, status, error) {
			console.error('Error al obtener el contenido AJAX:', error);
		}
	});
}
function loadPageFilter(){
	$("#load_generate-content").html("<div class='loading'><div class='lds-ripple'><div></div><div></div></div></div>");
	$.ajax({
		url: '/generate-content/slide-filter',
		type: 'GET',
		success: function(data_generate_filter) {
			$('#load_generate-content').html(data_generate_filter);
			addSelectKeyword();
			addTipoArticulo();
		},
		error: function(xhr, status, error) {
			console.error('Error al cargar generate-filter:', error);
		}
	})
}
function closeBanner(){
	console.log("close");
	$(".sys-banner").addClass("hidden");
}
function habilitarBoxCustomKeyword(){
	var $checkbox = $('#chk_custom_keyword_toggle');
	var $textBox = $('#txt_custom_keyword');
	$textBox.prop('disabled', !$checkbox.is(':checked'));
}
$("#main").on("click","#chk_custom_keyword_toggle",habilitarBoxCustomKeyword);
$("#main").on("click","#btn-generate-content",getResult);
$("#main").on("click","#btn-generate-new-article",loadPageFilter);
$("#main").on("change","#cbo_fuente",addSelectKeyword);
$("#main").on("click","#btn-banner-close",closeBanner);
loadPageFilter();
//addSelectKeyword();
