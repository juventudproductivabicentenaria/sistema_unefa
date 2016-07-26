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
    'name': 'Unefa Horarios',
    'version': '1.0',
    'depends': ['base_setup','unefa_configuracion','unefa_pensum','unefa_oferta_academica'],
    'author': 'Jeison Pernía y Jonathan Reyes',
    'category': '',
    'description': """
    Modulo "Horarios".
    """,
    'update_xml': [],
    "data" : [
        'views/unefa_horarios_view.xml',
        'views/crear_horario_t.xml',
        'views/editar_horarios_template.xml',
        'views/consultar_horarios_templete.xml',
        'report/report_horarios_data.xml',
        'report/report_horarios_template.xml',
        'report/report_horarios_data_particular.xml',
        'data/conf_dias_turno_horas_d.xml',
        'security/filtro_horarios.xml',
        'security/access_asistente/ir.model.access.csv',
        'security/access_coordinador/ir.model.access.csv',
        'security/access_estudiantes/ir.model.access.csv',
        'security/access_profesores/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': False,
}
