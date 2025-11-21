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
function addCampaign(){
	var v01 = validaSelect("#txt_camp-id");
	var v02 = validaSelect("#txt_camp-name");
	var v03 = validaSelect("#cbo_plataforma");
	var v04 = validaSelect("#utm_campaign");
	var v05 = validaSelect("#utm_content");
	var v06 = validaSelect("#utm_source");
	var v07 = validaSelect("#utm_medium");
	var v08 = validaSelect("#utm_term");
	var total = v01+v02+v03+v04+v05+v06+v07+v08;
	if(total==0){
		$(this).submit();
	}else{
		return false;
	}
}
function loadLista(){
	var plataforma 	= $("#cbo_plataforma").val();
	var camp_id 	= $("#txt_camp-id").val();
	var camp_name 	= $("#txt_camp-name").val();
	$("#lst-campaigns").html("<div class='loading'></div>");
	$("#lst-campaigns").load("/campaigns/listado-ajax",{plataforma:plataforma,camp_id:camp_id,camp_name:camp_name});
}
function loadCampaignPapelera(){
	var plataforma 	= $("#cbo_plataforma").val();
	var camp_id 	= $("#txt_camp-id").val();
	var camp_name 	= $("#txt_camp-name").val();
	$("#lst-campaigns-papelera").html("<div class='loading'></div>");
	$("#lst-campaigns-papelera").load("/campaigns/papelera-ajax",{plataforma:plataforma,camp_id:camp_id,camp_name:camp_name});
}
//$("#btn-guardar").click(addCampaign);
$("#btn-filtrar").click(loadLista);
$("#form-campaign").on("submit",addCampaign);
$("#btn-camp-papelera-filtrar").click(loadCampaignPapelera);
loadLista();
loadCampaignPapelera()
$(function() {
	/*$('#txt_fecfin').datepicker({
		showButtonPanel: true,
		dateFormat: 'yy-mm-dd',
	});*/
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