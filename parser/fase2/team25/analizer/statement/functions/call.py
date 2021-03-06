from analizer.abstract.expression import Expression, TYPE
from analizer.abstract import expression
from analizer.reports import Nodo
from analizer.statement.expressions.primitive import Primitive
import pandas as pd
from analizer.libs import TrigonometricFunctions as trf
from analizer.libs import MathFunctions as mf
from analizer.libs import StringFunctions as strf
from datetime import datetime
from analizer.statement.pl.function import envFunction

class FunctionCall(Expression):
    """
    Esta clase contiene las llamadas a funciones
    """

    def __init__(self, function, params, row, column):
        Expression.__init__(self, row, column)
        self.function = function.lower()
        self.params = params
        i = 0
        self.temp = str(function) + "("
        for t in params:
            if i > 0:
                self.temp += ", "
            self.temp += t.temp
            i += 1
        self.temp += ")"

    # TODO: Agregar un error de parametros incorrectos
    def execute(self, environment):
        type_ = TYPE.NUMBER
        try:
            valores = []
            types = []
            for p in self.params:
                obj = p.execute(environment)
                val = obj.value
                t = obj.type
                if isinstance(val, pd.core.series.Series):
                    val = val.tolist()
                valores.append(val)
                types.append(t)
            # Se toma en cuenta que las funcines matematicas
            # y trigonometricas producen un tipo NUMBER
            type_ = TYPE.NUMBER
            if self.function == "abs":
                value = mf.absolute(*valores)
            elif self.function == "cbrt":
                value = mf.cbrt(*valores)
            elif self.function == "ceil":
                value = mf.ceil(*valores)
            elif self.function == "ceiling":
                value = mf.ceiling(*valores)
            elif self.function == "degrees":
                value = mf.degrees(*valores)
            elif self.function == "div":
                value = mf.div(*valores)
            elif self.function == "exp":
                value = mf.exp(*valores)
            elif self.function == "factorial":
                value = mf.factorial(*valores)
            elif self.function == "floor":
                value = mf.floor(*valores)
            elif self.function == "gcd":
                value = mf.gcd(*valores)
            elif self.function == "lcm":
                value = mf.lcm(*valores)
            elif self.function == "ln":
                value = mf.ln(*valores)
            elif self.function == "log":
                value = mf.log(*valores)
            elif self.function == "log10":
                value = mf.log10(*valores)
            elif self.function == "mod":
                value = mf.mod(*valores)
            elif self.function == "pi":
                value = mf.pi()
            elif self.function == "power":
                value = mf.pow(*valores)
            elif self.function == "radians":
                value = mf.radians(*valores)
            elif self.function == "round":
                value = mf.round_(*valores)
            elif self.function == "sign":
                value = mf.sign(*valores)
            elif self.function == "sqrt":
                value = mf.sqrt(*valores)
            elif self.function == "trunc":
                value = mf.truncate_col(*valores)
            elif self.function == "width_bucket":
                value = mf.with_bucket(*valores)
            elif self.function == "random":
                value = mf.random_()
            elif self.function == "acos":
                value = trf.acos(*valores)
            elif self.function == "acosd":
                value = trf.acosd(*valores)
            elif self.function == "asin":
                value = trf.asin(*valores)
            elif self.function == "asind":
                value = trf.asind(*valores)
            elif self.function == "atan":
                value = trf.atan(*valores)
            elif self.function == "atand":
                value = trf.atand(*valores)
            elif self.function == "atan2":
                value = trf.atan2(*valores)
            elif self.function == "atan2d":
                value = trf.atan2d(*valores)
            elif self.function == "cos":
                value = trf.cos(*valores)
            elif self.function == "cosd":
                value = trf.cosd(*valores)
            elif self.function == "cot":
                value = trf.cot(*valores)
            elif self.function == "cotd":
                value = trf.cotd(*valores)
            elif self.function == "sin":
                value = trf.sin(*valores)
            elif self.function == "sind":
                value = trf.sind(*valores)
            elif self.function == "tan":
                value = trf.tan(*valores)
            elif self.function == "tand":
                value = trf.tand(*valores)
            elif self.function == "sinh":
                value = trf.sinh(*valores)
            elif self.function == "cosh":
                value = trf.cosh(*valores)
            elif self.function == "tanh":
                value = trf.tanh(*valores)
            elif self.function == "asinh":
                value = trf.asinh(*valores)
            elif self.function == "acosh":
                value = trf.acosh(*valores)
            elif self.function == "atanh":
                value = trf.atanh(*valores)
            elif self.function == "length":
                value = strf.lenght(*valores)
            elif self.function == "substring":
                type_ = TYPE.STRING
                value = strf.substring(*valores)
            elif self.function == "trim":
                type_ = TYPE.STRING
                value = strf.trim_(*valores)
            elif self.function == "get_byte":
                value = strf.get_byte(*valores)
            elif self.function == "md5":
                type_ = TYPE.STRING
                value = strf.md5(*valores)
            elif self.function == "set_byte":
                type_ = TYPE.STRING
                value = strf.set_byte(*valores)
            elif self.function == "sha256":
                type_ = TYPE.STRING
                value = strf.sha256(*valores)
            elif self.function == "substr":
                type_ = TYPE.STRING
                value = strf.substring(*valores)
            elif self.function == "convert_date":
                type_ = TYPE.DATETIME
                value = strf.convert_date(*valores)
            elif self.function == "convert_int":
                value = strf.convert_int(*valores)
            elif self.function == "encode":
                type_ = TYPE.STRING
                value = strf.encode(*valores)
            elif self.function == "decode":
                type_ = TYPE.STRING
                value = strf.decode(*valores)
            # Se toma en cuenta que la funcion now produce tipo DATE
            elif self.function == "now":
                type_ = TYPE.DATETIME
                value = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            else:
                # TODO: Agregar un error de funcion desconocida
                value = valores[0]
            if isinstance(value, list):
                if len(value) <= 1:
                    value = value[0]
                else:
                    value = pd.Series(value)
            return Primitive(type_, value, self.temp, self.row, self.column)
        except TypeError:
            expression.list_errors.append(
                "Error: 42883: La funcion "
                + str(self.function)
                + "("
                + str(type_)
                + ") no existe"
                + "\n En la linea: "
                + str(self.row)
            )
        except:
            expression.list_errors.append("Error: P0001: Error en funciones")

    def dot(self):
        f = Nodo.Nodo(self.function)
        new = Nodo.Nodo("CALL")
        new.addNode(f)
        if len(self.params) >0:
            p = Nodo.Nodo("PARAMS")
            for par in self.params:
                p.addNode(par.dot())
            new.addNode(p)
        return new

    def generate3d(self, environment, instanciaAux):
            if self.function == "abs":
                return f'{self.execute(0).value}'  #FALTA COSEGUIR LOS PARAMTROS en las funciones No definidas
            elif self.function == "cbrt":
                return f'{self.execute(0).value}' 
            elif self.function == "ceil":
                return f'{self.execute(0).value}' 
            elif self.function == "ceiling":
                return f'{self.execute(0).value}'  
            elif self.function == "degrees":
                return f'{self.execute(0).value}'  
            elif self.function == "div":
                return f'{self.execute(0).value}'  
            elif self.function == "exp":
                return f'{self.execute(0).value}'  
            elif self.function == "factorial":
                return f'{self.execute(0).value}'  
            elif self.function == "floor":
                return f'{self.execute(0).value}'  
            elif self.function == "gcd":
                return f'{self.execute(0).value}'  
            elif self.function == "lcm":
                return f'{self.execute(0).value}'  
            elif self.function == "ln":
                return f'{self.execute(0).value}'  
            elif self.function == "log":
                return f'{self.execute(0).value}'  
            elif self.function == "log10":
                return f'{self.execute(0).value}'  
            elif self.function == "mod":
                return f'{self.execute(0).value}'  
            elif self.function == "pi":
                return f'{self.execute(0).value}'  
            elif self.function == "power":
                return f'{self.execute(0).value}'  
            elif self.function == "radians":
                return f'{self.execute(0).value}'  
            elif self.function == "round":
                return f'{self.execute(0).value}'  
            elif self.function == "sign":
                return f'{self.execute(0).value}'  
            elif self.function == "sqrt":
                return f'{self.execute(0).value}'  
            elif self.function == "trunc":
                return f'{self.execute(0).value}'  
            elif self.function == "width_bucket":
                return f'{self.execute(0).value}'  
            elif self.function == "random":
                return f'{self.execute(0).value}'  
            elif self.function == "acos":
                return f'{self.execute(0).value}'  
            elif self.function == "acosd":
                return f'{self.execute(0).value}'  
            elif self.function == "asin":
                return f'{self.execute(0).value}'  
            elif self.function == "asind":
                return f'{self.execute(0).value}'  
            elif self.function == "atan":
                return f'{self.execute(0).value}'  
            elif self.function == "atand":
                return f'{self.execute(0).value}'  
            elif self.function == "atan2":
                return f'{self.execute(0).value}'  
            elif self.function == "atan2d":
                return f'{self.execute(0).value}'  
            elif self.function == "cos":
                return f'{self.execute(0).value}'  
            elif self.function == "cosd":
                return f'{self.execute(0).value}'  
            elif self.function == "cot":
                return f'{self.execute(0).value}'  
            elif self.function == "cotd":
                return f'{self.execute(0).value}'  
            elif self.function == "sin":
                return f'{self.execute(0).value}'  
            elif self.function == "sind":
                return f'{self.execute(0).value}'  
            elif self.function == "tan":
                return f'{self.execute(0).value}'  
            elif self.function == "tand":
                return f'{self.execute(0).value}'  
            elif self.function == "sinh":
                return f'{self.execute(0).value}'  
            elif self.function == "cosh":
                return f'{self.execute(0).value}'  
            elif self.function == "tanh":
                return f'{self.execute(0).value}'  
            elif self.function == "asinh":
                return f'{self.execute(0).value}'  
            elif self.function == "acosh":
                return f'{self.execute(0).value}'  
            elif self.function == "atanh":
                return f'{self.execute(0).value}'  
            elif self.function == "length":
                return f'{self.execute(0).value}'  
            elif self.function == "substring":
                return f'{self.execute(0).value}'  
            elif self.function == "trim":
                return f'{self.execute(0).value}'  
            elif self.function == "get_byte":
                return f'{self.execute(0).value}'  
            elif self.function == "md5":
                return f'{self.execute(0).value}'  
            elif self.function == "set_byte":
                return f'{self.execute(0).value}'  
            elif self.function == "sha256":
                return f'{self.execute(0).value}'  
            elif self.function == "substr":
                return f'{self.execute(0).value}'  
            elif self.function == "convert_date":
                return f'{self.execute(0).value}'  
            elif self.function == "convert_int":
                return f'{self.execute(0).value}'  
            elif self.function == "encode":
                return f'{self.execute(0).value}'  
            elif self.function == "decode":
                return f'{self.execute(0).value}'  
            elif self.function == "now":
                return f'{self.execute(0).value}'  
            else:
                tbFun = envFunction.getFunc(self.function)
                print(tbFun)
                #falta validacion de existencia
                tn = instanciaAux.getNewTemporal()
                salida = f'\t{tn} = {self.function}\n\t{tn} = RETURN[0]'
                instanciaAux.addToCode(salida)
            return tn


    def validaFuncionesFase2(self):
            if self.function == "abs":
                pass
            elif self.function == "cbrt":
                pass
            elif self.function == "ceil":
                pass
            elif self.function == "ceiling":
                pass
            elif self.function == "degrees":
                pass
            elif self.function == "div":
                pass
            elif self.function == "exp":
                pass
            elif self.function == "factorial":
                pass
            elif self.function == "floor":
                pass
            elif self.function == "gcd":
                pass
            elif self.function == "lcm":
                pass
            elif self.function == "ln":
                pass
            elif self.function == "log":
                pass
            elif self.function == "log10":
                pass
            elif self.function == "mod":
                pass
            elif self.function == "pi":
                pass
            elif self.function == "power":
                pass
            elif self.function == "radians":
                pass
            elif self.function == "round":
                pass
            elif self.function == "sign":
                pass
            elif self.function == "sqrt":
                pass
            elif self.function == "trunc":
                pass
            elif self.function == "width_bucket":
                pass
            elif self.function == "random":
                pass
            elif self.function == "acos":
                pass
            elif self.function == "acosd":
                pass
            elif self.function == "asin":
                pass
            elif self.function == "asind":
                pass
            elif self.function == "atan":
                pass
            elif self.function == "atand":
                pass
            elif self.function == "atan2":
                pass
            elif self.function == "atan2d":
                pass
            elif self.function == "cos":
                pass
            elif self.function == "cosd":
                pass
            elif self.function == "cot":
                pass
            elif self.function == "cotd":
                pass
            elif self.function == "sin":
                pass
            elif self.function == "sind":
                pass
            elif self.function == "tan":
                pass
            elif self.function == "tand":
                pass
            elif self.function == "sinh":
                pass
            elif self.function == "cosh":
                pass
            elif self.function == "tanh":
                pass
            elif self.function == "asinh":
                pass
            elif self.function == "acosh":
                pass
            elif self.function == "atanh":
                pass
            elif self.function == "length":
                pass
            elif self.function == "substring":
                pass
            elif self.function == "trim":
                pass
            elif self.function == "get_byte":
                pass
            elif self.function == "md5":
                pass
            elif self.function == "set_byte":
                pass
            elif self.function == "sha256":
                pass
            elif self.function == "substr":
                pass
            elif self.function == "convert_date":
                pass
            elif self.function == "convert_int":
                pass
            elif self.function == "encode":
                pass
            elif self.function == "decode":
                pass
            elif self.function == "now":
                pass
            else:
                tbFun = envFunction.getFunc(self.function)
                print(tbFun)
                pass
