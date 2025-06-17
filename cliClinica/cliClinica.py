import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from modeloclinica.Turnosclinica import (Paciente, Medico, Clinica, Especialidad)
from modeloclinica.excepciones import (ErrorAlAgregarMedico, ErrorAlAgregarPaciente, ErrorGeneralTurno, PacienteNoEncontradoExcepcion, MedicoNoDisponibleExcepcion, TurnoOcupadoException, ErrorPaciente, ErrorMedico, RecetaInvalidaException, EspecialidadYaExistente)
from datetime import datetime

clinica = Clinica()
def menu():

    while True:
        print("Menu Principal")
        print("1- Agregar Paciente")
        print("2- Agregar Medico")
        print("3- Agendar Turno")
        print("4- Agregar Especialidad")
        print("5- Emitir Receta")
        print("6- Ver Historia Clinica")
        print("7- Ver todos los Turnos")
        print("8- Ver todos los Pacientes")
        print("9- Ver todos los Medicos")
        print("0- Salir")

        try:
            opcion = int(input("Seleccione una opcion: "))

            if opcion == 1:

                print("Agregar Paciente")

                nombre = input("Ingrese el nombre: ")
                apellido = input("Ingrese el apellido: ")
                dni = input("Ingrese su DNI: ")
                fechaNac = input("Ingrese su fecha de nacimiento(dd/mm/aaaa)")

                paciente =Paciente(nombre, apellido, dni, fechaNac)

                clinica.agregar_paciente(paciente)

                print("Paciente Agregado Correctamente!")
            
            if opcion == 2:

                print("Agregar Medico")

                nombre = input("Ingrese el nombre: ")
                apellido = input("Ingrese el apellido: ")
                matricula = input("Ingrese el numero de matricula: ")
                especialidadTipo = input("Ingrese el tipo de Especialidad: ")
                especialidadDias = input("Ingrese los dias de atencion(separados por coma): ")

                dias = [d.strip().lower() for d in especialidadDias.split(",")]

                especialidad = Especialidad(especialidadTipo, dias)

                nuevoMedico = Medico(nombre, apellido, matricula, especialidad)

                clinica.agregar_medico(nuevoMedico)

                print("Medico Agregado Correctamente!")
            
            if opcion == 3:

                print("Agendar Turno")

                
                dni = input("Ingrese el dni del paciente: ")
                matricula = input("Ingrese la matricula del medico: ")
                especialidad = input("Ingrese la especialidad del medico: ")
                fechaHora = input("Ingrese la fecha y la hora del turno(dd/mm/aaaa hh:mm): ")

                clinica.agendar_turno(dni, matricula, especialidad, fechaHora)
                print("Turno agendado correctamente.")

            if opcion == 4:
                matricula = input("Ingrese la matricula del medico: ")
                tipo = input("Indique el tipo de especialidad: ")
                dias = [input("Dias de atencion(separados por coma): ").split(',')]

                medico = clinica.obtener_medico_por_matricula(matricula)
                especialidad = Especialidad(tipo, dias)

                medico.agregar_especialidad(especialidad)

                print('Especialidad agregada.')

            if opcion == 5:
                dni = input("Ingrese el dni del paciente: ")
                matricula = input("Ingrese la matricula del medico: ")
                medicamentos = [m.strip() for m in input("Ingrese los medicamnetos(separados por coma): ").split(",") if m.strip()]

                clinica.emitir_receta(dni, matricula, medicamentos)

                print("Receta emitida correctamente.")
            
            if opcion == 6:
                dni = input("Ingrese el dni del paciente: ")
                print(f'Historia Clinica de Paciente con dni numero {dni}')
                
                historia = clinica.obtener_historia_clinica(dni)
                print(historia)

            if opcion == 7:
                print("Todos los turnos")

                turnos = clinica.obtener_turnos()

                if len(turnos) == 0:
                    print("No hay turnos agendados")
                else:
                    for t in turnos:
                        print(t)

            if opcion == 8:
                print("Todos los Pacientes: ")
                
                pacientes = clinica.obtener_pacientes()

                if len(pacientes) == 0:
                    print("Todavia no hay pacientes registrados.")
                else:
                    for p in pacientes:
                        print(pacientes[p])

            if opcion == 9:
                print("Todos los Medicos: ")
                
                medicos = clinica.obtener_medicos()

                if len(medicos) == 0:
                    print("Todavia no hay medicos registrados.")
                else:
                    for m in medicos:
                        print(medicos[m])

            if opcion == 0:
                exit()

        except ErrorGeneralTurno as e:
            print(e)

        except ErrorAlAgregarPaciente as e:
            print(e)

        except ErrorAlAgregarMedico as e:
            print(e)
        
        except PacienteNoEncontradoExcepcion as e:
            print(e)

        except MedicoNoDisponibleExcepcion as e:
            print(e)

        except TurnoOcupadoException as e:
            print(e)

        except ErrorPaciente as e:
            print(e)

        except ErrorMedico as e:
            print(e)
        
        except RecetaInvalidaException as e:
            print(e)

        except EspecialidadYaExistente as e:
            print(e)


if __name__ == "__main__":
    menu()