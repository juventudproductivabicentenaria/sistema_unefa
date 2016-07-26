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
    'name': 'Pensum Académico',
    'version': '1.0',
    'depends': ['base','unefa_configuracion'],
    'authors': 'Jeison Pernía y Jonathan Reyes',
    'category': 'Configuración Técnica',
    'description': """
    Pensum académicos
    """,
    'update_xml': [],
    "data" : [
        'views/unefa_asignaturas.xml',
        'views/unefa_pensum.xml',
        'data/asignaturas_data.xml',
        'data/pensum_data.xml',
        "security/filtro_pensum.xml",
        "security/access_asistente/ir.model.access.csv",
        "security/access_coordinador/ir.model.access.csv",
        "security/access_profesor/ir.model.access.csv",
        "security/access_estudiante/ir.model.access.csv",
        
        ],
    'installable': True,
    'auto_install': False,
}

