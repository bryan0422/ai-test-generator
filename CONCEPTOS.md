# 📚 CONCEPTOS Y FUNDAMENTOS - AI Test Generator

Guía completa de conceptos, fundamentos y patrones aprendidos en este proyecto.

---

## 📑 TABLA DE CONTENIDOS

1. [Conceptos de IA y LLMs](#1-conceptos-de-ia-y-llms)
2. [Arquitectura de Sistemas AI](#2-arquitectura-de-sistemas-ai)
3. [Prompt Engineering](#3-prompt-engineering)
4. [APIs y Integración](#4-apis-y-integración)
5. [Async/Await en Python](#5-asyncawait-en-python)
6. [Validación de Código AI](#6-validación-de-código-ai)
7. [Testing con Playwright](#7-testing-con-playwright)
8. [CLI y UX](#8-cli-y-ux)
9. [Patrones de Diseño](#9-patrones-de-diseño)
10. [Mejores Prácticas](#10-mejores-prácticas)

---

## 1. CONCEPTOS DE IA Y LLMs

### 1.1 ¿Qué es un LLM?

**LLM = Large Language Model (Modelo de Lenguaje Grande)**
```
Definición:
Modelos de IA entrenados con cantidades masivas de texto
para predecir/generar texto de forma inteligente.

NO son:
❌ Bases de datos
❌ Buscadores
❌ Sistemas de reglas

SON:
✅ Predictores de texto sofisticados
✅ Basados en patrones aprendidos
✅ Probabilísticos (no determinísticos)
```

**Ejemplos de LLMs:**
- Claude (Anthropic) - Usado en este proyecto
- GPT-4 (OpenAI)
- Gemini (Google)
- LLaMA (Meta)

---

### 1.2 ¿Cómo funcionan los LLMs?
```
INPUT (Prompt) → LLM → OUTPUT (Respuesta)

Ejemplo:
INPUT: "Genera un test para login"
LLM: [Procesa basado en patrones aprendidos]
OUTPUT: [Código Python de test]
```

**Proceso interno (simplificado):**
```
1. Tokenización
   "Genera test" → [Token1, Token2]

2. Embedding
   Tokens → Vectores numéricos

3. Transformers
   Procesa relaciones entre tokens

4. Predicción
   ¿Cuál es el siguiente token más probable?

5. Decodificación
   Tokens → Texto legible
```

---

### 1.3 Características clave de LLMs

**Fortalezas:**
```
✅ Generación de código
✅ Comprensión de contexto
✅ Razonamiento básico
✅ Múltiples idiomas
✅ Creatividad
```

**Debilidades:**
```
❌ No son determinísticos (misma entrada ≠ misma salida)
❌ Pueden "alucinar" (inventar información)
❌ No tienen memoria entre llamadas
❌ Pueden ser verbosos o generar de más
❌ Sesgo de entrenamiento
```

---

### 1.4 Tokens y Costos

**¿Qué es un token?**
```
Token ≈ 4 caracteres en inglés
Token ≈ 1 palabra común

Ejemplos:
"Hello" = 1 token
"Playwright" = 1 token
"async def test_example():" = ~5 tokens
```

**Costos (Claude Sonnet 4):**
```
Input:  $3 por millón de tokens
Output: $15 por millón de tokens

Ejemplo:
User story (100 tokens) = $0.0003
Test generado (500 tokens) = $0.0075
Total: ~$0.008 por test
```

**Optimización:**
- ✅ Prompts concisos
- ✅ Cachear respuestas comunes
- ✅ Usar modelos más baratos para tareas simples

---

## 2. ARQUITECTURA DE SISTEMAS AI

### 2.1 Patrón General
```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       ↓
┌─────────────────────────────────┐
│   Interface (CLI, Web, etc.)    │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   Prompt Templates              │
│   (Instrucciones estructuradas) │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   AI Generator                  │
│   (Lógica de llamadas)          │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   LLM API (Claude, GPT, etc.)   │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   Validator                     │
│   (Verifica calidad)            │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   Output (Tests generados)      │
└─────────────────────────────────┘
```

**Este patrón se repite en miles de aplicaciones AI.**

---

### 2.2 Separación de Responsabilidades
```python
# ❌ MAL: Todo mezclado
def generate_test(user_story):
    prompt = "Generate test for " + user_story  # Prompt hardcoded
    response = api_call(prompt)  # Lógica mezclada
    return response  # Sin validación

# ✅ BIEN: Separado
# prompts.py - Solo templates
PROMPT = "..."

# ai_generator.py - Solo lógica
def generate_test(user_story):
    prompt = get_prompt(user_story)
    response = call_api(prompt)
    validation = validate(response)
    return response

# validators.py - Solo validación
def validate(code):
    # Validación
```

**Ventajas:**
- ✅ Fácil de mantener
- ✅ Fácil de probar
- ✅ Reutilizable
- ✅ Escalable

---

### 2.3 Flujo de 2 Pasos

**¿Por qué 2 pasos (Gherkin → Code)?**
```
OPCIÓN 1: User Story → Code directo
❌ Difícil de revisar
❌ Menos control
❌ Errores más frecuentes

OPCIÓN 2: User Story → Gherkin → Code
✅ Puedes revisar Gherkin antes
✅ Separación de QUÉ y CÓMO
✅ Mejor calidad
✅ Más flexible
```

**Analogía:**
```
Construcción de casa:

Método 1: Cliente → Constructor directo
❌ Sin planos
❌ Errores costosos

Método 2: Cliente → Arquitecto → Planos → Constructor
✅ Revisas planos primero
✅ Cambios baratos
✅ Mejor resultado
```

---

## 3. PROMPT ENGINEERING

### 3.1 ¿Qué es Prompt Engineering?
```
Definición:
El arte y ciencia de escribir instrucciones (prompts)
efectivas para que LLMs generen el output deseado.

NO es:
❌ Solo pedirle cosas al AI
❌ Magia o adivinanza

SÍ es:
✅ Proceso iterativo
✅ Basado en experimentación
✅ Requiere entender cómo piensan los LLMs
✅ Disciplina emergente con mejores prácticas
```

---

### 3.2 Anatomía de un Prompt Efectivo
```
1. ROL/CONTEXTO
   "You are an expert QA Engineer..."
   ↓ Define identidad y expertise

2. TAREA
   "Generate Playwright test code..."
   ↓ Qué debe hacer

3. INPUT
   "Given this user story: {story}"
   ↓ Datos a procesar

4. RESTRICCIONES
   "MUST include fixtures"
   "FORBIDDEN: Page Object Model"
   ↓ Límites claros

5. FORMATO
   "Output ONLY Python code"
   ↓ Estructura esperada

6. EJEMPLOS (opcional)
   "Good example: ..."
   "Bad example: ..."
   ↓ Clarifica expectativas
```

---

### 3.3 Patrones de Prompts

**Pattern 1: Few-Shot Learning**
```python
prompt = """
Generate a greeting.

Examples:
Input: "morning"
Output: "Good morning!"

Input: "evening"
Output: "Good evening!"

Now do:
Input: "afternoon"
Output: 
"""
# LLM aprende del patrón
```

**Pattern 2: Chain of Thought**
```python
prompt = """
Solve this step by step:
User story: {story}

Step 1: Identify main action
Step 2: Identify expected result
Step 3: Generate test steps
Step 4: Write code
"""
# LLM razona paso a paso
```

**Pattern 3: Constraining**
```python
prompt = """
Requirements:
1. MUST have X
2. MUST NOT have Y
3. Maximum 20 lines
4. Use only basic assertions

CRITICAL: Follow ALL requirements.
"""
# Límites claros
```

---

### 3.4 Iteración de Prompts
```
Proceso típico:

Iteración 1: Prompt básico
└─ Output: 150 líneas, complejo ❌

Iteración 2: Agregar "keep it simple"
└─ Output: 100 líneas, aún complejo ❌

Iteración 3: Agregar restricciones específicas
└─ Output: 80 líneas, mejor pero... ❌

Iteración 4: Agregar ejemplo + FORBIDDEN list
└─ Output: 30 líneas, perfecto ✅
```

**Lecciones:**
- ✅ Los LLMs necesitan ser MUY específicos
- ✅ "Simple" no es suficiente - define QUÉ es simple
- ✅ Ejemplos > Descripciones
- ✅ Restricciones negativas ("DON'T") son importantes

---

### 3.5 Prompts en este Proyecto

**SYSTEM_PROMPT:**
```python
# Define ROL
"You are an expert QA Engineer..."

# Define EXPERTISE
"Your expertise includes: ..."

# Define PRIORIDADES
"Always prioritize: ..."
```

**GHERKIN_PROMPT:**
```python
# TAREA clara
"Generate a SINGLE, SIMPLE Gherkin scenario"

# RESTRICCIONES
"ONLY ONE scenario"
"NO edge cases"

# EJEMPLO
"GOOD example: ..."
```

**PLAYWRIGHT_PROMPT:**
```python
# ESTRUCTURA obligatoria
"You MUST include these fixtures: ..."

# PROHIBICIONES
"FORBIDDEN: Page Object Model"

# FORMATO
"Output ONLY Python code"
```

---

## 4. APIS Y INTEGRACIÓN

### 4.1 ¿Qué es una API?
```
API = Application Programming Interface

Definición simple:
Una forma de que tu programa hable con otro programa.

Analogía:
API = Menú de restaurante
- Lista de opciones disponibles
- Cómo pedirlas
- Qué esperar
```

---

### 4.2 Claude API - Estructura

**Endpoint:**
```
POST https://api.anthropic.com/v1/messages
```

**Request (lo que envías):**
```python
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4000,
  "system": "You are an expert...",  # ← ROL
  "messages": [
    {
      "role": "user",                # ← Quién habla
      "content": "Generate a test..."  # ← Qué dice
    }
  ]
}
```

**Response (lo que recibes):**
```python
{
  "content": [
    {
      "type": "text",
      "text": "import pytest\n..."  # ← Código generado
    }
  ],
  "usage": {
    "input_tokens": 150,
    "output_tokens": 500
  }
}
```

---

### 4.3 Roles en Mensajes
```python
# SYSTEM (opcional, pero recomendado)
system = "You are an expert..."
# Define comportamiento global

# USER
{"role": "user", "content": "Do X"}
# Lo que el humano dice

# ASSISTANT
{"role": "assistant", "content": "Sure, here's X"}
# Lo que Claude responde

# Conversación multi-turn:
messages = [
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi! How can I help?"},
  {"role": "user", "content": "Generate a test"}
]
```

**Reglas:**
- ✅ Debe empezar con "user"
- ✅ Debe alternar: user → assistant → user → assistant
- ❌ No puede tener dos "user" seguidos

---

### 4.4 Manejo de Errores
```python
try:
    response = client.messages.create(...)
except APIError as e:
    # Error de la API (rate limit, etc.)
    print(f"API Error: {e}")
except AuthenticationError as e:
    # API key inválida
    print(f"Auth Error: {e}")
except Exception as e:
    # Cualquier otro error
    print(f"Unexpected Error: {e}")
```

**Errores comunes:**
```
401: API key inválida o faltante
429: Rate limit excedido (demasiadas llamadas)
500: Error del servidor de Anthropic
Timeout: La llamada tardó demasiado
```

---

### 4.5 Optimización de Llamadas

**Estrategias:**
```python
# 1. Cachear resultados comunes
cache = {}
if user_story in cache:
    return cache[user_story]
else:
    result = call_api(user_story)
    cache[user_story] = result
    return result

# 2. Batch processing
user_stories = [story1, story2, story3]
# Mejor: Enviar todas juntas (si API lo soporta)

# 3. Usar modelos más baratos para tareas simples
if task == "simple":
    model = "claude-haiku"  # Más barato
else:
    model = "claude-sonnet"  # Más potente
```

---

## 5. ASYNC/AWAIT EN PYTHON

### 5.1 ¿Qué es Async/Await?
```
Programación ASÍNCRONA:
Permite que tu programa haga otras cosas
mientras espera operaciones lentas (I/O).

NO significa:
❌ Ejecutar cosas en paralelo (eso es threading)
❌ Hacer todo más rápido automáticamente

SÍ significa:
✅ No bloquear el programa mientras esperas
✅ Mejor uso de recursos
✅ Múltiples operaciones I/O concurrentes
```

---

### 5.2 Sync vs Async

**SYNC (Síncrono):**
```python
def hacer_cosas():
    resultado1 = operacion_lenta_1()  # Espera 5 seg
    resultado2 = operacion_lenta_2()  # Espera 5 seg
    resultado3 = operacion_lenta_3()  # Espera 5 seg
    return resultado1, resultado2, resultado3

# Tiempo total: 15 segundos (secuencial)
```

**ASYNC (Asíncrono):**
```python
async def hacer_cosas():
    resultado1 = await operacion_lenta_1()  # Espera pero no bloquea
    resultado2 = await operacion_lenta_2()  # Espera pero no bloquea
    resultado3 = await operacion_lenta_3()  # Espera pero no bloquea
    return resultado1, resultado2, resultado3

# Tiempo dentro de función: 15 seg (secuencial)
# Pero otras funciones pueden correr en paralelo
```

---

### 5.3 Reglas de Async/Await

**1. async def → Función asíncrona**
```python
# Función normal
def suma(a, b):
    return a + b

# Función asíncrona
async def suma_async(a, b):
    return a + b
```

**2. await → Esperar operación asíncrona**
```python
async def ejemplo():
    # Operaciones de I/O (red, disco, etc.)
    await page.goto("...")        # ✅ Espera
    await page.click("...")       # ✅ Espera
    
    # Operaciones normales (CPU)
    x = 5 + 5                     # Sin await
    assert x == 10                # Sin await
```

**3. Solo puedes usar await dentro de async def**
```python
# ❌ ERROR
def funcion_normal():
    await page.goto("...")  # Error!

# ✅ CORRECTO
async def funcion_async():
    await page.goto("...")  # OK
```

---

### 5.4 ¿Cuándo usar await?
```python
# Regla simple:
# await = Operaciones que esperan algo EXTERNO

✅ await page.goto(...)       # Espera red
✅ await page.click(...)      # Espera interacción
✅ await page.screenshot(...) # Espera I/O disco
✅ await asyncio.sleep(1)     # Espera tiempo

❌ x = 5 + 5                  # Cálculo instantáneo
❌ name = "test".upper()      # Operación inmediata
❌ assert x == y              # Comparación inmediata
```

---

### 5.5 Dentro vs Entre Tests

**IMPORTANTE: Entender la diferencia**
```python
# DENTRO de un test: SECUENCIAL
async def test_ejemplo(page):
    await page.goto("...")    # Paso 1
    await page.click("...")   # Paso 2 (después de 1)
    title = await page.title() # Paso 3 (después de 2)
    assert "X" in title       # Paso 4 (después de 3)
    
# Esto es SECUENCIAL, en orden

# ENTRE tests: PARALELO (con pytest-xdist)
# test_1 y test_2 pueden correr al mismo tiempo
async def test_1(page):
    await page.goto("site1.com")
    
async def test_2(page):
    await page.goto("site2.com")
```

---

### 5.6 Analogía Visual
```
RESTAURANTE (Async)

Mesero (Thread único):
1. Toma orden Cliente 1 → Cocina
   ↓ (No se queda esperando)
2. Toma orden Cliente 2 → Cocina
   ↓ (No se queda esperando)
3. Toma orden Cliente 3 → Cocina
   ↓
4. Orden 1 lista → Sirve Cliente 1
5. Orden 2 lista → Sirve Cliente 2
6. Orden 3 lista → Sirve Cliente 3

Tiempo eficiente: Mesero nunca inactivo

SYNC (Bloqueante):
1. Toma orden Cliente 1 → Cocina
   ↓ (SE QUEDA PARADO ESPERANDO)
2. Orden lista → Sirve
3. AHORA SÍ atiende Cliente 2

Tiempo ineficiente: Mesero inactivo mientras cocina prepara
```

---

## 6. VALIDACIÓN DE CÓDIGO AI

### 6.1 ¿Por qué validar?
```
LLMs NO son perfectos:

Problemas comunes:
❌ Sintaxis incorrecta
❌ Imports faltantes
❌ Fixtures ausentes
❌ async/await mal usado
❌ Código innecesariamente complejo
❌ Selectores frágiles
❌ Assertions débiles
```

**Sin validación:**
```
Usuario: "Genera test"
AI: [Genera código con errores]
Usuario: [Ejecuta]
Test: ❌ FALLA
Usuario: "¿Por qué no funciona?"
```

**Con validación:**
```
Usuario: "Genera test"
AI: [Genera código]
Validator: "⚠️ Faltan imports, fixtures incorrectas"
Sistema: [Puede reintentar o avisar usuario]
Usuario: "Ok, arreglo esto"
```

---

### 6.2 Tipos de Validación

**1. Validación de Sintaxis**
```python
import ast

try:
    ast.parse(code)  # Intenta parsear como Python
    # Si no lanza error = sintaxis válida
except SyntaxError:
    # Sintaxis inválida
```

**2. Validación de Imports**
```python
required = ["pytest", "playwright"]
for lib in required:
    if lib not in code:
        error("Falta import: " + lib)
```

**3. Validación de Fixtures**
```python
if "@pytest.fixture" not in code:
    error("Faltan fixtures")

if "async def browser" not in code:
    error("Falta fixture 'browser'")
```

**4. Validación de Async/Await**
```python
# Buscar funciones async sin decorador
if "async def test_" in code:
    if "@pytest.mark.asyncio" not in code:
        warning("Falta @pytest.mark.asyncio")

# Buscar uso de await
if "page.goto(" in code:
    if "await page.goto(" not in code:
        error("Falta 'await' en page.goto()")
```

**5. Validación de Complejidad**
```python
lines = len(code.split('\n'))
tests = code.count("async def test_")

if tests > 3:
    warning("Demasiados tests, simplifica")

if lines > tests * 30:
    warning("Código muy largo para cantidad de tests")
```

---

### 6.3 Niveles de Severidad
```python
@dataclass
class ValidationResult:
    errors: List[str]      # 🔴 CRÍTICO - debe arreglarse
    warnings: List[str]    # ⚠️  IMPORTANTE - debería arreglarse
    suggestions: List[str] # 💡 OPCIONAL - mejoras recomendadas

# Ejemplo:
result = ValidationResult(
    errors=["Falta import pytest"],        # Bloquea ejecución
    warnings=["Código complejo"],          # Funciona pero mejorable
    suggestions=["Considera usar POM"]     # Idea para refactoring
)
```

---

### 6.4 Patrón Validator
```python
class CodeValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.suggestions = []
    
    def validate_syntax(self, code):
        # Valida una cosa
        if problem:
            self.errors.append("...")
    
    def validate_imports(self, code):
        # Valida otra cosa
        if problem:
            self.warnings.append("...")
    
    def validate_code(self, code):
        # Ejecuta TODAS las validaciones
        self.validate_syntax(code)
        self.validate_imports(code)
        # ... más validaciones
        
        return ValidationResult(
            errors=self.errors,
            warnings=self.warnings,
            suggestions=self.suggestions
        )
```

---

## 7. TESTING CON PLAYWRIGHT

### 7.1 ¿Qué es Playwright?
```
Playwright = Framework para automatización de navegadores

Características:
✅ Multi-navegador (Chrome, Firefox, Safari)
✅ Multi-plataforma (Windows, Mac, Linux)
✅ Auto-wait (espera elementos automáticamente)
✅ Screenshots y videos
✅ Network interception
✅ Mobile emulation
```

---

### 7.2 Sync vs Async API

**Playwright tiene 2 APIs:**
```python
# SYNC API (legacy, más simple)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    browser.close()

# ASYNC API (moderna, recomendada)
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto("https://example.com")
    await browser.close()
```

**¿Por qué Async?**
- ✅ Recomendación oficial de Playwright
- ✅ Mejor performance
- ✅ Necesario para tests en paralelo
- ✅ Skill más demandado en el mercado

---

### 7.3 Fixtures en Playwright
```python
@pytest.fixture
async def browser():
    """Fixture de navegador - se crea una vez por sesión"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser  # ← Provee el navegador
        await browser.close()  # ← Limpia después

@pytest.fixture
async def page(browser):
    """Fixture de página - se crea para cada test"""
    page = await browser.new_page()
    yield page  # ← Provee la página
    await page.close()  # ← Limpia después
```

**¿Qué hace yield?**
```python
# ANTES de yield: SETUP
# Se ejecuta antes del test

yield objeto  # ← Pausa aquí, ejecuta test

# DESPUÉS de yield: TEARDOWN
# Se ejecuta después del test
```

---

### 7.4 Operaciones Comunes
```python
# Navegación
await page.goto("https://example.com")
await page.go_back()
await page.reload()

# Interacción
await page.click("button")
await page.fill("input", "texto")
await page.press("input", "Enter")
await page.select_option("select", "valor")

# Obtener información
title = await page.title()
content = await page.content()
url = page.url

# Esperas
await page.wait_for_selector("div.loaded")
await page.wait_for_load_state("networkidle")
await page.wait_for_timeout(1000)

# Screenshots
await page.screenshot(path="screenshot.png")
await page.screenshot(path="full.png", full_page=True)

# Locators (nueva API)
element = page.locator("button")
await element.click()
is_visible = await element.is_visible()
text = await element.text_content()
```

---

### 7.5 Selectores
```python
# CSS Selector
page.locator("button.submit")
page.locator("#login-button")
page.locator("[data-testid='submit']")

# Texto
page.locator("text=Login")
page.locator("text=Login >> visible=true")

# XPath
page.locator("//button[@type='submit']")

# Combinados
page.locator("form >> button.submit")
```

**Mejores prácticas:**
- ✅ Usar data-testid cuando posible
- ✅ Preferir texto visible sobre CSS
- ❌ Evitar selectores frágiles (nth-child, etc.)

---

## 8. CLI Y UX

### 8.1 ¿Qué es un CLI?
```
CLI = Command Line Interface

Ejemplos que usas:
- git add, git commit, git push
- pip install playwright
- pytest tests/ -v
- python script.py

Ventajas:
✅ Rápido de usar
✅ Scriptable (automation)
✅ Integrable en CI/CD
✅ Profesional
```

---

### 8.2 Anatomía de un Comando CLI
```bash
python cli.py generate "user story" --file input.txt --output tests

│      │      │        │            │                 │
│      │      │        │            └─ Option (--output)
│      │      │        └─ Option (--file)
│      │      └─ Argument (obligatorio)
│      └─ Command (subcomando)
└─ Program
```

**Componentes:**
```
Program: python cli.py
Command: generate, validate, info
Arguments: Valores obligatorios
Options/Flags: Valores opcionales (--flag, -f)
```

---

### 8.3 Click Library
```python
import click

@click.group()
def cli():
    """Main command group"""
    pass

@cli.command()
@click.argument('name')
@click.option('--count', '-c', default=1)
def greet(name, count):
    """Greet someone COUNT times"""
    for _ in range(count):
        click.echo(f"Hello {name}!")

# Uso:
# python script.py greet Alice
# python script.py greet Alice --count 3
```

**Features:**
- ✅ Parsing automático de argumentos
- ✅ Validación de tipos
- ✅ Help automático (--help)
- ✅ Colores en terminal
- ✅ Progress bars
- ✅ Prompts interactivos

---

### 8.4 UX Best Practices
```python
# 1. Feedback claro
click.echo("🚀 Iniciando proceso...")
click.echo("✅ Completado exitosamente")
click.secho("❌ Error", fg='red')

# 2. Progress bars
with click.progressbar(items) as bar:
    for item in bar:
        process(item)

# 3. Confirmaciones
if click.confirm('¿Continuar?'):
    # Hacer algo

# 4. Prompts
name = click.prompt('Tu nombre')
password = click.prompt('Password', hide_input=True)

# 5. Colores semánticos
click.secho("Error", fg='red')      # Rojo para errores
click.secho("Success", fg='green')  # Verde para éxito
click.secho("Warning", fg='yellow') # Amarillo para advertencias
```

---

## 9. PATRONES DE DISEÑO

### 9.1 Separation of Concerns
```
Principio:
Cada módulo debe tener UNA responsabilidad clara.

❌ MAL:
archivo.py (1000 líneas)
- Prompts
- Lógica AI
- Validación
- CLI
- Todo mezclado

✅ BIEN:
prompts.py    → Solo templates
ai_generator.py → Solo lógica de generación
validators.py → Solo validación
cli.py        → Solo interfaz
```

---

### 9.2 DRY (Don't Repeat Yourself)
```python
# ❌ MAL: Repetición
def test_login():
    browser = launch_browser()
    page = create_page(browser)
    # ... test
    close_browser(browser)

def test_search():
    browser = launch_browser()  # Repetido
    page = create_page(browser) # Repetido
    # ... test
    close_browser(browser)      # Repetido

# ✅ BIEN: Fixtures
@pytest.fixture
def browser():
    browser = launch_browser()
    yield browser
    close_browser(browser)

def test_login(browser):  # Usa fixture
    # ... test

def test_search(browser):  # Usa fixture
    # ... test
```

---

### 9.3 Single Source of Truth
```python
# ❌ MAL: Información duplicada
# archivo1.py
API_URL = "https://api.example.com"

# archivo2.py
API_URL = "https://api.example.com"  # Duplicado!

# ✅ BIEN: Una sola fuente
# config.py
API_URL = "https://api.example.com"

# archivo1.py
from config import API_URL

# archivo2.py
from config import API_URL
```

---

### 9.4 Dependency Injection
```python
# ❌ MAL: Dependencia hardcoded
class Generator:
    def __init__(self):
        self.api_key = "hardcoded_key"  # ❌
        self.client = Anthropic(api_key=self.api_key)

# ✅ BIEN: Inyección de dependencia
class Generator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("API_KEY")  # ✅
        self.client = Anthropic(api_key=self.api_key)
```

**Ventajas:**
- ✅ Fácil de testear (mock dependencies)
- ✅ Flexible (cambiar implementación)
- ✅ Reutilizable

---

## 10. MEJORES PRÁCTICAS

### 10.1 Manejo de Errores
```python
# ❌ MAL: Errores silenciosos
try:
    result = call_api()
except:
    pass  # ¡Error ignorado!

# ✅ BIEN: Logging y manejo
import logging

try:
    result = call_api()
except APIError as e:
    logging.error(f"API Error: {e}")
    # Manejar específicamente
except Exception as e:
    logging.error(f"Unexpected: {e}")
    raise  # Re-lanzar si no sabemos manejar
```

---

### 10.2 Logging
```python
import logging

# Configuración
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Uso
logger.debug("Detalles técnicos")    # Solo en desarrollo
logger.info("Información general")   # Flujo normal
logger.warning("Advertencia")        # Potencial problema
logger.error("Error")                # Error que se maneja
logger.critical("Error crítico")     # Sistema comprometido
```

---

### 10.3 Type Hints
```python
# ❌ Sin tipos (menos claro)
def generate(story):
    return something

# ✅ Con tipos (más claro)
def generate(story: str) -> Dict[str, str]:
    return {"gherkin": "...", "code": "..."}

# Tipos comunes
from typing import List, Dict, Optional, Tuple

def process(
    items: List[str],
    config: Dict[str, Any],
    callback: Optional[Callable] = None
) -> Tuple[int, str]:
    return (42, "result")
```

**Ventajas:**
- ✅ Autodocumentación
- ✅ IDE autocomplete
- ✅ Detección temprana de errores
- ✅ Más fácil de mantener

---

### 10.4 Docstrings
```python
def generate_test(user_story: str) -> Dict[str, str]:
    """
    Genera un test de Playwright desde una user story.
    
    Args:
        user_story: La user story en formato texto
        
    Returns:
        Diccionario con:
        - 'gherkin': Escenarios Gherkin generados
        - 'code': Código Playwright generado
        
    Raises:
        ValueError: Si la user story está vacía
        APIError: Si hay error en llamada a Claude
        
    Example:
        >>> story = "As a user I want to login"
        >>> result = generate_test(story)
        >>> print(result['code'])
    """
    # Implementación...
```

---

### 10.5 Testing del Código
```python
# test_validators.py
def test_validator_detects_missing_imports():
    code = """
    async def test_example():
        pass
    """
    
    validator = CodeValidator()
    result = validator.validate_code(code)
    
    assert not result.is_valid
    assert "pytest" in str(result.errors)
    assert "playwright" in str(result.errors)

# test_generator.py
def test_generator_creates_valid_code():
    generator = AITestGenerator()
    story = "As a user I want to visit example.com"
    
    result = generator.generate_complete_test(story)
    
    assert result['gherkin']
    assert result['code']
    assert result['validation'].is_valid
```

---

### 10.6 Environment Variables
```python
# .env
ANTHROPIC_API_KEY=sk-ant-...
MODEL_NAME=claude-sonnet-4
MAX_TOKENS=4000

# Código
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
model = os.getenv("MODEL_NAME", "claude-sonnet-4")  # Con default
```

**Ventajas:**
- ✅ Seguridad (no commitear secrets)
- ✅ Flexibilidad (cambiar sin código)
- ✅ Diferentes configs por ambiente

---

### 10.7 Project Structure
```
proyecto/
├── src/              # Código fuente
│   ├── __init__.py
│   ├── prompts.py
│   ├── ai_generator.py
│   └── validators.py
├── tests/            # Tests generados
├── user_stories/     # User stories
├── cli.py            # CLI
├── .env              # Config (no commitear)
├── .gitignore        # Ignora archivos
├── requirements.txt  # Dependencias
├── README.md         # Documentación
└── CONCEPTOS.md      # Este archivo
```

---

## 📚 RECURSOS ADICIONALES

### Documentación Oficial
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Playwright Python Docs](https://playwright.dev/python/)
- [Pytest Docs](https://docs.pytest.org/)
- [Click Docs](https://click.palletsprojects.com/)

### Conceptos para profundizar
- Async/await: [Real Python - Async IO](https://realpython.com/async-io-python/)
- Prompt Engineering: [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- Testing Best Practices: [Playwright Best Practices](https://playwright.dev/docs/best-practices)

---

## 🎯 RESUMEN EJECUTIVO

### Lo que aprendiste:
```
1. LLMs y APIs
   - Cómo funcionan los modelos de lenguaje
   - Cómo integrar Claude API
   - Manejo de tokens y costos

2. Prompt Engineering
   - Anatomía de prompts efectivos
   - Iteración y refinamiento
   - Patrones comunes

3. Arquitectura AI
   - Separación de responsabilidades
   - Flujo de 2 pasos
   - Validación automática

4. Async/Await
   - Programación asíncrona
   - Cuándo y cómo usar await
   - Diferencia dentro vs entre tests

5. Testing
   - Playwright básico
   - Fixtures y manejo de recursos
   - Mejores prácticas

6. CLI y UX
   - Comandos profesionales
   - User experience
   - Integración con herramientas

7. Patrones y prácticas
   - Diseño de software limpio
   - Manejo de errores
   - Testing y documentación
```

### Aplicabilidad:
```
✅ Este conocimiento aplica a:
- Cualquier proyecto con LLMs
- Cualquier API de IA (OpenAI, Anthropic, etc.)
- Testing automation en general
- Arquitectura de software
- Prompt engineering para cualquier modelo
- Integración de AI en aplicaciones

❌ Estos conceptos NO son solo para este proyecto
✅ Son FUNDAMENTOS que usarás por años
```

---

**Última actualización:** Diciembre 2025  
**Autor:** Bryan R  
**Proyecto:** AI Test Generator v1.0

---