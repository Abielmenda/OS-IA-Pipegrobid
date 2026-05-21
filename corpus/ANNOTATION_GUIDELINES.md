# Guía de Anotación para NER en Agradecimientos (Acknowledgements)
---

## 1. ¿Para qué sirve este documento?

Este documento define las reglas que seguimos para anotar a mano las entidades nombradas (personas, organizaciones, proyectos) que aparecen en la sección de **agradecimientos** de los papers científicos.

¿Por qué es importante? Porque esas anotaciones manuales son nuestro **Gold Standard** (`gold_standard.json`), es decir, la verdad absoluta contra la que medimos cómo de bien funciona cada modelo de NER (Reconocimiento de Entidades Nombradas). Calculamos precisión, recall y F1 comparando lo que el modelo predice contra lo que nosotros anotamos.

Dos anotadores humanos aplicaron estas reglas trabajando en sesiones de consenso. Si en el futuro alguien quiere repetir o ampliar la anotación, debe seguir estas reglas al pie de la letra para que los resultados sean comparables.

---

## 2. Las 3 categorías de entidades que anotamos

Solo anotamos **3 categorías**. Nada más. Si una entidad no encaja en ninguna, no se anota.

### 2.1. PER — Persona

Cualquier persona mencionada en los agradecimientos a la que se le agradece, reconoce o menciona por su contribución.

**Incluye:**
- Nombres completos: `Daniel Garijo`, `Emmanuel Johnson`
- Iniciales: `SS`, `CJP`, `A.-F. B.`
- Nombres que aparecen con título académico (anotamos solo el nombre, sin el título — mira la regla 3.4): de `Prof. C.Z. Zhang` anotamos `C.Z. Zhang`
- Nicks y pseudónimos online cuando se refieren a una persona: `xlr8harder`

**No incluye:**
- Pronombres ni referencias genéricas como *"our collaborators"*, *"the authors"*, *"they"*, *"the team"*
- Grupos de autores: *"the FAIR Chemistry group"* (eso es una ORG, no una lista de personas)

### 2.2. ORG — Organización

Cualquier entidad organizativa mencionada como fuente de apoyo, afiliación, financiación o colaboración.

**Incluye:**
- Universidades y centros de investigación: `UC Berkeley`, `LBNL`, `Stanford Medicine Post-Baccalaureate Experience In Research program`
- Agencias de financiación y fundaciones: `National Science Foundation`, `Simons Foundation`, `Henri Seydoux Fund`
- Programas marco de financiación: `Horizon 2020`, `FP7`, `Marie Skłodowska-Curie Actions`
- Departamentos gubernamentales y organismos supranacionales: `Department of Health -Epidemiology Bureau`, `European Union`
- Grupos de investigación, colaboraciones e iniciativas con nombre propio: `FAIR Chemistry group`, `Simons Foundation Collaboration on the Physics of Learning and Neural Computation`, `national SARS-CoV-2 biosurveillance initiative`
- Premios y programas con nombre que se tratan como entidades organizativas: `Schmidt Sciences Polymath Award`
- Empresas que donan recursos o cómputo: `Prime Intellect`

**No incluye:**
- Librerías de software, código o herramientas: `FEniCS`, `PyTorch`, `TensorFlow`
- Plataformas de hosting cuando se mencionan genéricamente: `GitHub` (como sitio de código)
- URLs y direcciones web: `www.safeandtrustedai.org`
- Países tratados solo como ubicaciones geográficas (no como entidades financiadoras)

### 2.3. PROJ — Proyecto / Grant / Ayuda

**Definición estricta:** solo códigos alfanuméricos que identifican de forma única un proyecto, grant o contrato de financiación. Un PROJ es un **código identificador**, no el nombre bonito del proyecto.

**Incluye:**
- Códigos de grant estándar: `IIS-2229876`, `R01EY022933`, `EP/S023356/1`, `851173`, `SA-AUT-2024-015b`, `26-23955S`
- Códigos con formatos mixtos: cadenas alfanuméricas con separadores (guiones, barras, puntos) que funcionen como identificadores de proyecto

**No incluye:**
- Nombres de programas marco (Horizon 2020 → ORG)
- Nombres de iniciativas o programas sin código
- Nombres de premios sin código (Schmidt Sciences Polymath Award → ORG)
- Las palabras que rodean al código: *"grant"*, *"award"*, *"contract"*, *"agreement"*, *"number"*, *"No."*, *"#"*

**¿Por qué esta definición tan estricta?** Por dos razones. Primero, porque en clase (Sesión 11, diapositiva 7) el profesor marca solo códigos alfanuméricos como Project IDs. Segundo, porque en nuestra ontología la clase `schema:Project` tiene propiedades como `schema:identifier`, `schema:startDate`, `schema:endDate` y `my:fundingAmount`, que solo tienen sentido para proyectos concretos con un identificador único, no para programas marco.

---

## 3. Reglas generales de anotación

Estas reglas aplican siempre, en cualquier caso.

### 3.1. Anotar el texto tal como aparece (literal text principle)

