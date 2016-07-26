# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp import http,tools, api,SUPERUSER_ID

class unefa_autoevaluacion_docente(osv.osv):
   
    _name ='unefa.autoevaluacion_docente'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name ='profesor_id'
    
    def get_select_porcentaje(desde,hasta):
        porc=[]
        for i in range(desde,hasta):
            porc.append((str(i),str(i)))
        return porc
    
    def default_usuarios(self, cr, uid, ids, context=None):
        profesores_obj=self.pool.get('res.users')
        profesores_ids=profesores_obj.search(cr,uid,[('id','=',uid)],context=context)
        profesores_datos=profesores_obj.browse(cr,uid,profesores_ids,context=context)
        return profesores_datos['id']

    _columns = {
        'name': fields.char('Autoevaluación', required=False, copy=False,
            readonly=True,  select=True),
        'profesor_id': fields.many2one('res.users',
                    'Profesor',
                    required=False,
                    readonly=True,
                    ),
        
        'periodo_id': fields.many2one('unefa.conf.periodo_academico',
                    'Periodo Académico',
                    required=False,
                    readonly=True,
                    ),
                    
        'carrera_id': fields.many2one('unefa.carrera',
                    'Carrera',
                    required=False,
                    readonly=True,
                    ),
                    
        'materia_id':fields.many2one('unefa.asignatura',
                    'Asignatura',
                    required=False,
                    readonly=True,
                    ),
        'n_secciones_asignadas': fields.integer('N° Secciones Asignadas',
                    required=False,
                    readonly=True,
                    ),
        'seccion_evaluada':fields.many2one('unefa.oferta_academica_seccion',
                    'Sección Evaluada',
                    required=False,
                     readonly=True,
                    ),
        'coordinador_id': fields.many2one('unefa.usuario_coordinador',
                    'Coordinador',
                    required=False,
                    readonly=True,
                    ),
        'asistencia_puntualidad_ids': fields.one2many('unefa.asis_puntualidad', 'asistencia_puntualidad_id','asistencia', required=True, states={'aprobado': [('readonly', True)]},),
        
        'planif_registro_control_ids': fields.one2many('unefa.planificacion_registro_control', 'planif_registro_control_id','Planificacion', required=True, states={'aprobado': [('readonly', True)]}),
        'interaccion_doce_estu_ids': fields.one2many('unefa.interaccion_docente_estudiante', 'interac_docente_estudiante_id','Interacción', required=True, states={'aprobado': [('readonly', True)]}),
        'praxis_academica_ids': fields.one2many('unefa.praxis_academica', 'praxis_academica_id','Praxis', required=True, states={'aprobado': [('readonly', True)]}),
        'estrategias_ense_ids': fields.one2many('unefa.estrategia_ensenanza', 'estrat_ensen_id','Estrategias', required=True, states={'aprobado': [('readonly', True)]}),
        'recursos_didacticos': fields.one2many('unefa.recur_didacticos', 'recursos_didacticos_id','Recursos Didacticos', required=True, states={'aprobado': [('readonly', True)]}),
        'evaluacion_aprendizaje_ids': fields.one2many('unefa.eval_aprendizaje', 'eval_aprendizaje_id','Evaluación', required=True, states={'aprobado': [('readonly', True)]}),
        'aspecto_positivo': fields.text('Aspectos Positivos',
                    required=False,
                    states={'aprobado': [('readonly', True)]},
                    ),
        'aspectos_cambiar': fields.text('Aspectos Positivos',
                    required=False,
                    states={'aprobado': [('readonly', True)]},
                    ),
        'aspectos_mejoras': fields.text('Aspectos Positivos',
                    required=False,
                    states={'aprobado': [('readonly', True)]},
                    ),
        'califi_personal': fields.text('Aspectos Positivos',
                    required=False,
                    states={'aprobado': [('readonly', True)]},
                    ),
        'calificacion': fields.selection(
                    get_select_porcentaje(1,21),
                    'Calificación', select=True,
                    states={'aprobado': [('readonly', True)]},),
                    
        'comentarios_adic': fields.text('Comentarios Adicionales',
                    required=False,
                    states={'aprobado': [('readonly', True)]},
                    ),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la autoevaluación'),

        
    }
    _order = 'create_date desc, id desc'
    
    _defaults={
        'name':'N°',
    }
    
    def aprobar_autoevaluacion(self,cr,uid,ids,context=None):
        for i in self.browse(cr,uid,ids):
            profesor_id=i.profesor_id.id
            profesor=i.profesor_id.nombre_completo
            partner_id=i.coordinador_id.partner_id.id
        values={
            'body': 'El Profesor '+profesor+' ha culminado su proceso de Autoevaluación.', 
            'model': 'unefa.autoevaluacion_docente', 
            'res_id': ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, [partner_id]]], 
            'subject': False}
        mail_message_obj=self.pool.get('mail.message')
        mail_message_obj.create(cr,SUPERUSER_ID,values)
        return self.write(cr,uid,ids,{'state':'aprobado'})
    
    
    
    
    def create(self,cr,uid,vals,context=None):
        if vals.get('Aviso', 'N°') == 'N°':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'unefa.autoevaluacion_docente') or 'N°'
        #~ res=self.onchange_cargar_datos_profesor(cr, uid, [], context=None)
        #~ res=res.values()
        #~ res=res[0]
        return super(unefa_autoevaluacion_docente, self).create(cr, uid, vals, context=context)
        #~ self.write(cr,uid,h,res,context=context)
        #~ return h

    
    
    
   
