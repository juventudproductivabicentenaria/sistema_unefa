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
    'name': 'Unefa Cronograma Recuperación',
    'version': '1.0',
    'depends': ['base_setup','unefa_configuracion','unefa_pensum','unefa_oferta_academica'],
    'author': 'Jeison Pernía y Jonathan Reyes',
    'category': '',
    'description': """
    Modulo "Cronograma de reparación".
    """,
    'update_xml': [],
    "data" : [
        'views/unefa_cronograma_recuperacion_view.xml',
        'report/report_cronograma_recuperacion_data.xml',
        'report/report_cronograma_recuperacion_template.xml',
        'security/filtro_cronograma_recuperacion.xml',
        'security/access_asistente/ir.model.access.csv',
        'security/access_coordinador/ir.model.access.csv',
        'security/access_estudiantes/ir.model.access.csv',
        'security/access_profesores/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': False,
}
