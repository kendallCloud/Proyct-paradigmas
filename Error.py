class Error:
  def __init__(self,linea,error_message,tipo_error,err_cod):
    self.linea = linea
    self.error_message = error_message
    self.tipo_error = tipo_error
    self.err_cod = err_cod
   
  def __str__(self):
    return f"line:{self.linea} error type:{self.tipo_error} error code: {self.err_cod}error_message: {self.error_message} \n"