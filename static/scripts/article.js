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
			url: "article-title",
			type: 'GET',
			data: {
				tipo: data_tipo,
				tema: data_tema,
				keyword: data_keyword
			},
			success: function (data) {
				$inputTitle.val(data).show();
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

		$.ajax({
			url: "article-content",
			type: 'GET',
			data: {
				tipo: data_tipo,
				tema: data_tema,
				titulo: data_titulo,
				keyword: data_keyword
			},
			success: function (data) {
				$inputTitle.val(data).show();
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
	var v02 = validaSelect("#txt_tema");
	var v03 = validaSelect("#txt_titulo");
	var total = v01 + v02 + v03;

	if (total == 0) {
		// Datos
		var data_tipo = $("#cbo_tipo_articulo").val();
		var data_tema = $("#txt_tema").val();
		var data_titulo = $("#txt_titulo").val();
		var data_keyword = $("#txt_keyword").val();
		var data_content = $("#txt_content").val();

		// ⚠️ INICIAMOS LA CARGA VISUAL AQUÍ SI ES NECESARIO

		$.ajax({
			url: "download-generated-article",
			type: 'POST',
			data: {
				tipo: data_tipo,
				tema: data_tema,
				titulo: data_titulo,
				content: data_content,
				keyword: data_keyword
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
				// ⚠️ QUITAR LA CARGA VISUAL AQUÍ SI ES NECESARIO
			}
		});
	}
}
function guardarContenido() {

}
$("#select-tipo-articulo").html("<div class='loading'><div class='lds-ellipsis'><div></div><div></div><div></div><div></div></div></div>");
$("#select-tipo-articulo").load("select-tipo-contenido");
$("#main").on("click", "#btn-generar-title", generaTitle);
$("#main").on("click", "#btn-generar", generaContenido);
$("#main").on("click", "#btn-descargar", descargarContenido);
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
	// Esta es la validación CLAVE que previene el error 'split' si content es undefined/null.
	var photo = $("#txt_photo").val();
	if (typeof content !== 'string' || !content) {
		console.error("Error: La función parseArticleContent recibió un argumento nulo o no válido.");
		return '';
	}
	// ===================================================

	const lines = content.split('\n');
	let html = '';
	let currentSection = '';
	let inArticleLinksSection = false; // Flag para controlar la sección de enlaces sugeridos

	lines.forEach(line => {
		line = line.trim();
		if (!line) return;

		if (line.startsWith('[title]')) {
			const title = line.replace('[title]', '').trim();

			// Detecta si es el título principal o el título de la sección de URLs Sugeridas
			if (title.toLowerCase().includes('urls sugeridas')) {
				// Cierra el div.article-links anterior si estaba abierto
				if (inArticleLinksSection) {
					html += `</div>`;
				}
				html += `<div class="article-links-title"><span class="material-icons">link</span>${title}</div>`;
				html += `<div class="article-links">`; // Abre el contenedor de enlaces sugeridos
				inArticleLinksSection = true;
				currentSection = 'links-title';
			} else if (currentSection === '') {
				html += `<img src="${photo}">`;
				html += `<h1 class="article-title">${title}</h1>`;
				currentSection = 'title';
			} else {
				html += `<h3 class="section-title">${title}</h3>`; // Títulos intermedios/subtítulos H3
			}

		} else if (line.startsWith('[intro]')) {
			const intro = line.replace('[intro]', '').trim();
			html += `<div class="article-intro">${intro}</div>`;
		} else if (line.startsWith('[subtitle]')) {
			const subtitle = line.replace('[subtitle]', '').trim();
			html += `<h2 class="article-subtitle">${subtitle}</h2>`;
		} else if (line.startsWith('[text]')) {
			let text = line.replace('[text]', '').trim();

			// 🛠️ CORRECCIÓN APLICADA: Nueva Expresión Regular para [link=URL]TEXTO[/link]
			// Captura 1: URL (.*?)
			// Captura 2: Texto del enlace (.*?)
			const linkRegex = /\[link=(.*?)\](.*?)\[\/link\]/g;

			// Reemplazar el formato completo con la etiqueta <a>
			text = text.replace(linkRegex, (match, url, linkText) => {
				// 'url' y 'linkText' son el resultado de las capturas (.*?)
				if (url && linkText) {
					return `<a href="${url}" target="_blank" class="text-link">${linkText}</a>`;
				}
				// Si no coincide o falta algo, devuelve el match original para que se vea el error en el texto.
				return match;
			});

			html += `<p class="article-text">${text}</p>`;

		} else if (line.startsWith('[item-link=')) {
			// Manejo seguro del match para URLs sugeridas (previene el error si la regex falla)
			const match = line.match(/\[item-link=(.*?)\]/);
			if (match && match[1]) {
				const url = match[1];

				html += `
					<a href="${url}" target="_blank" class="article-link">
						<span class="material-icons">open_in_new</span>
						<span>${url}</span>
					</a>
				`;
			}
		}
	});

	// Cierra el div.article-links si la sección estaba abierta al final del contenido
	if (inArticleLinksSection) {
		html += `</div>`;
	}

	// Añadir metadata al final
	const date = new Date().toLocaleDateString('es-ES', {
		day: 'numeric',
		month: 'long',
		year: 'numeric'
	});
	html += `
		<div class="article-meta">
			<div class="article-meta-item">
				<span class="material-icons">calendar_today</span>
				<span>${date}</span>
			</div>
			<div class="article-meta-item">
				<span class="material-icons">person</span>
				<span>Redacción Claro</span>
			</div>
			<div class="article-meta-item">
				<span class="material-icons">label</span>
				<span id="article-keyword">Blog</span>
			</div>
		</div>
	`;

	return html;
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
		var data_content = $("#txt_content").val();
		//var data_content = exampleContent;
		console.log(data_keyword);
		console.log(data_content);
		loadArticleContent(data_content, data_keyword);
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

// Buscar con Enter
document.getElementById('search-input').addEventListener('keypress', function (e) {
	if (e.key === 'Enter') {
		searchImages();
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