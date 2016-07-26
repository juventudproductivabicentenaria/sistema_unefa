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
    'name':'Unefa Oferta Académica',
    'version': '1.0',
    'depends': ['base_setup','unefa_configuracion','unefa_pensum','unefa_usuarios'],
    'author': 'Jeison Pernía y Jonathan Reyes',
    'category': '',
    'description': """
        Módulo donde se define las oferta académica de la Coordinación.
    """,
    'update_xml': [],
    "data" : [
        "views/unefa_oferta_academica_view.xml",
        "data/tipo_estudiante_modalidad_d.xml",
        "report/report_oferta_academica.xml",
        "report/report_oferta_academica_data.xml",
        "security/filtro_oferta_academica.xml",
        "security/access_asistente/ir.model.access.csv",
        "security/access_coordinador/ir.model.access.csv",
        "security/access_estudiante/ir.model.access.csv",
        "security/access_profesor/ir.model.access.csv",
        ],
    'installable': True,
    'auto_install': False,
}
