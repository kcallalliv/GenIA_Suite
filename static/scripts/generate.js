function generateImageIA(){
	var formData = $("#form-iagenerate-save").serialize();
	$("#load_generate-content").html("<div class='loading'><div class='lds-ripple'><div></div><div></div></div></div>");
	$.ajax({
		url: '/proyectos/colecciones/image-article/image',
		type: 'GET',
		data: formData,
		success: function(data) {
			var imagen = data.imagen_temporal;
			var img = `<img src='${imagen}'>`;
			$('#load_generate-content').html(img);
		},
		error: function(xhr, status, error) {
			$('#load_generate-content').html("Error al obtener la imagen");
			console.error('Error al obtener el contenido AJAX:', error);
		}
	});
}
$("#main").on("click","#btn-generar",generateImageIA);