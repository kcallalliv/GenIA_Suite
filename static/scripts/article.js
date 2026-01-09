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
function generaImagen() {
	var v01 = validaSelect("#cbo_tipo_articulo");
	var v02 = validaSelect("#txt_titulo");
	var total = v01+v02;
	if (total == 0) {
		const $inputTitle = $("#txt_titulo");
		const $loadContainer = $("#load-image");
		const loadingHtml = "<div class='loading loader-temp-image' id='loader-temp'><div class='lds-ellipsis'><div></div><div></div><div></div><div></div></div></div>";
		$loadContainer.append(loadingHtml);
		//Datos
		var data_tipo = $("#cbo_tipo_articulo").val();
		var data_description = $("#cbo_tipo_articulo").find('option:selected').data('description');
		var data_tema = $("#txt_tema").val();
		var data_keyword = $("#txt_keyword").val();
		var data_titulo = $("#txt_titulo").val();
		var data_motivo = $("#txt_motivo").val();
		//genera promt
		$.ajax({
			url: "generated-promt",
			type: 'POST',
			data: {
				tipo: data_tipo,
				description: data_description,
				tema: data_tema,
				keyword: data_keyword,
				titulo: data_titulo,
				motivo: data_motivo
			},
			success: function (data) {
				const data_promt = data.promt;
				$("#txt_promt_image").val(data_promt);
				//Genera Imagen
				var imageModel = $("#cbo_image_model").val();
				var aspectRatio = $("#cbo_image_aspect").val();
				var files = $("#image_reference_files")[0].files;
				if (files.length > 3) {
					alert("Puedes subir máximo 3 imágenes de referencia.");
					$(".loader-temp-image").remove();
					return;
				}
				var formData = new FormData();
				formData.append("tipo", data_tipo);
				formData.append("tema", data_tema);
				formData.append("keyword", data_keyword);
				formData.append("promt", data_promt);
				formData.append("model_label", imageModel);
				formData.append("aspect_ratio", aspectRatio);
				for (var i = 0; i < files.length; i++) {
					formData.append("files", files[i]);
				}

				$.ajax({
					url: "generated-image",
					type: 'POST',
					data: formData,
					processData: false,
					contentType: false,
					success: function (data) {
						const imageUrl = data.imagen_temporal;
						if (data.imagen_base64) {
							const mimeType = data.imagen_mime_type || "image/png";
							const base64Url = "data:" + mimeType + ";base64," + data.imagen_base64;
							$("#ia_img").css("background-image", "url(" + base64Url + ")");
						}
						$("#txt_image").val(imageUrl);
						$("#txt_photo-descarga").attr("href",imageUrl);
						if (!data.imagen_base64) {
							$("#ia_img").css("background-image", "url(" + imageUrl + ")");
						}
						$(".loader-temp-image").remove();
					},
					error: function (xhr, status, error) {
						console.error('Error al obtener el contenido AJAX:', error);
						alert("No se pudo generar la imagen. Revisa el prompt y las imágenes de referencia.");
						$(".loader-temp-image").remove();
					}
				});


			},
			error: function (xhr, status, error) {
				console.error('Error al obtener el contenido AJAX:', error);
			}
		});
	}
}
function descargarImagen(e) {
	if (e) {
		e.preventDefault();
	}
	var data_photo = $("#txt_image").val();

	if (data_photo && data_photo.trim().length > 0) {
		var a = document.createElement('a');
		a.href = data_photo;
		try {
			var urlObj = new URL(data_photo);
			var path = urlObj.pathname;
			var defaultName = path.substring(path.lastIndexOf('/') + 1);
			a.download = defaultName || 'imagen_descargada.png';
		} catch (e) {
			a.download = 'imagen_descargada.png';
			console.error("Fallo al parsear la URL, usando nombre por defecto.", e);
		}

		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
	} else {
		console.warn("No se encontraron datos válidos de imagen para descargar.");
	}
}
function generaTitle() {
	var v01 = validaSelect("#cbo_tipo_articulo");
	//var v02 = validaSelect("#txt_tema");
	var total = v01;
	if (total == 0) {
		const $inputTitle = $("#txt_titulo");
		const $loadContainer = $("#load-titulo");
		$inputTitle.hide();
		const loadingHtml = "<div class='loading' id='loader-temp'><div class='lds-ellipsis'><div></div><div></div><div></div><div></div></div></div>";
		$loadContainer.append(loadingHtml);
		//Datos
		var data_tipo = $("#cbo_tipo_articulo").val();
		var data_tema = $("#txt_tema").val();
		var data_keyword = $("#txt_keyword").val();
		$.ajax({
			url: "generated-title",
			type: 'GET',
			data: {
				tipo: data_tipo,
				tema: data_tema,
				keyword: data_keyword
			},
			success: function (data) {
				const title = data.title;
				$inputTitle.val(title).show();
				$("#loader-temp").remove();
			},
			error: function (xhr, status, error) {
				console.error('Error al obtener el contenido AJAX:', error);
			}
		});
	}
}
function generaContenido() {
	var v01 = validaSelect("#cbo_tipo_articulo");
	var v02 = validaSelect("#txt_titulo");
	var total = v01 + v02;
	console.log(v01 + "/" + v02);
	if (total == 0) {
		const $inputTitle = $("#txt_content");
		const $loadContainer = $("#load-content");
		//Limpiar
		$inputTitle.show();
		$(".loading").remove();
		//Mostrar loading
		$inputTitle.hide();
		const loadingHtml = "<div class='loading' id='loader-content-temp'><div class='lds-ripple'><div></div><div></div></div></div>";
		$loadContainer.append(loadingHtml);
		//Datos
		var data_tipo = $("#cbo_tipo_articulo").val();
		var data_tema = $("#txt_tema").val();
		var data_titulo = $("#txt_titulo").val();
		var data_keyword = $("#txt_keyword").val();
		var usar_contexto_google = $("#chk_google_context").is(":checked") ? "1" : "0";

		$.ajax({
			url: "article-content",
			type: 'GET',
			data: {
				tipo: data_tipo,
				tema: data_tema,
				titulo: data_titulo,
				keyword: data_keyword,
				usar_contexto_google: usar_contexto_google
			},
			success: function (data) {
				$inputTitle.val(data.texto).show();
				$(".loading").remove();
			},
			error: function (xhr, status, error) {
				$inputTitle.val("Error al obtener el contenido AJAX").show();
				$(".loading").remove();
				console.error('Error al obtener el contenido AJAX:', error);
			}
		});
	}
}
function descargarContenido() {
	var v01 = validaSelect("#cbo_tipo_articulo");
	var v02 = validaSelect("#txt_titulo");
	var total = v01 + v02;

	if (total == 0) {
		// Datos
		var data_tipo = $("#cbo_tipo_articulo").val();
		var data_tema = $("#txt_tema").val();
		var data_titulo = $("#txt_titulo").val();
		var data_keyword = $("#txt_keyword").val();
		var data_content = $("#txt_content").val();
		var data_image = $("#txt_image").val();

		// ⚠️ INICIAMOS LA CARGA VISUAL AQUÍ SI ES NECESARIO

		$.ajax({
			url: "download-generated-article",
			type: 'POST',
			data: {
				tipo: data_tipo,
				tema: data_tema,
				titulo: data_titulo,
				content: data_content,
				keyword: data_keyword,
				image_url: data_image
			},
			// 🛠️ CONFIGURACIÓN CLAVE PARA DESCARGA DE ARCHIVOS BINARIOS
			xhrFields: {
				responseType: 'blob' // Indica a jQuery que espere una respuesta binaria (archivo)
			},
			success: function (blob, status, xhr) {
				// El backend debe enviar el Content-Disposition header con el nombre del archivo.

				// 1. Obtener el nombre del archivo (si el backend lo proporciona)
				// Usaremos un nombre por defecto si no se puede extraer.
				var fileName = "articulo.docx";
				var disposition = xhr.getResponseHeader('Content-Disposition');
				if (disposition && disposition.indexOf('attachment') !== -1) {
					var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
					var matches = filenameRegex.exec(disposition);
					if (matches != null && matches[1]) fileName = matches[1].replace(/['"]/g, '');
				}

				// 2. Crear una URL de descarga temporal para el Blob
				var url = window.URL.createObjectURL(blob);

				// 3. Crear un enlace oculto y simular un clic
				var a = document.createElement('a');
				a.href = url;
				a.download = fileName; // Nombre del archivo
				document.body.appendChild(a);
				a.click();

				// 4. Limpiar
				window.URL.revokeObjectURL(url);
				a.remove();

				// ⚠️ QUITAR LA CARGA VISUAL AQUÍ SI ES NECESARIO
			},
			error: function (xhr, status, error) {
				console.error('Error al descargar el archivo Word:', error);
				alert("No se pudo descargar el archivo Word. Revisa que el contenido esté generado e intenta nuevamente.");
			}
		});
	} else {
		alert("Completa Tipo de contenido y Título antes de descargar el Word.");
	}
}
function descargarContenidoHTML() {
	var v01 = validaSelect("#cbo_tipo_articulo");
	var v02 = validaSelect("#txt_titulo");
	var total = v01 + v02;

	if (total == 0) {
		// Datos
		var data_tipo = $("#cbo_tipo_articulo").val();
		var data_tema = $("#txt_tema").val();
		var data_titulo = $("#txt_titulo").val();
		var data_keyword = $("#txt_keyword").val();
		var data_content = $("#txt_content").val();
		var data_image = $("#txt_image").val();

		// ⚠️ INICIAMOS LA CARGA VISUAL AQUÍ SI ES NECESARIO

		$.ajax({
			url: "download-html",
			type: 'POST',
			data: {
				tipo: data_tipo,
				tema: data_tema,
				titulo: data_titulo,
				content: data_content,
				keyword: data_keyword,
				image_url: data_image
			},
			// 🛠️ CONFIGURACIÓN CLAVE PARA DESCARGA DE ARCHIVOS BINARIOS
			xhrFields: {
				responseType: 'blob' // Indica a jQuery que espere una respuesta binaria (archivo)
			},
			success: function (blob, status, xhr) {
				// El backend debe enviar el Content-Disposition header con el nombre del archivo.

				// 1. Obtener el nombre del archivo (si el backend lo proporciona)
				// Usaremos un nombre por defecto si no se puede extraer.
				var fileName = "articulo.html";
				var disposition = xhr.getResponseHeader('Content-Disposition');
				if (disposition && disposition.indexOf('attachment') !== -1) {
					var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
					var matches = filenameRegex.exec(disposition);
					if (matches != null && matches[1]) fileName = matches[1].replace(/['"]/g, '');
				}

				// 2. Crear una URL de descarga temporal para el Blob
				var url = window.URL.createObjectURL(blob);

				// 3. Crear un enlace oculto y simular un clic
				var a = document.createElement('a');
				a.href = url;
				a.download = fileName; // Nombre del archivo
				document.body.appendChild(a);
				a.click();

				// 4. Limpiar
				window.URL.revokeObjectURL(url);
				a.remove();

				// ⚠️ QUITAR LA CARGA VISUAL AQUÍ SI ES NECESARIO
			},
			error: function (xhr, status, error) {
				console.error('Error al descargar el archivo Word:', error);
				alert("No se pudo descargar el archivo HTML. Revisa que el contenido esté generado e intenta nuevamente.");
			}
		});
	} else {
		alert("Completa Tipo de contenido y Título antes de descargar el HTML.");
	}
}
function guardarContenido() {

}
$("#select-tipo-articulo").html("<div class='loading'><div class='lds-ellipsis'><div></div><div></div><div></div><div></div></div></div>");
$("#select-tipo-articulo").load("select-tipo-contenido");
$("#main").on("click", "#btn-generar-title", generaTitle);
$("#main").on("click", "#btn-generar", generaContenido);
$("#main").on("click", ".btn-descargar-word", descargarContenido);
$("#main").on("click", ".btn-descargar-html", descargarContenidoHTML);
$("#main").on("click", ".btn-descargar-image", descargarImagen);
$("#main").on("click", "#btn-save", guardarContenido);
/*popup*/
// Función para abrir el popup
function openPopup() {
	const popup = document.getElementById('popup-article');
	popup.classList.add('active');
	document.body.style.overflow = 'hidden';
}

// Función para cerrar el popup
function closePopup() {
	const popup = document.getElementById('popup-article');
	popup.classList.remove('active');
	document.body.style.overflow = '';
}

// Cerrar al hacer click fuera del popup
document.getElementById('popup-article').addEventListener('click', function (e) {
	if (e.target === this) {
		closePopup();
	}
});

// Cerrar con tecla ESC
document.addEventListener('keydown', function (e) {
	if (e.key === 'Escape') {
		closePopup();
	}
});
// Función para parsear el contenido del artículo
function parseArticleContent(content) {
	
}

// Función para cargar el contenido del artículo
function loadArticleContent(content, keyword = '') {
	const container = document.getElementById('article-container');
	container.innerHTML = parseArticleContent(content);

	if (keyword) {
		document.getElementById('article-keyword').textContent = keyword;
	}
}
function copyArticle() {
	const container = document.getElementById('article-container');

	// 1. Obtener el HTML con formato de la sección (incluye la etiqueta <img>)
	const htmlContent = container.innerHTML;

	// 2. Crear un objeto ClipboardItem para manejar múltiples formatos
	const blobHtml = new Blob([htmlContent], { type: 'text/html' });
	const blobPlain = new Blob([container.innerText], { type: 'text/plain' });

	const item = new ClipboardItem({
		'text/html': blobHtml,
		'text/plain': blobPlain
	});

	// 3. Escribir al portapapeles. El navegador lee las URLs absolutas del HTML 
	// y descarga la imagen para incluirla en la copia.
	navigator.clipboard.write([item])
		.then(() => {
			alert('Artículo copiado al portapapeles con formato e imágenes.');
		})
		.catch(err => {
			console.error('Error al copiar el contenido formateado:', err);
			//alert('Error al copiar el formato. Se copió solo texto plano.');
			// Fallback: Si falla el HTML, intenta copiar solo texto plano como fallback
			navigator.clipboard.writeText(container.innerText);
		});
}

// Función para publicar
function publishArticle() {
	if (confirm('¿Estás seguro de que deseas publicar este artículo?')) {
		alert('Artículo publicado correctamente');
		closePopup();
	}
}

// Cargar contenido de ejemplo al hacer click en el botón demo
window.addEventListener('DOMContentLoaded', function () {
	const demoButton = document.querySelector('.popup-btn-open');
	demoButton.addEventListener('click', function () {
		var data_keyword = $("#txt_keyword").val();
		var data_photo = $("#txt_image").val();
		var data_content = $("#txt_content").val();
		//var data_content = exampleContent;
		console.log(data_keyword);
		console.log(data_content);
		$("#article-container").html(data_content);
		$("#article-photo").css("background-image", "url(" + data_photo + ")");
		/*$.ajax({
			url: "generated-html",
			type: 'POST',
			data: {
				content: data_content,
				keyword: data_keyword
			},
			success: function (data) {
				const html = data.html;
				$("#article-container").html(html);
			},
			error: function (xhr, status, error) {
				console.error('Error al obtener el contenido AJAX:', error);
			}
		});*/
	});
});


let selectedImages = [];

// Abrir galería
function openGallery() {
	document.getElementById('popup-gallery').classList.add('active');
	document.body.style.overflow = 'hidden';
	var pid = $("#txt_pid").val();
	console.log(pid);
	$("#gallery-grid").html("<div class='loading'>cargando</div>");
	$("#gallery-grid").load("images", { pid: pid });
}
// Cerrar galería item
function closeGalleryItem(clickedElement) {
	var $element = $(clickedElement);
	var myimage = $element.attr("data-image");
	var myphoto = $element.attr("data-photo");
	$("#txt_image").val(myimage);
	$("#txt_photo").val(myphoto);
	$("#ia_img").css("background-image", "url(" + myphoto + ")");
	console.log(myimage);
	document.getElementById('popup-gallery').classList.remove('active');
	document.body.style.overflow = '';
}
// Cerrar galería
function closeGallery() {
	document.getElementById('popup-gallery').classList.remove('active');
	document.body.style.overflow = '';
	selectedImages = [];
	updateSelectedCount();
}

// Cerrar al hacer click fuera
document.getElementById('popup-gallery').addEventListener('click', function (e) {
	if (e.target === this) {
		closeGallery();
	}
});

// Cerrar con ESC
document.addEventListener('keydown', function (e) {
	if (e.key === 'Escape') {
		const popup = document.getElementById('popup-gallery');
		if (popup.classList.contains('active')) {
			closeGallery();
		}
	}
});

// Buscar imágenes (simulado)
function searchImages() {
	const query = document.getElementById('search-input').value;
	const grid = document.getElementById('gallery-grid');
	const loadingState = document.getElementById('loading-state');

	if (!query.trim()) {
		alert('Por favor ingresa un término de búsqueda');
		return;
	}

	// Mostrar loading
	grid.innerHTML = '<div class="loading-state"><span class="material-icons">hourglass_empty</span><p>Buscando imágenes...</p></div>';

	// Simular búsqueda (en producción, aquí harías una petición AJAX)
	setTimeout(() => {
		// Imágenes de ejemplo (usando placeholder)
		const images = Array.from({ length: 12 }, (_, i) => ({
			id: i + 1,
			url: `https://picsum.photos/400/400?random=${i + 1}`,
			alt: `${query} ${i + 1}`
		}));

		renderGallery(images);
	}, 1000);
}

// Renderizar galería
function renderGallery(images) {
	const grid = document.getElementById('gallery-grid');
	grid.innerHTML = '';

	images.forEach(image => {
		const item = document.createElement('div');
		item.className = 'gallery-item';
		item.dataset.imageId = image.id;
		item.dataset.imageUrl = image.url;

		item.innerHTML = `
			<img src="${image.url}" alt="${image.alt}" loading="lazy">
			<div class="gallery-item-overlay">
				<div class="gallery-item-check">
					<span class="material-icons">check</span>
				</div>
			</div>
		`;

		item.addEventListener('click', () => toggleImage(item));
		grid.appendChild(item);
	});
}

// Toggle selección de imagen
function toggleImage(item) {
	const imageId = item.dataset.imageId;
	const imageUrl = item.dataset.imageUrl;

	if (item.classList.contains('selected')) {
		item.classList.remove('selected');
		selectedImages = selectedImages.filter(img => img.id !== imageId);
	} else {
		item.classList.add('selected');
		selectedImages.push({ id: imageId, url: imageUrl });
	}

	updateSelectedCount();
}

// Actualizar contador
function updateSelectedCount() {
	const count = selectedImages.length;
	document.getElementById('selected-count').textContent = count;
	document.getElementById('btn-insert').disabled = count === 0;
}

// Insertar imágenes seleccionadas
function insertImages() {
	if (selectedImages.length === 0) return;

	console.log('Imágenes seleccionadas:', selectedImages);

	// Aquí puedes hacer lo que necesites con las imágenes
	// Por ejemplo, insertarlas en un editor, enviarlas al servidor, etc.

	alert(`Se insertaron ${selectedImages.length} imagen(es)`);

	// Mostrar las URLs en consola
	selectedImages.forEach((img, index) => {
		console.log(`Imagen ${index + 1}:`, img.url);
	});

	closeGallery();
}
