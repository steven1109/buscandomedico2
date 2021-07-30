from regions.domain.model_departamento import Departamento

departamento = Departamento()

departamento.set_cod_departamento("14")
departamento.set_des_departamento("Lima")

print(departamento.get_cod_departamento() + " -- " + departamento.get_des_departamento())
