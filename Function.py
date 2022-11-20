class Function:
  def __init__(self, identifier,args,codigo,retorna):
        self.args = args
        self.retorna = retorna
        self.codigo = codigo
        self.identifier = identifier
  def __str__(self):
    return f"{self.identifier}// {self.args}// {self.codigo} // {self.retorna}"