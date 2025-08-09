from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import json
import os

class TipoBeneficiario(Enum):
    TRABAJADOR_SALUD = "trabajador_salud"
    PACIENTE_CUIDADOR = "paciente_cuidador"
    PERSONA_PARTICULAR = "persona_particular"

class Genero(Enum):
    MASCULINO = "masculino"
    FEMENINO = "femenino"
    OTRO = "otro"

class RespuestaTratamiento(Enum):
    EXCELENTE = "excelente"
    BUENA = "buena"
    REGULAR = "regular"
    MALA = "mala"

class Beneficiario:
    """Clase que representa un beneficiario del proyecto"""
    
    def __init__(self, nombre: str, tipo: TipoBeneficiario, genero: Genero, 
                 edad: int, enfermedad: str, herramienta_tratamiento: str, 
                 respuesta_tratamiento: RespuestaTratamiento):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__genero = genero
        self.__edad = edad
        self.__enfermedad = enfermedad
        self.__herramienta_tratamiento = herramienta_tratamiento
        self.__respuesta_tratamiento = respuesta_tratamiento
        self.__fecha_registro = datetime.now()
    
    # Properties (getters y setters) 
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def genero(self):
        return self.__genero
    
    @property
    def edad(self):
        return self.__edad
    
    @property
    def enfermedad(self):
        return self.__enfermedad
    
    @property
    def herramienta_tratamiento(self):
        return self.__herramienta_tratamiento
    
    @property
    def respuesta_tratamiento(self):
        return self.__respuesta_tratamiento
    
    @respuesta_tratamiento.setter
    def respuesta_tratamiento(self, valor: RespuestaTratamiento):
        self.__respuesta_tratamiento = valor
    
    def get_data(self):
        """Muestra información completa del beneficiario"""
        print(f"""
Id beneficiario: {self.__nombre}
Tipo: {self.__tipo.value}
Género: {self.__genero.value}
Edad: {self.__edad}
Enfermedad/Padecimiento: {self.__enfermedad}
Herramienta de tratamiento: {self.__herramienta_tratamiento}
Respuesta al tratamiento: {self.__respuesta_tratamiento.value}
""")
    
    def __str__(self):
        return f"{self.__nombre} ({self.__tipo.value}, {self.__edad} años)"

class Institucion:
    """Clase que representa una institución participante"""
    
    def __init__(self, nombre: str, direccion: str, telefono: str):
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.__beneficiarios: List[Beneficiario] = []
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def beneficiarios(self):
        return self.__beneficiarios.copy()
    
    def agregar_beneficiario(self, beneficiario: Beneficiario):
        """Agrega un beneficiario de los 3 grupos a la institución"""
        self.__beneficiarios.append(beneficiario)
        print(f"Beneficiario {beneficiario.nombre} agregado a {self.__nombre}")
    
    def remover_beneficiario(self, nombre: str) -> bool:
        """Remueve un beneficiario por nombre"""
        for i, beneficiario in enumerate(self.__beneficiarios):
            if beneficiario.nombre == nombre:
                self.__beneficiarios.pop(i)
                print(f"Beneficiario {nombre} removido de {self.__nombre}")
                return True
        print(f"Beneficiario {nombre} no encontrado en {self.__nombre}")
        return False
    
    def buscar_beneficiario(self, nombre: str) -> Optional[Beneficiario]:
        """Buscar beneficiario por su nombre"""
        for beneficiario in self.__beneficiarios:
            if beneficiario.nombre == nombre:
                return beneficiario
        return None
    
    def consultar_beneficiario(self, nombre: str):
        """Consulta y muestra información de un beneficiario"""
        beneficiario = self.buscar_beneficiario(nombre)
        if beneficiario:
            print(f"\nBENEFICIARIO ENCONTRADO en {self.__nombre}")
            beneficiario.get_data()
        else:
            print(f"\nEl beneficiario {nombre} no se encuentra registrado en {self.__nombre}")
    
    def obtener_estadisticas(self) -> Dict:
        """Obtener datos/estadísticas de beneficiarios en la institución"""
        total = len(self.__beneficiarios)
        if total == 0:
            return {"total": 0}
        
        stats = {
            "total": total,
            "por_tipo": {},
            "por_genero": {},
            "por_respuesta": {},
            "edad_promedio": sum(b.edad for b in self.__beneficiarios) / total
        }
        
        for beneficiario in self.__beneficiarios:
            # Estadísticas por tipo
            tipo = beneficiario.tipo.value
            stats["por_tipo"][tipo] = stats["por_tipo"].get(tipo, 0) + 1
            
            # Estadísticas por género
            genero = beneficiario.genero.value
            stats["por_genero"][genero] = stats["por_genero"].get(genero, 0) + 1
            
            # Estadísticas por respuesta al tratamiento
            respuesta = beneficiario.respuesta_tratamiento.value
            stats["por_respuesta"][respuesta] = stats["por_respuesta"].get(respuesta, 0) + 1
        
        return stats
    
    def __str__(self):
        return f"{self.__nombre} ({len(self.__beneficiarios)} beneficiarios)"

