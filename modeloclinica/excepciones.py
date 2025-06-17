class PacienteNoEncontradoExcepcion(Exception):
    pass

class MedicoNoEncontrado(Exception):
    pass

class MedicoNoDisponibleExcepcion(Exception):
    pass

class TurnoOcupadoException(Exception):
    pass

class RecetaInvalidaException(Exception):
    pass

class ErrorAlAgregarPaciente(Exception):
    pass

class ErrorAlAgregarMedico(Exception):
    pass

class EspecialidadYaExistente(Exception):
    pass

class ErrorGeneralTurno(Exception):
    pass

class ErrorGeneralClinica(Exception):
    pass

class ErrorPaciente(Exception):
    pass

class ErrorMedico(Exception):
    pass