class unefa_asis_puntualidad(osv.osv):
   
    _name = 'unefa.asis_puntualidad'
    _rec_name = 'items_evaluacion'

    _columns = {
        
        'asistencia_puntualidad_id': fields.many2one('unefa.autoevaluacion_docente', 'Autoevaluación',),
        'items_evaluacion': fields.many2one('unefa.items_asis_puntualidad', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.selection([
                    ('nunca', 'Nunca'),
                    ('algunas', 'Algunas Veces'),
                    ('casi', 'Casi Siempre'),
                    ('siempre', 'Siempre'),
            ], 'Evaluación', readonly=False,required=False, select=True),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la autoevaluación'),
        }

    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_asis_puntualidad, self).create(cr, uid, vals, context=context)
        

class unefa_items_asis_puntualidad(osv.osv):
   
    _name = 'unefa.items_asis_puntualidad'
    _rec_name = 'item_evaluacion'

    _columns = {
        
        'item_evaluacion': fields.char('Item de evaluación',
                    required=True,
                    help="",
                    ),
        'item_activo': fields.boolean('Item Activo',
                        help="",
                    ),
    }
    
    _defaults={
        'item_activo':True,
    }

  
    
class unefa_planificacion_registro_control(osv.osv):
   
    _name = 'unefa.planificacion_registro_control'
    _rec_name = 'items_evaluacion'

    _columns = {
         
        'planif_registro_control_id': fields.many2one('unefa.autoevaluacion_docente', 'Autoevaluación',),
        'items_evaluacion': fields.many2one('unefa.items_planificacion_registro_control', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.selection([
                    ('nunca', 'Nunca'),
                    ('algunas', 'Algunas Veces'),
                    ('casi', 'Casi Siempre'),
                    ('siempre', 'Siempre'),
            ], 'Evaluación', readonly=False,required=False, select=True),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la autoevaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_planificacion_registro_control, self).create(cr, uid, vals, context=context)
        

class unefa_items_planif_registro_control(osv.osv):
   
    _name = 'unefa.items_planificacion_registro_control'
    _rec_name = 'item_evaluacion'

    _columns = {
        
        'item_evaluacion': fields.char('Item de evaluación',
                    required=True,
                    help="",
                    ),
        'item_activo': fields.boolean('Item Activo',
                        help="",
                    ),
    }
    
    _defaults={
        'item_activo':True,
    }
    
    
    
class unefa_interaccion_docente_estudiante(osv.osv):
   
    _name = 'unefa.interaccion_docente_estudiante'
    _rec_name = 'items_evaluacion'

    _columns = {
 
        'interac_docente_estudiante_id': fields.many2one('unefa.autoevaluacion_docente', 'Autoevaluación',),
        'items_evaluacion': fields.many2one('unefa.items_interaccion_docente_estudiante', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.selection([
                    ('nunca', 'Nunca'),
                    ('algunas', 'Algunas Veces'),
                    ('casi', 'Casi Siempre'),
                    ('siempre', 'Siempre'),
            ], 'Evaluación', readonly=False,required=False, select=True),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la autoevaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_interaccion_docente_estudiante, self).create(cr, uid, vals, context=context)
        

class unefa_items_planif_registro_control(osv.osv):
   
    _name = 'unefa.items_interaccion_docente_estudiante'
    _rec_name = 'item_evaluacion'

    _columns = {
        
        'item_evaluacion': fields.char('Item de evaluación',
                    required=True,
                    help="",
                    ),
        'item_activo': fields.boolean('Item Activo',
                        help="",
                    ),
    }
    
    _defaults={
        'item_activo':True,
    }
    
class unefa_praxis_academica(osv.osv):
   
    _name = 'unefa.praxis_academica'
    _rec_name = 'items_evaluacion'

    _columns = {

        'praxis_academica_id': fields.many2one('unefa.autoevaluacion_docente', 'Autoevaluación',),
        'items_evaluacion': fields.many2one('unefa.items_praxis_academica', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.selection([
                    ('nunca', 'Nunca'),
                    ('algunas', 'Algunas Veces'),
                    ('casi', 'Casi Siempre'),
                    ('siempre', 'Siempre'),
            ], 'Evaluación', readonly=False,required=False, select=True),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la autoevaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_praxis_academica, self).create(cr, uid, vals, context=context)
        

class unefa_items_praxis_academica(osv.osv):
   
    _name = 'unefa.items_praxis_academica'
    _rec_name = 'item_evaluacion'

    _columns = {
        
        'item_evaluacion': fields.char('Item de evaluación',
                    required=True,
                    help="",
                    ),
        'item_activo': fields.boolean('Item Activo',
                        help="",
                    ),
    }
    
    _defaults={
        'item_activo':True,
    }
    
    
    
class unefa_estrategia_ensenanza(osv.osv):
   
    _name = 'unefa.estrategia_ensenanza'
    _rec_name = 'items_evaluacion'

    _columns = {
        

        'estrat_ensen_id': fields.many2one('unefa.autoevaluacion_docente', 'Autoevaluación',),
        'items_evaluacion': fields.many2one('unefa.items_estrategia_ensenanza', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.selection([
                    ('nunca', 'Nunca'),
                    ('algunas', 'Algunas Veces'),
                    ('casi', 'Casi Siempre'),
                    ('siempre', 'Siempre'),
            ], 'Evaluación', readonly=False,required=False, select=True),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la autoevaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_estrategia_ensenanza, self).create(cr, uid, vals, context=context)
        

class unefa_items_estrategia_ensenanza(osv.osv):
   
    _name = 'unefa.items_estrategia_ensenanza'
    _rec_name = 'item_evaluacion'

    _columns = {
        
        'item_evaluacion': fields.char('Item de evaluación',
                    required=True,
                    help="",
                    ),
        'item_activo': fields.boolean('Item Activo',
                        help="",
                    ),
    }
    
    _defaults={
        'item_activo':True,
    }
    
    
class unefa_recur_didacticos(osv.osv):
   
    _name = 'unefa.recur_didacticos'
    _rec_name = 'items_evaluacion'

    _columns = {
         
        'recursos_didacticos_id': fields.many2one('unefa.autoevaluacion_docente', 'Autoevaluación',),
        'items_evaluacion': fields.many2one('unefa.items_recur_didacticos', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.selection([
                    ('nunca', 'Nunca'),
                    ('algunas', 'Algunas Veces'),
                    ('casi', 'Casi Siempre'),
                    ('siempre', 'Siempre'),
            ], 'Evaluación', readonly=False,required=False, select=True),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la autoevaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_recur_didacticos, self).create(cr, uid, vals, context=context)
        

class unefa_items_recur_didacticos(osv.osv):
   
    _name = 'unefa.items_recur_didacticos'
    _rec_name = 'item_evaluacion'

    _columns = {
        
        'item_evaluacion': fields.char('Item de evaluación',
                    required=True,
                    help="",
                    ),
        'item_activo': fields.boolean('Item Activo',
                        help="",
                    ),
    }
    
    _defaults={
        'item_activo':True,
    }
    
    
class unefa_eval_aprendizaje(osv.osv):
   
    _name = 'unefa.eval_aprendizaje'
    _rec_name = 'items_evaluacion'

    _columns = {
        
        'eval_aprendizaje_id': fields.many2one('unefa.autoevaluacion_docente', 'Autoevaluación',),
        'items_evaluacion': fields.many2one('unefa.items_eval_aprendizaje', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.selection([
                    ('nunca', 'Nunca'),
                    ('algunas', 'Algunas Veces'),
                    ('casi', 'Casi Siempre'),
                    ('siempre', 'Siempre'),
            ], 'Evaluación', readonly=False,required=False, select=True),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la autoevaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_eval_aprendizaje, self).create(cr, uid, vals, context=context)
        

class unefa_items_eval_aprendizaje(osv.osv):
   
    _name = 'unefa.items_eval_aprendizaje'
    _rec_name = 'item_evaluacion'

    _columns = {
        
        'item_evaluacion': fields.char('Item de evaluación',
                    required=True,
                    help="",
                    ),
        'item_activo': fields.boolean('Item Activo',
                        help="",
                    ),
    }
    
    _defaults={
        'item_activo':True,
    }