**Anota las entidades exactamente como aparecen en el texto.** No expandas iniciales, no infieras entidades implícitas, no normalices variantes ortográficas.

**¿Por qué?** Porque los modelos NER procesan el texto literal. Si nosotros anotamos "Anne-Florence Bitbol" donde el texto pone solo "A.-F. B.", el modelo fallará al compararse no porque no sepa reconocer entidades, sino porque no hace resolución de identidades (esa es otra tarea distinta, que va después).

| El texto dice | Anotación correcta | Anotación incorrecta |
|---|---|---|
| `A.-F. B.` | `A.-F. B.` (PER) | `Anne-Florence Bitbol` |
| `CJP` | `CJP` (PER) | `C. J. Palpal-latoc` |
| `S.G.` | `S.G.` (PER) | `Surya Ganguli` |

La resolución de entidades (enlazar `A.-F. B.` con un ORCID o un ID de Wikidata) es un paso **posterior del pipeline**, no parte de la anotación.

### 3.2. El mínimo span limpio (span cleanliness)

Anota el **trozo de texto más corto que identifique únicamente a la entidad**, sin conectores, preposiciones ni determinantes sobrantes.

| El texto dice | Anotación correcta | Anotación incorrecta |
|---|---|---|
| `the US Office of Naval Research` | `US Office of Naval Research` | `the US Office of Naval Research` |
| `grant number EP/S023356/1` | `EP/S023356/1` | `grant number EP/S023356/1` |
| `the FAIR Chemistry group` | `FAIR Chemistry group` | `the FAIR Chemistry group` |

### 3.3. Nombre completo y sigla: se anotan los dos

Cuando una entidad aparece con su nombre completo y su sigla entre paréntesis, anotamos **ambos como entidades separadas de la misma categoría**.

**Ejemplo:**

> *"the National Eye Institute (NEI)"*

Anotación:
- ORG: `National Eye Institute`
- ORG: `NEI`

> *"the European Research Council (ERC)"*

Anotación:
- ORG: `European Research Council`
- ORG: `ERC`

### 3.4. Los títulos académicos no van dentro de la persona

Los títulos académicos (`Prof.`, `Dr.`, `Professor`, `Doctor`) **NO** se incluyen en el span de PER. Los quitamos durante la anotación para que la entidad contenga solo el nombre.

**¿Por qué?** En nuestro Grafo de Conocimiento, las personas son `foaf:Person` con una propiedad `name`. Si metemos "Prof. C.Z. Zhang" como nombre, ese dato no se corresponde con el nombre canónico de la persona. Los títulos son metadatos (cargo, rol), no parte del nombre. Además, cuando después busquemos a esa persona en ORCID o Wikidata, tendríamos que quitar el título para encontrar la coincidencia.

| El texto dice | Anotación correcta | Anotación incorrecta |
|---|---|---|
| `Prof. C.Z. Zhang` | `C.Z. Zhang` (PER) | `Prof. C.Z. Zhang` |
| `Dr. Hussein Al Osman` | `Hussein Al Osman` (PER) | `Dr. Hussein Al Osman` |
| `Professor Zhang and his team` | `Zhang` (PER) | `Professor Zhang` |

**Importante:** esto es un cambio respecto a la versión 1.1, donde los títulos pegados al nombre sí se incluían. Puedes ver la justificación completa en el historial de cambios (sección 8).

Los nicks y pseudónimos online (como `xlr8harder`, `Janus`) **NO** son títulos académicos, así que se anotan literalmente como aparecen (mira la sección 4.5).

### 3.5. No inventes entidades implícitas

No anotes organizaciones que solo están implícitas dentro de un nombre compuesto.

**Ejemplo:** En *"Simons Foundation Collaboration on the Physics of Learning and Neural Computation"*, anotamos solo el nombre completo de la colaboración como ORG. No anotamos "Simons Foundation" por separado a menos que aparezca independientemente en otra parte del mismo texto.

### 3.6. Pronombres y referencias genéricas nunca se anotan

- *"our collaborators"* → no se anota
- *"the authors"* → no se anota
- *"the team"* → no se anota
- *"others from the X group"* → solo `X group` se anota como ORG

---

## 4. Casos especiales y decisiones importantes

Esta sección recoge las decisiones que tomamos durante las sesiones de consenso para casos complicados. Son vinculantes para cualquier anotador futuro.

### 4.1. Programas marco vs. proyectos individuales

**Decisión:** Los programas marco de financiación (Horizon 2020, FP7, Horizon Europe, Marie Skłodowska-Curie Actions, etc.) se anotan como **ORG**, no como PROJ.

**¿Por qué?** Estos programas son marcos administrativos bajo los que se financian miles de proyectos individuales. El proyecto concreto que financia un paper se identifica por su código de grant (ej. `851173`), y ese código es lo que va a PROJ.

**Ejemplo (paper_13):**

> *"This research was partly funded by the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No. 851173, to A.-F. B.)."*

Anotación:
- PER: `A.-F. B.`
- ORG: `European Research Council`, `ERC`, `European Union`, `Horizon 2020`
- PROJ: `851173`

