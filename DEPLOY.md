# Guía de Despliegue en Railway

## 📋 Pre-requisitos

- [ ] Cuenta de GitHub
- [ ] Cuenta de Railway ([railway.app](https://railway.app))
- [ ] API Key de OpenAI
- [ ] Credenciales de correo (Gmail con App Password recomendado)

## 🚀 Pasos para Desplegar

### 1. Subir Proyecto a GitHub

```bash
# Inicializar git (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit - SimplexityInvoiceAgent"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/tu-usuario/SimplexityInvoiceAgent.git

# Push
git push -u origin main
```

### 2. Conectar con Railway

#### Opción A: Interfaz Web

1. Ve a [railway.app](https://railway.app)
2. Haz clic en **"Start a New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Autoriza Railway a acceder a GitHub
5. Selecciona el repositorio **SimplexityInvoiceAgent**
6. Railway automáticamente:
   - Detectará que es un proyecto Python
   - Leerá `railway.json` para configuración
   - Instalará dependencias desde `requirements.txt`
   - Iniciará la app con gunicorn

#### Opción B: Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login en Railway
railway login

# Inicializar proyecto
railway init

# Vincular con Railway
railway link

# Deploy
railway up
```

### 3. Configurar Variables de Entorno

En el Dashboard de Railway, ve a tu proyecto:

1. Haz clic en la pestaña **"Variables"**
2. Agrega las siguientes variables:

#### Variables Requeridas:
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
MAIL_USERNAME=tu-correo@gmail.com
MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx  # App Password de Gmail
SECRET_KEY=genera-una-clave-secreta-super-aleatoria-aqui
```

#### Variables Opcionales:
```bash
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_VISION_MODEL=gpt-4-vision-preview
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
FLASK_ENV=production
```

### 4. Generar Secret Key

Para generar una SECRET_KEY segura:

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Configurar Gmail App Password

1. Ve a [Google Account Security](https://myaccount.google.com/security)
2. Habilita **"Verificación en 2 pasos"**
3. Ve a **"App Passwords"**
4. Genera una contraseña para "Mail"
5. Usa esa contraseña de 16 caracteres como `MAIL_PASSWORD`

### 6. Generar Domain Público

1. En Railway Dashboard, ve a **Settings**
2. En la sección **"Networking"** o **"Domains"**
3. Haz clic en **"Generate Domain"**
4. Railway te asignará una URL: `tu-proyecto.up.railway.app`

### 7. Verificar Deployment

1. Visita la URL generada
2. Deberías ver el **Agente de Procesamiento de Facturas**
3. Prueba la funcionalidad:
   - Define limitaciones de prueba
   - Sube una factura (PDF o imagen)
   - Ingresa tu email
   - Procesa y verifica que recibas el reporte

## 📊 Monitoreo

### Ver Logs en Tiempo Real

En Railway Dashboard:
- Pestaña **"Deployments"** → Click en el deployment activo
- Pestaña **"Logs"** → Ver logs en vivo

O con CLI:
```bash
railway logs
```

### Métricas

Railway muestra automáticamente:
- **CPU Usage**: Uso de procesador
- **Memory**: Consumo de RAM
- **Network**: Tráfico de red

## 🔧 Troubleshooting

### Error: "Application failed to respond"

**Causa**: Variables de entorno no configuradas

**Solución**:
1. Verifica que `OPENAI_API_KEY` esté configurada
2. Verifica `MAIL_USERNAME` y `MAIL_PASSWORD`
3. Agrega `PORT` variable (aunque Railway la inyecta automáticamente)

### Error: "OpenAI API Error"

**Causa**: API Key inválida o sin créditos

**Solución**:
1. Verifica tu API key en [OpenAI Platform](https://platform.openai.com/api-keys)
2. Verifica que tengas créditos disponibles
3. Verifica que el modelo esté disponible

### Error: "Email delivery failed"

**Causa**: Credenciales SMTP incorrectas

**Solución**:
1. Para Gmail, usa **App Password**, no tu contraseña normal
2. Verifica que 2FA esté habilitado
3. Verifica `MAIL_SERVER` y `MAIL_PORT`

### Error: "Build Failed"

**Causa**: Dependencias incompatibles

**Solución**:
1. Verifica que `runtime.txt` tenga versión Python válida
2. Verifica que `requirements.txt` tenga versiones compatibles
3. Chequea los build logs en Railway

## 💰 Costos

### Plan Gratuito de Railway

- **$5 USD** de crédito mensual gratis
- **500 horas** de ejecución aproximadamente
- **100 GB** de ancho de banda

### Uso Estimado

Para SimplexityInvoiceAgent:
- **Idle**: ~$0.0001/hora (muy bajo consumo)
- **Procesando**: ~$0.001/hora (depende de uso OpenAI)

### Optimización de Costos

1. **Auto-sleep**: Railway pone apps en sleep después de inactividad
2. **Monitorear uso**: Revisa el dashboard regularmente
3. **OpenAI**: El costo real estará en las llamadas a OpenAI API

## 🔄 Actualizaciones

### Deploy Automático

Railway hace deploy automático cuando haces push a GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
# Railway detecta el cambio y hace redeploy automáticamente
```

### Deploy Manual

Con Railway CLI:
```bash
railway up
```

## 🌐 Custom Domain (Opcional)

1. En Railway → Settings → Custom Domains
2. Agrega tu dominio: `facturas.tudominio.com`
3. Configura DNS en tu proveedor:
   ```
   CNAME facturas → tu-proyecto.up.railway.app
   ```

## 📝 Checklist Final

Antes de compartir tu app:

- [ ] Variables de entorno configuradas
- [ ] Domain generado y funcionando
- [ ] Prueba completa realizada
- [ ] Email de reporte recibido
- [ ] Logs revisados sin errores
- [ ] Monitoreo configurado
- [ ] README actualizado con URL de producción

## 🎉 ¡Listo!

Tu SimplexityInvoiceAgent está ahora en producción en Railway!

**URL de ejemplo**: `https://simplexityinvoiceagent.up.railway.app`

---

## Recursos Adicionales

- [Railway Docs](https://docs.railway.app/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
