1) NEGOCIO: 
Existe una falta de acceso a servicios profesionales y oficios para personas de clase media (30 a 55 años) debido a barreras económicas. Aunque estas personas tienen sus propios servicios para ofrecer, no existe una plataforma que les permita valorar y proponer intercambios de servicios sin intermediarios monetarios.

Solución
Un evaluador web de propuestas de intercambio de servicios. El usuario ingresará qué oficio ofrece (y por cuántas horas) y qué oficio solicita a cambio (y por cuántas horas). El sistema consultará un archivo con los "valores referenciales en puntos" de cada oficio y emitirá un veredicto automático sobre si el trato es justo para ambas partes.

Alcance (POC / MVP)
Para esta prueba de concepto, el alcance se limita estrictamente a la validación de la lógica de negocio detrás del intercambio. Se simulará el entorno de la plataforma mediante un único formulario web conectado a una sola vista de Django. Las profesiones u oficios disponibles y sus valores estarán fijos en un archivo de texto plano, omitiendo por completo la persistencia de datos, perfiles de usuario o comunicación real entre personas.

Priorización MoSCoW

Must:

Lectura de profesiones u oficios y sus valores desde un archivo estático servicios.json.

Una única Vista (View) en Django que reciba los datos por método POST.

Lógica matemática con if/elif para evaluar si el trueque es justo.

Una sola plantilla HTML que muestre el formulario y el resultado del cálculo.

Should:

Validación básica en la vista de Django para evitar que se ingresen horas negativas o valores nulos.

Could:

Estilos visuales básicos usando Bootstrap mediante CDN para que el formulario y el resultado (ej. verde para aceptado, rojo para rechazado) se vean presentables.

Won't:

Base de datos relacional (SQL/SQLite).

Sistema de registro o Login de usuarios.

Consumo o creación de APIs.

2) TÉCNICO: Datos de entrada, Reglas y Pantalla
Para resolver el problema sin base de datos, el proyecto contará con un archivo llamado servicios.json en la carpeta del proyecto. Este archivo contendrá un diccionario donde la llave es el nombre del servicio y el valor son los "puntos base por hora" (ej. {"gasfiteria": 20, "asesoria_legal": 35, "clases_ingles": 15, "programacion": 30}).

Datos de Entrada (Enviados desde el formulario HTML a la vista Django):

servicio_ofrecido: Tipo String (El oficio que el usuario va a entregar).

horas_ofrecidas: Tipo Integer (Cantidad de horas de trabajo que ofrece).

servicio_solicitado: Tipo String (El oficio que el usuario quiere recibir).

horas_solicitadas: Tipo Integer (Cantidad de horas del servicio que espera a cambio).

Regla de Decisión (Lógica con variables e if/elif):
En la vista de Django, se declararán variables para calcular el valor total de cada lado:
valor_ofrecido = horas_ofrecidas * json[servicio_ofrecido]
valor_solicitado = horas_solicitadas * json[servicio_solicitado]
diferencia = valor_ofrecido - valor_solicitado

Utilizando if/elif, el sistema evaluará la variable diferencia y devolverá 1 de 4 posibles resultados a la plantilla HTML:

Si (if diferencia == 0): "Intercambio Perfecto"

Los puntos de ambos servicios equivalen exactamente a lo mismo. La propuesta es 100% equitativa.

Si (elif diferencia > 0): "Intercambio Favorable para el Receptor"

El usuario está ofreciendo más valor del que está pidiendo a cambio. El sistema advierte que el usuario saldrá perdiendo un poco, pero aprueba el trueque.

Si (elif diferencia < 0 and diferencia >= -(valor_solicitado * 0.20)): "Requiere Ajuste Menor"

El usuario está pidiendo más de lo que ofrece, pero la diferencia negativa no supera el 20%. El sistema sugiere que agregue un par de horas a su oferta para igualar la balanza.

Si no (else): "Intercambio Desproporcionado (Rechazado)"

La diferencia negativa supera el 20%. Lo que el usuario pide es excesivamente más caro que lo que ofrece a cambio. Se le pide replantear la oferta por completo.

Qué mostraría la única pantalla web:
Al ingresar a la URL, la pantalla mostrará una interfaz dividida:

Arriba (Formulario): Un título "Simulador de Intercambio", dos listas desplegables (cargadas leyendo las llaves del archivo JSON) para seleccionar los servicios, y dos campos de texto numéricos para ingresar las horas. Un botón que diga "Evaluar Propuesta".

Abajo (Resultado): Al hacer clic y recargar la misma página por POST, aparecerá un bloque de texto que diga, por ejemplo: "Tus 4 hrs de Programación valen 120 pts. Estás pidiendo 2 hrs de Asesoría Legal (70 pts). Resultado: Intercambio Favorable para el Receptor."

Última actualización: 2026-08-18 (actualizado para push).