### 4.2. Premios con nombre pero sin código

**Decisión:** Los premios que tienen un nombre propio pero no un código alfanumérico se anotan como **ORG**, no como PROJ.

**¿Por qué?** Sin un identificador único, un premio no encaja en nuestra clase `schema:Project` (que necesita `schema:identifier`). El premio se modela como una entidad de reconocimiento/financiación, que es ORG.

**Ejemplo (paper_27):**

> *"a Schmidt Sciences Polymath Award"*

Anotación:
- ORG: `Schmidt Sciences Polymath Award`

### 4.3. Software, librerías y herramientas

**Decisión:** El software **no se anota**, en ninguna categoría.

**¿Por qué?** El software está fuera del alcance de nuestras 3 categorías. En el grafo de conocimiento podría modelarse como `schema:SoftwareApplication`, pero esa no es parte de la tarea de NER que estamos evaluando.

**Ejemplos:**
- `FEniCS` → no se anota
- `PyTorch` → no se anota
- `GitHub` (como plataforma de código) → no se anota

### 4.4. URLs y direcciones web

**Decisión:** Las URLs **no se anotan**, en ninguna categoría.

**Ejemplo (paper_09):** `www.safeandtrustedai.org` → no se anota.

### 4.5. Nicks y pseudónimos de autores

**Decisión:** Los nicks online y pseudónimos que se usan para referirse a contribuidores individuales se anotan como **PER**.

**Ejemplo (paper_07):** `xlr8harder`, `Janus` → ambos se anotan como PER.

### 4.6. Departamentos y organismos gubernamentales

**Decisión:** Los departamentos gubernamentales y sus divisiones internas se anotan como **ORG**, incluyendo las subdivisiones cuando se mencionan juntas.

**Ejemplo (paper_19):**

> *"the Department of Health -Epidemiology Bureau"*

Anotación:
- ORG: `Department of Health -Epidemiology Bureau` (se anota exactamente como aparece, incluso con espacios raros alrededor del guión)

### 4.7. Afiliaciones de las personas agradecidas

Cuando el texto dice *"X from University Y"*, se anotan tanto X (como PER) como University Y (como ORG).

**Ejemplo (paper_28):**

> *"We thank Tobias Kreiman, Sam Blau, ... from UC Berkeley / LBNL"*

Anotación:
- PER: `Tobias Kreiman`, `Sam Blau`, ...
- ORG: `UC Berkeley`, `LBNL`

---

## 5. Lo que NO anotamos (y por qué)

Estas categorías las **excluimos a propósito** de nuestro gold standard:

- **LOC / País**: No anotamos ubicaciones geográficas. La información de país y ciudad de las organizaciones se enriquece después mediante Wikidata y otras fuentes externas, no se extrae del texto de agradecimientos.
- **Software / Herramientas**: Excluido, como explicamos en la sección 4.3.
- **Fecha / Hora**: No es relevante para identificar entidades financiadoras.
- **Dinero / Cantidades**: Los valores monetarios que aparecen no se anotan. En la ontología existe `my:fundingAmount` para modelar cantidades, pero se rellena desde fuentes externas, no desde la salida del NER.

---

## 6. Cómo se hizo la anotación

El proceso fue el siguiente:

1. Un parser en Python extrae el texto de los agradecimientos de cada paper a partir de los XML TEI que genera GROBID. Ese texto en plano se guarda en el campo `text` de cada entrada del `gold_standard.json`.
2. Dos anotadores leen de forma independiente cada agradecimiento e identifican las entidades siguiendo estas guías.
3. Las discrepancias se resuelven en una sesión de consenso con al menos tres miembros del grupo presentes.
4. La anotación final acordada se registra en `gold_standard.json`.

---

## 7. Cómo se usa esto para evaluar modelos NER

El gold standard se usa para calcular precisión, recall y F1 por categoría (PER, ORG, PROJ) para cada modelo de NER candidato. Los modelos se comparan contra las **anotaciones literales**: la predicción del modelo debe coincidir exactamente con la cadena de texto del gold standard para contar como acierto (true positive).

El corpus actual contiene **8 documentos** con estructuras de agradecimiento variadas: desde frases cortas con un único financiador, hasta párrafos densos con múltiples personas, organizaciones, programas y códigos de proyecto.

---

## 8. Historial de cambios

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | Mayo 2026 | Anotación inicial, con interpretación mixta de PROJ |
| 1.1 | Mayo 2026 | Definición estricta de PROJ (solo códigos alfanuméricos). Programas marco pasan a ORG. Se formaliza el principio de texto literal. |
| 1.2 | Mayo 2026 | Los títulos académicos (`Prof.`, `Dr.`, `Professor`) se excluyen de los spans PER (sección 3.4). Entidad afectada: `paper_11` PER `Prof. C.Z. Zhang` → `C.Z. Zhang`. Motivación: en el grafo de conocimiento, una propiedad `foaf:Person.name` no debe contener el título, y la resolución downstream (ORCID, Wikidata) también lo quitaría antes de buscar. |
