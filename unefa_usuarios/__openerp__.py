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
    'name': 'Unefa Usuarios',
    'version': '1.0',
    'depends': ['base_setup','unefa_configuracion','unefa_pensum','web_fields_masks'],
    'author': 'Jeison Pernía y Jonathan Reyes',
    'category': '',
    'description': """
    Modulo "usuarios".
    """,
    'update_xml': [],
    "data" : [
        'views/unefa_usuarios_view.xml',
        'report/report_ficha_estudiante.xml',
        'report/report_ficha_estudiante_data.xml',
        'report/report_ficha_profesor.xml',
        'report/repor_ficha_profesor_data.xml',
        'report/report_historial_nota_data.xml',
        'report/report_historial_notas_template.xml',
        'security/filtro_usuarios.xml',
        'security/access_asistente/ir.model.access.csv',
        'security/access_coordinador/ir.model.access.csv',
        'security/access_estudiantes/ir.model.access.csv',
        'security/access_profesores/ir.model.access.csv',
        'data/caracteriscas_prof_d.xml',
        ],
    'installable': True,
    'auto_install': False,
}
