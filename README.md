# Prueba Técnica – Evaluación de Audios con AI (Python + FastAPI)

## Objetivo

El objetivo de esta prueba es construir un **servicio backend en Python 3** que permita:

1. Obtener audios desde una carpeta local.
2. Transcribir dichos audios a texto.
3. Evaluar cada transcripción según una **pauta definida**, utilizando AI (prompt engineering).

La prueba busca evaluar **criterio técnico, claridad de código y uso práctico de AI**, no soluciones complejas o sobre-diseñadas.

> **Nota importante:**  
> Se entrega una **estructura inicial de proyecto incompleta** como punto de partida.  
> Esta estructura **puede y debe ser modificada libremente** si el candidato lo considera necesario para una mejor solución.

---

## Alcance y tiempo

- **Tiempo máximo estimado:** 5 horas
- Se prioriza una solución:
  - Clara
  - Funcional
  - Bien estructurada

---

## Requerimientos funcionales

### 1. Obtención de audios desde una carpeta

El sistema debe:

- Leer archivos de audio desde una carpeta local.
- Permitir:
  - Evaluar un audio específico.
  - Evaluar todos los audios de la carpeta.

**Consideraciones:**
- Validar que el archivo exista.
- Manejar errores de forma controlada (sin romper la API).

---

### 2. Transcripción de audios

Cada audio debe ser convertido a texto.

**Requerimientos:**
- Implementar un mecanismo de transcripción:
  - API externa (Whisper OpenAI).

**Resultado esperado:**
- Texto transcrito en formato `JSON`.
- Separar mensajes entre un **ejecutivo** y un **cliente**

**Ejemplo**
``` JSON
[
   {
      "role": "agent",
      "content": "Hola, buen dia, ¿Cómo se encuentra?"
   },
   {
      "role": "client",
      "content": "Muy bien, muchas gracias"
   }
   ...
]
```


---

### 3. Evaluación según pauta

Cada transcripción debe ser evaluada utilizando una **pauta definida**, mediante un modelo de lenguaje (LLM).

La evaluación debe producir un **resultado estructurado**, no texto libre.

#### Prompt engineering

El prompt debe:

- Explicar claramente la pauta de evaluación.
- Indicar explícitamente el formato de salida esperado.
- Forzar una salida estructurada (por ejemplo, JSON).

**Ejemplo de dimensiones a evaluar (referencial):**
- Claridad del mensaje.
- Cumplimiento de normas o tono esperado.
- Detección de intención relevante.

**Consideraciones:**
- No se requiere fine-tuning.
- Se valora un prompt claro, reproducible y fácil de modificar.

---

### 4. Resultados y persistencia

Cada evaluación debe generar un resultado estructurado que:

- Se retorne vía API.
- Se persista en disco (JSON, JSONL u otro formato simple).

**Contenido mínimo esperado:**
- Identificador del audio.
- Transcripción.
- Resultado de la evaluación.

---

## API (FastAPI)

### Requerimientos mínimos

El servicio debe exponer:

- Un endpoint para evaluar **un audio específico**.
- Un endpoint para evaluar **todos los audios** de la carpeta.

**Buenas prácticas esperadas:**
- Uso de FastAPI.
- Uso de Pydantic para request y response.
- Códigos HTTP adecuados.
- Manejo básico de errores.

---

## Buenas prácticas esperadas

Se evaluará positivamente que el candidato:

- Separe correctamente:
  - Capa API (routes)
  - Lógica de negocio (services)
  - Contratos de datos (schemas)
- Use schemas **solo** para request/response.
- Evite lógica de negocio dentro de los schemas.
- Use nombres claros y consistentes.
- Utilice variables de entorno para configuración.

---

## Fuera de alcance (no evaluado)

No es necesario implementar:

- Arquitectura limpia formal (DDD, Clean Architecture).
- Dependency Injection avanzada.
- Tests unitarios.
- Autenticación o seguridad avanzada.

---

## Entregable

El entregable debe incluir:

- La solución debe poder ejecutarse localmente.

### Opcional

- Incluir archivo Dockerfile.
- Generar una Base de datos en SQlite, para guardar las evaluaciones y transcripciones.
- Utilizar RAG para clasificar **motivos de no pago**.
 
---

## Criterio general de evaluación

Se evaluará principalmente:

- Claridad y calidad del código.
- Comprensión práctica de AI aplicada.
- Uso correcto de FastAPI y Pydantic.
- Buen criterio técnico dentro del tiempo limitado.

---

### Nota final

No se espera una solución “enterprise”.  
Se espera una solución **simple, correcta y bien razonada**, que demuestre tu capacidad para integrar AI en un backend Python real.
