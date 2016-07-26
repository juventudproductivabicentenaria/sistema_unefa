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
    'name': 'Planificación de Semestre',
    'version': '1.0',
    'depends': ['base','unefa_configuracion','unefa_pensum','unefa_usuarios'],
    'authors': 'Jeison Pernía y Jonathan Reyes',
    'category': 'Configuración Técnica',
    'description': """
    Este módulo configura la planificación de semetsre emanada de las 
    autoridades de la UNEFA a las coordinaciones.
    """,
    'update_xml': [],
    "data" : [
        'views/configuracion_cronograma_periodo_academico/configuracion_cronograma_periodo_academico.xml',
        'views/planificacion_semestre/unefa_planificacion_semestre_view.xml',
        'data/cronogr_actividades_data.xml',
        'data/periodo_data.xml',
        'security/filtro_planificacion.xml',
        'security/access_asistente/ir.model.access.csv',
        'security/access_coordinador/ir.model.access.csv',
        'security/access_estudiantes/ir.model.access.csv',
        'security/access_profesores/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': False,
}

