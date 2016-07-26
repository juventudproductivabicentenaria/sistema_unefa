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
    'name': 'Gestión Semestre',
    'version': '1.0',
    'depends': ['base_setup','unefa_usuarios','unefa_configuracion','unefa_pensum','unefa_planificacion_semestre','unefa_horarios','unefa_oferta_academica','unefa_contenido_programatico'],
    'authors': 'Jeison Pernía y Jonathan Reyes',
    'category': 'Gestión Semestre',
    'description': """
    Pensum académicos
    """,
    'update_xml': [],
    "data" : [
        'views/unefa_gestion_semestre.xml',
        'views/crear_acta_nota_t.xml',
        'views/consultar_acta_nota_t.xml',
        'views/editar_acta_nota_t.xml',
        'wizard/unefa_generar_lista_semestre.xml',
        'report/report_listas_estudiantes_data.xml',
        'report/report_listas_estudiantes_template.xml',
        'report/report_contrato_aprendizaje_data.xml',
        'report/report_contrato_aprendizaje_template.xml',
        'report/report_listas_plan_evaluacion_template.xml',
        'report/report_plan_evaluacion_data.xml',
        'report/report_acta_notas_data.xml',
        'report/report_acta_notas_template.xml',
        'report/report_acta_recuperacion_template.xml',
        'report/report_actas_recuperacion_data.xml',
        'report/report_listas_estudiantes_semestre_template.xml',
        'report/report_listas_estudiantes_semestre_data.xml',
        "security/filtro_gestion_semestre.xml",
        "security/access_asistente/ir.model.access.csv",
        "security/access_coordinador/ir.model.access.csv",
        "security/access_profesor/ir.model.access.csv",
        "security/access_estudiante/ir.model.access.csv",
        
        ],
    'installable': True,
    'auto_install': False,
}

