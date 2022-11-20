class Variable:
  def __init__(self, identifier,data_type,valor):
        self.data_type = data_type
        self.valor = valor
        self.identifier = identifier
  def __str__(self):
    return f"{self.identifier}// {self.data_type}// {self.valor}"