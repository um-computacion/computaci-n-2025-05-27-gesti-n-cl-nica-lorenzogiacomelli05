## Como ejecutar el sistema

Para iniciar el sistema desde la consola
Ejecutar el siguiente comando

python -m clicClinica.cliClinica
Se mostrara un menu con las siguientes opciones

1 Agregar Paciente  
2 Agregar Medico  
3 Agendar Turno  
4 Agregar Especialidad  
5 Emitir Receta  
6 Ver Historia Clinica  
7 Ver todos los Turnos  
8 Ver todos los Pacientes  
9 Ver todos los Medicos  
0 Salir 

## Como ejecutar las pruebas

Para ejecutar todos los tests del sistema

python -m unittest discover test

Para ejecutar una prueba especifica

python -m unittest test.test_clases-> clases
python -m unittest test.testexepcion-> expeciones

## Diseño general del sistema

El sistema esta implementado utilizando programacion orientada a objetos y se compone de las siguientes clases

- Paciente guarda los datos personales de cada paciente  
- Medico contiene los datos del medico y sus especialidades  
- Especialidad representa las especialidades medicas y los dias disponibles  
- Turno administra los turnos agendados entre pacientes y medicos  
- Receta guarda los medicamentos indicados por los medicos  
- HistoriaClinica reune los turnos y recetas de cada paciente  
- Clinica clase principal que gestiona pacientes medicos turnos especialidades y recetas  

## Manejo de errores

Se implementaron excepciones personalizadas para controlar

- Ingreso de datos duplicados  
- Turnos asignados en horarios ocupados  
- Validaciones de datos ingresados  
