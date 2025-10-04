# Guía de Seguridad

## 🔐 Información Sensible

### ⚠️ NUNCA Compartas en Público

**NUNCA compartas o expongas:**
- ❌ API Keys de OpenAI
- ❌ Contraseñas de email
- ❌ SECRET_KEY de Flask
- ❌ Archivo `.env`
- ❌ Credenciales de cualquier tipo

### 🚨 Si Expusiste una API Key Accidentalmente

**ACCIÓN INMEDIATA:**

1. **OpenAI API Key**
   - Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
   - Encuentra la key expuesta
   - Haz clic en "Revoke" o el icono de basura
   - Genera una nueva API key
   - Actualiza tu `.env` local
   - Actualiza las variables en Railway

2. **Gmail Password**
   - Ve a [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Revoca la contraseña expuesta
   - Genera una nueva App Password
   - Actualiza tu `.env` y Railway

3. **SECRET_KEY de Flask**
   - Genera una nueva:
     ```bash
     python -c "import secrets; print(secrets.token_hex(32))"
     ```
   - Actualiza en `.env` y Railway

## 🛡️ Mejores Prácticas

### 1. Archivo `.env`

✅ **HACER:**
```bash
# En .gitignore
.env
```

❌ **NO HACER:**
```bash
# Nunca hacer commit de .env
git add .env  # ❌ NUNCA
```

### 2. Variables de Entorno

✅ **HACER:**
```python
# Usar variables de entorno
api_key = os.getenv('OPENAI_API_KEY')
```

❌ **NO HACER:**
```python
# Hardcodear credenciales
api_key = "sk-proj-xxxxx"  # ❌ NUNCA
```

### 3. Railway Variables

✅ **Configurar en Dashboard:**
- Variables → Add Variable
- Nunca en el código

### 4. Compartir Código

✅ **Antes de compartir:**
- Verifica que `.env` NO esté incluido
- Verifica que no haya credenciales hardcodeadas
- Usa `.env.example` con valores placeholder

## 📋 Checklist de Seguridad

Antes de hacer deploy o compartir código:

- [ ] `.env` está en `.gitignore`
- [ ] No hay API keys en el código
- [ ] `.env.example` solo tiene placeholders
- [ ] Variables configuradas en Railway
- [ ] No hay contraseñas en commits
- [ ] SECRET_KEY es aleatoria y segura

## 🔍 Verificar Seguridad

```bash
# Verificar que .env no esté trackeado
git status

# Buscar posibles keys expuestas
grep -r "sk-proj-" .
grep -r "sk-" . --exclude-dir=.git --exclude=".env"

# Verificar .gitignore
cat .gitignore | grep .env
```

## 🚀 Deployment Seguro

### Railway

1. **Variables de Entorno**
   - Configurar en Dashboard (no en código)
   - Una por una manualmente
   - Nunca en archivos de configuración

2. **Logs**
   - No logguear credenciales
   - No imprimir variables sensibles
   - Usar niveles de log apropiados

## 📞 ¿Qué Hacer Si...?

### Mi API Key fue expuesta en GitHub

1. **Revoca inmediatamente** en OpenAI
2. Genera nueva key
3. Actualiza `.env` local y Railway
4. Considera hacer un force push para remover del historial:
   ```bash
   # ⚠️ Solo si es absolutamente necesario
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

### Commit accidental de `.env`

1. **Revoca todas las credenciales** en ese archivo
2. Remueve del historial:
   ```bash
   git rm .env
   git commit --amend
   git push --force
   ```
3. Regenera todas las credenciales
4. Verifica que `.env` esté en `.gitignore`

## 🔒 Generación de Claves Seguras

### SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Password Aleatorio

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📚 Recursos

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Railway Security](https://docs.railway.app/guides/optimize-usage)

---

**Recuerda**: La seguridad es responsabilidad de todos. Mantén tus credenciales seguras siempre.
