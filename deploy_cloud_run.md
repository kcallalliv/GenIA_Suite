## Despliegue en Google Cloud (Cloud Run)

Esta sección describe el proceso de **construcción y despliegue** de **GenIA Suite** en Google Cloud usando **Google Cloud SDK**, **Cloud Build** y **Cloud Run**.

---

### 📦 Prerrequisitos

- Google Cloud SDK instalado  
- Proyecto configurado  
- Permisos para Cloud Build y Cloud Run  

```bash
gcloud auth login
gcloud config set project prd-claro-mktg-data-storage
```

## 🏗️ Paso 1: Construcción de la Imagen (Cloud Build)

Se construye la imagen Docker del proyecto y se publica en Google Container Registry (GCR).

```bash
gcloud builds submit . \
  --tag gcr.io/prd-claro-mktg-data-storage/content-claromarketingcloud-pe
```

**¿Qué realiza este paso?**

- Lee el Dockerfile del proyecto
- Ejecuta la build en infraestructura administrada por Google
- Genera una imagen versionada
- Publica la imagen en GCR
- Evita builds locales y garantiza reproducibilidad

## 🔄 Paso 2: Versionado y Subida de Cambios (GitHub)

Se recomienda subir los cambios al repositorio antes o después del despliegue para mantener trazabilidad.

```bash
git add .
git commit -m "Deploy: build y release a Cloud Run"
git push origin main
```

## ☁️ Paso 3: Despliegue del Servicio en Cloud Run

Se despliega la imagen construida como un servicio serverless en Cloud Run.

```bash
gcloud run deploy content-claromarketingcloud-pe \
  --image gcr.io/prd-claro-mktg-data-storage/content-claromarketingcloud-pe \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

**Parámetros utilizados**

- image: Imagen Docker publicada en GCR
- region us-central1: Región recomendada por latencia y costos
- platform managed: Infraestructura totalmente administrada
- allow-unauthenticated: Acceso público vía HTTPS

## ✅ Paso 4: Resultado del Despliegue

Al finalizar el despliegue, Google Cloud devolverá una URL pública HTTPS, por ejemplo:

**https://content-claromarketingcloud-pe-xxxxx-uc.a.run.app**

Esta URL corresponde a la aplicación GenIA Suite desplegada en producción.

## 🧩 Arquitectura de Despliegue

```text
Developer
   |
   +-- gcloud builds submit
   |        |
   |    Cloud Build
   |        |
   |  Container Registry
   |        |
   +-- Cloud Run (HTTPS)
            |
       Usuarios Finales
```

