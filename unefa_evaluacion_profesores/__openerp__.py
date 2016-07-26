# -*- coding: utf-8 -*-

{
    'name': 'Unefa Evaluación Profesores',
    'version': '1.0',
    'depends': ['base','unefa_configuracion','unefa_pensum','unefa_usuarios','unefa_planificacion_semestre','unefa_inscripcion','mail'],
    'author': 'Nancy Castellanos',
    'category': 'Configuración',
    'description': """
            Módulo de supervisión y evaluación del personal docente
            """,
    'update_xml': [],
    "data" : [
        'views/supervision_clase_view.xml',
        'views/autoevaluacion_docente_view.xml',
        'views/autoevaluacion_docente_sequence .xml',
        'views/supervision_clase_sequence.xml',
        'views/unefa_evaluacion_estudiante_profesores_v.xml',
        'views/evaluacion_estudiante_docente_sequence.xml',
        'data/supervision_data.xml',
        'data/valor_supervision_data.xml',
        'data/autoevaluacion_data.xml',
        'data/apreciacion_evaluacion_estudiante_docprofesor_data.xml',
        'data/evaluacion_estudiante_profesor_data.xml',
        #~ 'security/group_unefa_admin/ir.model.access.csv',
        'security/group_unefa_coor/ir.model.access.csv',
        'security/group_unefa_est/ir.model.access.csv',
        #~ 'security/group_unefa_eval/ir.model.access.csv',
        'security/group_unefa_prof/ir.model.access.csv',
        'security/group_unefa_secret/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': False,
}