class Proyecto(ABC):
    """Clase base para proyectos"""
    
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: datetime):
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio
        self.__instituciones: List[Institucion] = []
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    @property
    def instituciones(self):
        return self.__instituciones.copy()
    
    def agregar_institucion(self, institucion: Institucion):
        """Agrega una institución al proyecto"""
        self.__instituciones.append(institucion)
        print(f"Institución {institucion.nombre} agregada al proyecto {self.__nombre}")
    
    def buscar_institucion(self, nombre: str) -> Optional[Institucion]:
        """Busca una institución por nombre"""
        for institucion in self.__instituciones:
            if institucion.nombre == nombre:
                return institucion
        return None
    
    def obtener_total_beneficiarios(self) -> int:
        """Obtiene el total de beneficiarios en el proyecto"""
        return sum(len(inst.beneficiarios) for inst in self.__instituciones)
    
    @abstractmethod
    def obtener_herramientas_especificas(self) -> List[str]:
        """Método que debe ser implementado por las subclases"""
        pass
    
    @abstractmethod
    def generar_reporte_especializado(self) -> Dict:
        """Método para generar reportes específicos del tipo de proyecto"""
        pass
    
    def obtener_estadisticas_generales(self) -> Dict:
        """Obtiene estadísticas generales del proyecto"""
        stats = {
            "nombre_proyecto": self.__nombre,
            "total_instituciones": len(self.__instituciones),
            "total_beneficiarios": self.obtener_total_beneficiarios(),
            "estadisticas_por_institucion": {}
        }
        
        for institucion in self.__instituciones:
            stats["estadisticas_por_institucion"][institucion.nombre] = institucion.obtener_estadisticas()
        
        return stats
    
    def __str__(self):
        return f"{self.__nombre} - {len(self.__instituciones)} instituciones"

class ProyectoMusicoterapia(Proyecto):
    """Clase específica para proyectos de musicoterapia"""
    
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: datetime):
        super().__init__(nombre, descripcion, fecha_inicio)
        self.__herramientas_disponibles = ["Meditación sonora", "Acompañamiento musical", "Taller"]
    
    def obtener_herramientas_especificas(self) -> List[str]:
        """Retorna las herramientas específicas de musicoterapia"""
        return self.__herramientas_disponibles.copy()
    
    def generar_reporte_especializado(self) -> Dict:
        """Genera reporte específico para musicoterapia"""
        reporte = self.obtener_estadisticas_generales()
        reporte["tipo_proyecto"] = "Musicoterapia"
        reporte["herramientas_disponibles"] = self.__herramientas_disponibles
        
        # Análisis específico de musicoterapia
        abordajes_usados = {}
        for institucion in self.instituciones:
            for beneficiario in institucion.beneficiarios:
                abordaje = beneficiario.herramienta_tratamiento
                abordajes_usados[abordaje] = abordajes_usados.get(abordaje, 0) + 1
        
        reporte["abordajes_mas_usados"] = abordajes_usados
        return reporte

