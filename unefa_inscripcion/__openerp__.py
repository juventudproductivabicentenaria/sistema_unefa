# -*- coding: utf-8 -*-
##############################################################################
#
#    Programa realizado por, Jeison Pernía y Jonathan Reyes en el marco
#    del plan de estudios de la UNEFA, como TRABAJO ESPECIAL DE GRADO,
#    con el fin de optar al título de Ingeniero de Sistemas.
#    
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com
#
##############################################################################
{
    'name': 'Unefa Inscripción de Asignaturas',
    'version': '1.0',
    'depends': ['base','unefa_configuracion'],
    'authors': 'Jeison Pernía y Jonathan Reyes',
    'category': 'Configuración Técnica',
    'description': """
    Módulo de inscripción de asignaturas...
    """,
    'update_xml': [],
    "data" : [
        'views/inscripcion_asignatura_view.xml',
        'report/report_planilla_inscripcion.xml',
        'report/report_planilla_inscripcion_data.xml',
        "security/filtro_inscripcion.xml",
        "security/access_asistente/ir.model.access.csv",
        "security/access_coordinador/ir.model.access.csv",
        "security/access_profesor/ir.model.access.csv",
        "security/access_estudiante/ir.model.access.csv",
        
        ],
    'installable': True,
    'auto_install': False,
}

