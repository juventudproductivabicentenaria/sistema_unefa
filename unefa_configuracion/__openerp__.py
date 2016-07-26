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
    'name':'Unefa Configuración',
    'version': '1.0',
    'depends': ['base_setup','base','website_apiform'],
    'author': 'IRP unefa (Comunidad Bachaco.ve)',
    'category': '',
    'description': """

    Modulo de configuración de la UNEFA

    """,
    'update_xml': [],
    "data" : [
        "views/menu_views.xml",
        "views/redis.xml",
        "views/estados.xml",
        "views/municipios.xml",
        "views/parroquias.xml",
        "views/region_defensa_integral_view.xml",
        "views/cantidad_estudiantes.xml",
        "views/cantidad_unidades_credito.xml",
        "views/res_company.xml",
        "views/nucleo_views.xml",
        "views/carrera_views.xml",
        "views/coordinacion_views.xml",
        "views/pisos_views.xml",
        "views/aulas_views.xml",
        "views/fuerza_grado_militar.xml",
        "report/report_lista_general_estudiantes_data.xml",
        "report/report_listas_generales_estudiantes.xml",
        #~ "security/filtro_coordinacion.xml",
        "security/unefa_roles.xml",
        "security/access_asistente/ir.model.access.csv",
        "security/access_coordinador/ir.model.access.csv",
        "security/access_estudiante/ir.model.access.csv",
        "security/access_profesor/ir.model.access.csv",
        "data/unefa_redis_d.xml",
        "data/data_estados.xml",
        "data/data_municipios.xml",
        "data/data_parroquias.xml",
        "data/universidad_data.xml",
        "data/area_cnmto_carrera_d.xml",
        "data/cordinacion_data.xml",
        "data/fuerza_grado_militar_data.xml",
        "data/cant_estudiantes_cant_uc.xml",
        #~ "data/universidad_data.xml",
        #~ "data/data_estados.xml",
        #~ "data/data_municipios.xml",
        #~ "data/data_parroquias.xml",
        ],
    'installable': True,
    'auto_install': False,
}