class ProyectoArteterapia(Proyecto):
    """Clase específica para proyectos de arteterapia"""
    
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: datetime):
        super().__init__(nombre, descripcion, fecha_inicio)
        self.__tecnicas_disponibles = ["Pintura", "Poesía", "Lectura", "Artesanías", "Otro"]
    
    def obtener_herramientas_especificas(self) -> List[str]:
        """Retorna las herramientas específicas de arteterapia"""
        return self.__tecnicas_disponibles.copy()
    
    def generar_reporte_especializado(self) -> Dict:
        """Genera reporte específico para arteterapia"""
        reporte = self.obtener_estadisticas_generales()
        reporte["tipo_proyecto"] = "Arteterapia"
        reporte["tecnicas_disponibles"] = self.__tecnicas_disponibles
        
        # Análisis específico de arteterapia
        tecnicas_usadas = {}
        for institucion in self.instituciones:
            for beneficiario in institucion.beneficiarios:
                tecnica = beneficiario.herramienta_tratamiento
                tecnicas_usadas[tecnica] = tecnicas_usadas.get(tecnica, 0) + 1
        
        reporte["tecnicas_mas_usadas"] = tecnicas_usadas
        return reporte

class GestorProyectos:
    """Clase principal para gestionar el sistema"""
    
    def __init__(self):
        self.__proyectos: List[Proyecto] = []
    
    def agregar_proyecto(self, proyecto: Proyecto):
        """Agrega un proyecto al sistema"""
        self.__proyectos.append(proyecto)
        print(f"Proyecto {proyecto.nombre} agregado al sistema")
    
    def buscar_proyecto(self, nombre: str) -> Optional[Proyecto]:
        """Busca un proyecto por nombre"""
        for proyecto in self.__proyectos:
            if proyecto.nombre == nombre:
                return proyecto
        return None
    
    def listar_proyectos(self) -> List[str]:
        """Lista todos los proyectos"""
        return [proyecto.nombre for proyecto in self.__proyectos]
    
    def buscar_beneficiario_global(self, nombre: str) -> List[tuple]:
        """Busca un beneficiario en todos los proyectos e instituciones"""
        resultados = []
        for proyecto in self.__proyectos:
            for institucion in proyecto.instituciones:
                beneficiario = institucion.buscar_beneficiario(nombre)
                if beneficiario:
                    resultados.append((proyecto.nombre, institucion.nombre, beneficiario))
        return resultados
    
    def generar_reporte_consolidado(self) -> Dict:
        """Genera un reporte consolidado de todos los proyectos"""
        reporte = {
            "fecha_generacion": datetime.now().isoformat(),
            "total_proyectos": len(self.__proyectos),
            "total_beneficiarios": sum(p.obtener_total_beneficiarios() for p in self.__proyectos),
            "proyectos": []
        }
        
        for proyecto in self.__proyectos:
            reporte["proyectos"].append(proyecto.generar_reporte_especializado())
        
        return reporte
    
    def exportar_datos(self, archivo: str = "reporte_proyectos.json") -> bool:
        """Exporta todos los datos a un archivo JSON"""
        try:
            reporte = self.generar_reporte_consolidado()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(reporte, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False

# Función para imprimir menú de opciones
def impresion_menu():
    lmenu = [
        "1. Agregar beneficiario", 
        "2. Consultar beneficiario", 
        "3. Ver estadísticas proyecto", 
        "4. Generar reporte consolidado",
        "5. Exportar datos",
        "6. Salir"
    ]
    
    print("\n" + "="*50)
    print("MENÚ DE OPCIONES - SISTEMA DE SALUD PÚBLICA")
    print("="*50)
    for opcion in lmenu:
        print(opcion)
    
    while True:
        try:
            op = int(input("\nDigite su opción: "))
            if 1 <= op <= len(lmenu):
                return op
            else:
                print(f"Su opción debe ser un número entre 1 y {len(lmenu)}")
        except ValueError:
            print(f"Su opción debe ser un número entre 1 y {len(lmenu)}")

def main():
    """Función principal para demostrar el uso del sistema"""
    
    print("=== SISTEMA DE GESTIÓN DE PROYECTOS DE SALUD PÚBLICA ===")
    
    # Crear gestor principal
    gestor = GestorProyectos()
    
    # Crear proyectos
    proyecto_musico = ProyectoMusicoterapia(
        "Melodía Vital", 
        "Proyecto de musicoterapia para bienestar integral",
        datetime(2024, 1, 15)
    )
    
    proyecto_arte = ProyectoArteterapia(
        "Cuadro Clínico",
        "Proyecto de arteterapia para expresión y sanación",
        datetime(2024, 2, 1)
    )
    
    # Agregar proyectos al gestor
    gestor.agregar_proyecto(proyecto_musico)
    gestor.agregar_proyecto(proyecto_arte)
    
    # Crear instituciones
    hospital = Institucion("Hospital General", "Av. Salud 123", "555-0001")
    clinica = Institucion("Clínica del Valle", "Calle Bienestar 456", "555-0002")
    centro = Institucion("Centro de Rehabilitación", "Plaza Esperanza 789", "555-0003")
    
    # Agregar instituciones a proyectos
    proyecto_musico.agregar_institucion(hospital)
    proyecto_musico.agregar_institucion(clinica)
    proyecto_musico.agregar_institucion(centro)
    
    proyecto_arte.agregar_institucion(hospital)
    proyecto_arte.agregar_institucion(clinica)
    proyecto_arte.agregar_institucion(centro)
    
    # Crear algunos beneficiarios de ejemplo
    beneficiarios_ejemplo = [
        Beneficiario("Ana García", TipoBeneficiario.TRABAJADOR_SALUD, Genero.FEMENINO, 35, 
                    "Estrés laboral", "Meditación sonora", RespuestaTratamiento.EXCELENTE),
        Beneficiario("Carlos López", TipoBeneficiario.PACIENTE_CUIDADOR, Genero.MASCULINO, 42,
                    "Ansiedad", "Acompañamiento musical", RespuestaTratamiento.BUENA),
        Beneficiario("María Torres", TipoBeneficiario.PERSONA_PARTICULAR, Genero.FEMENINO, 28,
                    "Depresión", "Taller", RespuestaTratamiento.REGULAR)
    ]
    
    # Agregar beneficiarios de ejemplo al hospital en musicoterapia
    hospital_musico = proyecto_musico.buscar_institucion("Hospital General")
    for beneficiario in beneficiarios_ejemplo:
        hospital_musico.agregar_beneficiario(beneficiario)
    
    print("\n=== DATOS INICIALES CARGADOS ===")
    print("✓ Proyectos creados: Melodía Vital (Musicoterapia) y Cuadro Clínico (Arteterapia)")
    print("✓ Instituciones agregadas a cada proyecto")
    print("✓ Beneficiarios de ejemplo agregados")
    
    # Menú interactivo
    op = impresion_menu()
    
    while op != 6:  # 6 es "Salir"
        if op == 1:  # Agregar beneficiario
            print("\n--- AGREGAR BENEFICIARIO ---")
            
            # Seleccionar proyecto
            proyectos = gestor.listar_proyectos()
            print("Proyectos disponibles:")
            for i, proyecto in enumerate(proyectos, 1):
                print(f"{i}. {proyecto}")
            
            try:
                sel_proyecto = int(input("Seleccione proyecto (número): ")) - 1
                if 0 <= sel_proyecto < len(proyectos):
                    proyecto_sel = gestor.buscar_proyecto(proyectos[sel_proyecto])
                    
                    # Seleccionar institución
                    instituciones = [inst.nombre for inst in proyecto_sel.instituciones]
                    print(f"\nInstituciones en {proyecto_sel.nombre}:")
                    for i, inst in enumerate(instituciones, 1):
                        print(f"{i}. {inst}")
                    
                    sel_inst = int(input("Seleccione institución (número): ")) - 1
                    if 0 <= sel_inst < len(instituciones):
                        institucion_sel = proyecto_sel.buscar_institucion(instituciones[sel_inst])
                        
                        # Recoger datos del beneficiario
                        nombre = input("Nombre del beneficiario: ")
                        
                        print("Tipos de beneficiario:")
                        tipos = list(TipoBeneficiario)
                        for i, tipo in enumerate(tipos, 1):
                            print(f"{i}. {tipo.value}")
                        
                        tipo_sel = int(input("Seleccione tipo (número): ")) - 1
                        tipo = tipos[tipo_sel]
                        
                        print("Géneros:")
                        generos = list(Genero)
                        for i, genero in enumerate(generos, 1):
                            print(f"{i}. {genero.value}")
                        
                        genero_sel = int(input("Seleccione género (número): ")) - 1
                        genero = generos[genero_sel]
                        
                        edad = int(input("Edad: "))
                        enfermedad = input("Enfermedad/Padecimiento: ")
                        
                        # Mostrar herramientas disponibles según el tipo de proyecto
                        herramientas = proyecto_sel.obtener_herramientas_especificas()
                        print("Herramientas de tratamiento disponibles:")
                        for i, herramienta in enumerate(herramientas, 1):
                            print(f"{i}. {herramienta}")
                        
                        herr_sel = int(input("Seleccione herramienta (número): ")) - 1
                        herramienta = herramientas[herr_sel]
                        
                        print("Respuesta al tratamiento:")
                        respuestas = list(RespuestaTratamiento)
                        for i, respuesta in enumerate(respuestas, 1):
                            print(f"{i}. {respuesta.value}")
                        
                        resp_sel = int(input("Seleccione respuesta (número): ")) - 1
                        respuesta = respuestas[resp_sel]
                        
                        # Crear y agregar beneficiario
                        nuevo_beneficiario = Beneficiario(nombre, tipo, genero, edad, 
                        enfermedad, herramienta, respuesta)
                        institucion_sel.agregar_beneficiario(nuevo_beneficiario)
                        
                    else:
                        print("Institución no válida")
                else:
                    print("Proyecto no válido")
            except (ValueError, IndexError):
                print("Entrada no válida")
        
        elif op == 2:  # Consultar beneficiario
            print("\n--- CONSULTAR BENEFICIARIO ---")
            nombre = input("Nombre del beneficiario a buscar: ")
            resultados = gestor.buscar_beneficiario_global(nombre)
            
            if resultados:
                for proyecto_nom, institucion_nom, beneficiario in resultados:
                    print(f"\nEncontrado en: {proyecto_nom} -> {institucion_nom}")
                    beneficiario.get_data()
            else:
                print("Beneficiario no encontrado")
        
        elif op == 3:  # Ver estadísticas proyecto
            print("\n--- ESTADÍSTICAS POR PROYECTO ---")
            proyectos = gestor.listar_proyectos()
            print("Proyectos disponibles:")
            for i, proyecto in enumerate(proyectos, 1):
                print(f"{i}. {proyecto}")
            
            try:
                sel_proyecto = int(input("Seleccione proyecto (número): ")) - 1
                if 0 <= sel_proyecto < len(proyectos):
                    proyecto_sel = gestor.buscar_proyecto(proyectos[sel_proyecto])
                    reporte = proyecto_sel.generar_reporte_especializado()
                    
                    print(f"\n=== ESTADÍSTICAS {reporte['tipo_proyecto'].upper()} ===")
                    print(f"Proyecto: {reporte['nombre_proyecto']}")
                    print(f"Total instituciones: {reporte['total_instituciones']}")
                    print(f"Total beneficiarios: {reporte['total_beneficiarios']}")
                    
                    if reporte['tipo_proyecto'] == 'Musicoterapia':
                        print(f"Abordajes más usados: {reporte['abordajes_mas_usados']}")
                    else:
                        print(f"Técnicas más usadas: {reporte['tecnicas_mas_usadas']}")
                else:
                    print("Proyecto no válido")
            except (ValueError, IndexError):
                print("Entrada no válida")
        
        elif op == 4:  # Generar reporte consolidado
            print("\n--- REPORTE CONSOLIDADO ---")
            reporte = gestor.generar_reporte_consolidado()
            print(f"Fecha: {reporte['fecha_generacion']}")
            print(f"Total proyectos: {reporte['total_proyectos']}")
            print(f"Total beneficiarios: {reporte['total_beneficiarios']}")
            print("\nProyectos:")
            for proyecto in reporte['proyectos']:
                print(f"- {proyecto['nombre_proyecto']} ({proyecto['tipo_proyecto']}): {proyecto['total_beneficiarios']} beneficiarios")
        
        elif op == 5:  # Exportar datos
            print("\n--- EXPORTAR DATOS ---")
            if gestor.exportar_datos():
                print("✓ Datos exportados exitosamente a 'reporte_proyectos.json'")
            else:
                print("✗ Error al exportar datos")
        
        else:
            print("Opción no válida")
        
        op = impresion_menu()
    
    print("\n=== SISTEMA FINALIZADO ===")
    print("Gracias por usar el sistema de gestión de proyectos de salud pública de Fundacion Sanartes")

if __name__ == "__main__":
    main()
