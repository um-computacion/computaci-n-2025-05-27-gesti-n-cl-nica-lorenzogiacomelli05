import unittest
from datetime import datetime, timedelta
from modeloclinica.Turnosclinica import Clinica, Paciente, Medico, Especialidad
from modeloclinica.excepciones import *

class TestExcepcionesClinica(unittest.TestCase):
    
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Juan", "Pérez", "12345678", "01/01/2000")
        self.medico = Medico("Ana", "Lopez", "M001", Especialidad("Cardiología", ["lunes", "miércoles"]))

    def test_paciente_no_encontrado(self):
        with self.assertRaises(PacienteNoEncontradoExcepcion):
            self.clinica.obtener_historia_clinica("00000000")

    def test_medico_no_encontrado(self):
        with self.assertRaises(MedicoNoDisponibleExcepcion):
            self.clinica.obtener_medico_por_matricula("X000")

    def test_turno_ocupado(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        fecha = datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7)  # próximo lunes
        fecha_str = fecha.strftime("%d/%m/%Y 10:00")
        self.clinica.agendar_turno("12345678", "M001", "Cardiología", fecha_str)
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("12345678", "M001", "Cardiología", fecha_str)

    def test_dia_domingo(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        domingo = datetime.now() + timedelta(days=(6 - datetime.now().weekday()) % 7)
        domingo_str = domingo.strftime("%d/%m/%Y 10:00")
        with self.assertRaises(ErrorGeneralTurno):
            self.clinica.agendar_turno("12345678", "M001", "Cardiología", domingo_str)

    def test_especialidad_no_valida_para_dia(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        fecha = datetime.now() + timedelta(days=(1 - datetime.now().weekday()) % 7)  # próximo martes
        fecha_str = fecha.strftime("%d/%m/%Y 10:00")
        with self.assertRaises(MedicoNoDisponibleExcepcion):
            self.clinica.agendar_turno("12345678", "M001", "Cardiología", fecha_str)

    def test_error_receta_vacia(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "M001", [])

    def test_error_paciente_duplicado(self):
        self.clinica.agregar_paciente(self.paciente)
        with self.assertRaises(ErrorPaciente):
            self.clinica.agregar_paciente(self.paciente)

    def test_error_medico_duplicado(self):
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(ErrorMedico):
            self.clinica.agregar_medico(self.medico)

    def test_especialidad_ya_existente(self):
        especialidad = Especialidad("Cardiología", ["lunes"])
        with self.assertRaises(EspecialidadYaExistente):
            self.medico.agregar_especialidad(especialidad)