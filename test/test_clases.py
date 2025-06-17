import unittest
from datetime import datetime
from modeloclinica.Turnosclinica import Paciente, Medico, Especialidad, Clinica
from modeloclinica.excepciones import (
    EspecialidadYaExistente, ErrorPaciente, ErrorMedico,
    RecetaInvalidaException, PacienteNoEncontradoExcepcion,
    MedicoNoDisponibleExcepcion, TurnoOcupadoException,
    ErrorGeneralTurno
)

class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()

        self.paciente1 = Paciente("Juan", "Perez", "12345678", "01/01/1980")
        self.paciente2 = Paciente("Ana", "Lopez", "87654321", "15/07/1990")

        self.esp1 = Especialidad("Cardiología", ["lunes", "miércoles"])
        self.esp2 = Especialidad("Pediatría", ["martes", "jueves"])

        self.medico1 = Medico("Carlos", "Gomez", "M123", self.esp1)
        self.medico2 = Medico("Laura", "Martinez", "M456", self.esp2)

   
    def test_registro_paciente_exitoso(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.assertIn("12345678", self.clinica.obtener_pacientes())

    def test_registro_paciente_duplicado(self):
        self.clinica.agregar_paciente(self.paciente1)
        with self.assertRaises(ErrorPaciente):
            self.clinica.agregar_paciente(self.paciente1)

    def test_registro_medico_exitoso(self):
        self.clinica.agregar_medico(self.medico1)
        self.assertIn("M123", self.clinica.obtener_medicos())

    def test_registro_medico_duplicado(self):
        self.clinica.agregar_medico(self.medico1)
        with self.assertRaises(ErrorMedico):
            self.clinica.agregar_medico(self.medico1)

    

    def test_agregar_especialidad_nueva(self):
        self.clinica.agregar_medico(self.medico1)
        nueva_esp = Especialidad("Neurología", ["viernes"])

        especialidades_actuales = self.medico1._Medico__especialidades

        self.medico1.agregar_especialidad(nueva_esp)
        nombres = [e.obtener_especialidad() for e in especialidades_actuales] + [nueva_esp.obtener_especialidad()]
        self.assertIn("Neurología", nombres)

    def test_agregar_especialidad_duplicada(self):
        self.clinica.agregar_medico(self.medico1)

        especialidades_actuales = self.medico1._Medico__especialidades

        with self.assertRaises(EspecialidadYaExistente):
            self.medico1.agregar_especialidad(especialidades_actuales[0])

    def test_agregar_especialidad_medico_no_registrado(self):
        with self.assertRaises(MedicoNoDisponibleExcepcion):
            self.clinica.obtener_medico_por_matricula("M999")


    def test_agendar_turno_exitoso(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        fecha_hora = "30/06/2025 09:00"  
        self.clinica.agendar_turno("12345678", "M123", "Cardiología", fecha_hora)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].obtener_medico().obtener_matricula(), "M123")

    def test_turno_duplicado(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        fecha_hora = "30/06/2025 09:00"  
        self.clinica.agendar_turno("12345678", "M123", "Cardiología", fecha_hora)
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("12345678", "M123", "Cardiología", fecha_hora)

    def test_turno_paciente_no_existente(self):
        self.clinica.agregar_medico(self.medico1)
        fecha_hora = "30/06/2025 09:00"
        with self.assertRaises(PacienteNoEncontradoExcepcion):
            self.clinica.agendar_turno("00000000", "M123", "Cardiología", fecha_hora)

    def test_turno_medico_no_existente(self):
        self.clinica.agregar_paciente(self.paciente1)
        fecha_hora = "30/06/2025 09:00"
        with self.assertRaises(MedicoNoDisponibleExcepcion):
            self.clinica.agendar_turno("12345678", "M999", "Cardiología", fecha_hora)

    def test_turno_especialidad_no_atendida(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        fecha_hora = "30/06/2025 09:00"
        with self.assertRaises(MedicoNoDisponibleExcepcion):
            self.clinica.agendar_turno("12345678", "M123", "Pediatría", fecha_hora)

    def test_turno_dia_no_laboral(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        fecha_hora = "06/07/2025 09:00"  
        with self.assertRaises(ErrorGeneralTurno):
            self.clinica.agendar_turno("12345678", "M123", "Cardiología", fecha_hora)

    def test_emitir_receta_exitoso(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        medicamentos = ["Paracetamol", "Ibuprofeno"]
        self.clinica.emitir_receta("12345678", "M123", medicamentos)
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_emitir_receta_sin_medicamentos(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "M123", [])

    def test_emitir_receta_paciente_no_existente(self):
        self.clinica.agregar_medico(self.medico1)
        with self.assertRaises(PacienteNoEncontradoExcepcion):
            self.clinica.emitir_receta("00000000", "M123", ["Paracetamol"])

    def test_emitir_receta_medico_no_existente(self):
        self.clinica.agregar_paciente(self.paciente1)
        with self.assertRaises(MedicoNoDisponibleExcepcion):
            self.clinica.emitir_receta("12345678", "M999", ["Paracetamol"])

    def test_historia_clinica_guarda_turnos_y_recetas(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        fecha_hora = "30/06/2025 09:00"
        self.clinica.agendar_turno("12345678", "M123", "Cardiología", fecha_hora)
        self.clinica.emitir_receta("12345678", "M123", ["Paracetamol"])
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_turnos()), 1)
        self.assertEqual(len(historia.obtener_recetas()), 1)

if __name__ == '__main__':
    unittest.main()