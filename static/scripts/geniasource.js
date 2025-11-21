// Obtener referencias a los elementos del DOM
const uploadButton = document.querySelector('.sys-source_upload-button');
const statusContainer = document.getElementById('upload-status-container');
const fileListContainer = document.getElementById('file-list');
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');
// Array para almacenar los archivos que el usuario ha seleccionado/arrastrado
let filesToUpload = [];
const uploaderName = "Usuario Anónimo";

function getFileIconClass(fileName) {
	const extension = fileName.split('.').pop().toLowerCase();
	switch (extension) {
		case 'pdf':
			return 'icon-pdf';
		case 'doc':
		case 'docx':
			return 'icon-word';
		case 'xls':
		case 'xlsx':
			return 'icon-excel';
		case 'ppt':
		case 'pptx':
			return 'icon-ppt';
		case 'zip':
		case 'rar':
		case '7z':
			return 'icon-zip';
		case 'jpg':
		case 'jpeg':
		case 'png':
		case 'gif':
		case 'bmp':
			return 'icon-image';
		case 'js':
			return 'icon-js';
		case 'mp4':
		case 'avi':
		case 'mov':
			return 'icon-video';
		case 'txt':
			return 'icon-txt';
		case 'svg':
			return 'icon-svg';
		case 'mp3':
		case 'wav':
		case 'ogg':
			return 'icon-audio';
		case 'apk':
			return 'icon-apk';
		case 'ai':
			return 'icon-ai';
		case 'eml':
			return 'icon-email';
		case 'psd':
			return 'icon-psd';
		case 'code':
		case 'html':
		case 'css':
			return 'icon-code';
		case 'json':
			return 'icon-json';
		case 'sql':
			return 'icon-sql';
		case 'ttf':
		case 'otf':
			return 'icon-font';
		case 'at': // Para el icono de arroba, si lo asocias a algún tipo de archivo
			return 'icon-at';
		case 'iso':
			return 'icon-iso';
		default:
			return 'icon-file-alt';
	}
}

// Función para renderizar la lista de archivos (ejemplo, puede variar)
function renderFileList() {
	fileList.innerHTML = '';
	filesToUpload.forEach((file, index) => {
		const iconClass = getFileIconClass(file.name);
		const fileItem = document.createElement('div');
		fileItem.classList.add('sys-source_file-item');
		fileItem.innerHTML = `
			<span class="sys-source_file-name ${iconClass}">${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</span>
			<button class="remove-file" data-index="${index}">&times;</button>
		`;
		fileList.appendChild(fileItem);
	});

	document.querySelectorAll('.remove-file').forEach(button => {
		button.addEventListener('click', (e) => {
			const indexToRemove = parseInt(e.target.dataset.index);
			filesToUpload.splice(indexToRemove, 1);
			renderFileList();
		});
	});
}

// Lógica de arrastrar y soltar
dropZone.addEventListener('dragover', (e) => {
	e.preventDefault();
	dropZone.classList.add('drag-over');
});
dropZone.addEventListener('dragleave', () => {
	dropZone.classList.remove('drag-over');
});
dropZone.addEventListener('drop', (e) => {
	e.preventDefault();
	dropZone.classList.remove('drag-over');
	const newFiles = Array.from(e.dataTransfer.files);
	filesToUpload.push(...newFiles);
	renderFileList();
});

// Lógica para el input de archivo
fileInput.addEventListener('change', (e) => {
	const newFiles = Array.from(e.target.files);
	filesToUpload.push(...newFiles);
	renderFileList();
});
dropZone.addEventListener('click', () => {
	fileInput.click();
});

// Función para mostrar la animación de carga
function showLoadingAnimation() {
	statusContainer.style.display = 'block';
	statusContainer.innerHTML = `
	<div class="sys-source_loading-spinner"></div>
	<p>Subiendo archivos...</p>
	`;
}

// Función para mostrar el resumen de la subida
function showUploadSummary(results) {
  const successCount = results.filter(r => r.success).length;
  const errorCount = results.length - successCount;
  const hasErrors = errorCount > 0;
  const successfulFiles = results.filter(r => r.success);
  
  statusContainer.style.display = 'block';
  statusContainer.classList.remove('success', 'error');
  statusContainer.classList.add(hasErrors ? 'error' : 'success');

  // Construye la lista de archivos exitosos
  const successListHTML = successfulFiles.length > 0 ? `
    <ul class="sys-source_success-list">
      ${successfulFiles.map(r => {
        const iconClass = getFileIconClass(r.fileName);
        return `
          <li class="sys-source_file-item">
            <span class="sys-source_file-name ${iconClass}">${r.fileName}</span>
            <i class="fas fa-check-circle"></i>
          </li>
        `;
      }).join('')}
    </ul>
  ` : '';

  statusContainer.innerHTML = `
    <h3>${hasErrors ? 'Subida con Errores' : 'Subida Exitosa'}</h3>
    <p>Archivos subidos con éxito: ${successCount}</p>
    <p>Archivos con error: ${errorCount}</p>
    
    ${successListHTML}

    ${hasErrors ? `<ul class="sys-source_error-list">
      ${results.filter(r => !r.success).map(r => `<li>${r.fileName}: ${r.error}</li>`).join('')}
    </ul>` : ''}
  `;
}

// Escuchador de eventos para el botón de subir
uploadButton.addEventListener('click', async () => {
	if (filesToUpload.length === 0) {
	// Puedes mostrar un mensaje temporal o simplemente no hacer nada
	statusContainer.style.display = 'none';
	alert('No hay archivos para subir.');
	return;
	}

	showLoadingAnimation();

	const uploadPromises = filesToUpload.map(async (file) => {
	const formData = new FormData();
	formData.append('file', file);
	formData.append('uploader', 'usuario_ejemplo');

	try {
		const response = await fetch('/genia-source/upload', {
		method: 'POST',
		body: formData,
		});

		if (!response.ok) {
		throw new Error(response.statusText);
		}

		const data = await response.text();
		return { success: true, fileName: file.name, data: data };
	} catch (error) {
		return { success: false, fileName: file.name, error: error.message };
	}
	});

	const results = await Promise.all(uploadPromises);

	filesToUpload = [];
	renderFileList();
	showUploadSummary(results);
});

// Ocultar el contenedor de estado al inicio
window.addEventListener('load', () => {
	statusContainer.style.display = 'none';
});