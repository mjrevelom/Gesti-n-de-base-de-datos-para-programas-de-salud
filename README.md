Hola! Este es un sistema de gestion de información para proyectos de salud pública, consiste en el manejo de una base de datos (principalmente desde un archivo json) sobre proyectos terapéuticos (musicoterapia y arte terapia) implementados en tres instituciones prestadoras de salud. Como ejemplo se emplea una base de datos sobre beneficiarios (género, edad, enfermedad/padecimiento, tratamiento y respuesta al tratamiento), clasificados en tres grupos (pacientes y sus cuidadores, trabajadores de salud y particulares. Diseño este sistema como parte de mi certificación en Programación con Python del Ministerio de Tecnologías de la Información y las Comunicaciones - Universidad Tecnológica de Pereira UTPFACEIT en el programa gubernamental Talento Tech.

Funcionalidades clave del sistema:
1. Registro y gestión de proyectos, instituciones y beneficiarios
2. Clasificación automática de beneficiarios por tipo
3. Búsqueda y filtrado
4. Generación de datos para reportes estadísticos
5. Exportación de datos
   
WBS / desglose de tareas:
Elementos necesarios para el sistema:
1. Herencias: Clase base Proyecto con subclases ProyectoMusicoterapia y ProyectoArteterapia
2. Encapsulación: Atributos info privada con getters/setters
3. Polimorfismo: Métodos sobrescritos para diferentes tipos de proyectos
4. Composición: Proyectos contienen instituciones, instituciones contienen beneficiarios
   
Procesos necesarios para el sistema:
1. Análisis y Diseño de Clases
2. Identificación de entidades principales (Proyecto, Institución, Beneficiarios)
3. Definir herencia con clase
4. Establecer enums para tipos de datos categóricos
5. Definir las clases principales que representarán los datos y procesos relevantes en el sistema de salud a desarrollar.
   
2. Atributos:
A. Para cada clase, identificar los atributos que almacenarán la información relevante
i.e. rol, edad, género, enfermedad y/o sintomatología.

4. Herencias:
A. Subclases especializadas: ProyectoMusicoterapia y ProyectoArteterapia
B. Métodos

5. Definir objetos
A. Proyectos contienen instituciones
B. Instituciones contienen beneficiarios

6. 2da revision a métodos:
A. Para cada clase, definir los métodos que realizarán las acciones necesarias i.e. agregar_beneficiario().

8. Establecer relaciones:
A. Cómo se relacionan las clases entre sí, qué elementos se repiten, cuales aplican a diferentes beneficiarios, por ej un tratamiento del que participa un beneficiario y una institución.

9. Implementación: Revisar código
A. Atributos privados con __
B. Properties
C. Validación setters
