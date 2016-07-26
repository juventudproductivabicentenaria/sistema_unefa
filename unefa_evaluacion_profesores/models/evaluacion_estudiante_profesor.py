# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp import http,tools, api,SUPERUSER_ID


class unefa_evaluacion_estudiante_docente(osv.osv):
   
    _name ='unefa.evaluacion_estudiante'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name ='carrera_id'

    _columns = {
        'name': fields.char('Evaluación', required=False, copy=False,
            readonly=True,  select=True),
        'state': fields.selection([
                            ('espera', 'En espera'),
                            ('aprobado', 'Aprobado'),
                            ], 'Estado', 
                            readonly=True, 
                            copy=False, 
                            help="", 
                            select=True),
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
                    
        'semestre_id': fields.many2one('unefa.semestre',
                        'Semestre',
                        required=False,
                        readonly=True,
                        ),
        'materia_id': fields.many2one('unefa.asignatura',
                        'Asignatura',
                        required=False,
                        readonly=True,
                        ),
        'seccion_id': fields.many2one('unefa.oferta_academica_seccion',
                        'Sección',
                        required=False,
                        readonly=True,
                        ),
                        
        'profesor_id': fields.many2one('res.users',
                        'Profesor',
                        required=False,
                        readonly=True,
                        ),
                    
        'competencia_profesional_ids': fields.one2many('unefa.evaluacion_competencia_profesional', 'evaluacion_id', required=False,states={'aprobado': [('readonly', True)]}),
        
        'interaccion_docente_estudiante_ids': fields.one2many('unefa.evaluacion_interaccion_docente_estudiante', 'evaluacion_id', required=False,states={'aprobado': [('readonly', True)]}),
        'estrategia_ensenanza_ids': fields.one2many('unefa.evaluacion_estrategia_ensenanza_2', 'evaluacion_id', required=False,states={'aprobado': [('readonly', True)]}),
        'recursos_ids': fields.one2many('unefa.evaluacion_recursos', 'evaluacion_id', required=False,states={'aprobado': [('readonly', True)]}),
        'evaluacion_aprendizaje_ids': fields.one2many('unefa.evaluacion_aprendizajes_2', 'evaluacion_id', required=False,states={'aprobado': [('readonly', True)]}),
        'aspecto_positivo': fields.text('Aspectos Positivos',
                    required=False,
                    states={'aprobado': [('readonly', True)]}
                    ),
        'aspecto_mejorable': fields.text('Aspectos Mejorables',
                    required=False,
                    states={'aprobado': [('readonly', True)]}
                    ),
        'user_id': fields.many2one('unefa.usuario_estudiante','Estudiante', readonly=False,required=True,states={'preinscrito': [('readonly', True)],'inscrito': [('readonly', True)]},),
    }
    
    _order = 'create_date desc, id desc'
    
    _defaults={
        'create_date':fields.datetime.now,
        'name':'N°',
    }
    
    def aprobar_evaluacion (self, cr, uid, ids, context=None):
        coordinacion_obj=self.pool.get('unefa.coordinacion')
        coordinador_obj=self.pool.get('res.users')
        for i in self.browse(cr,uid,ids):
            profesor_id=i.profesor_id.id
            profesor=i.profesor_id.nombre_completo
            turno=i.user_id.regimen
            coordinacion_ids=coordinacion_obj.search(cr,uid,[('carrera_id','=',i.carrera_id.id),('regimen','=',turno)])
            coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_ids)
            coordinador_ids=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_data['id']),('is_coordinador','=',True)])
            coordinador_data=coordinador_obj.browse(cr,uid,coordinador_ids)
            partner_id=coordinador_data['partner_id']['id']
        values={
            'body': 'Ha culminado el proceso de evaluación de un estudiante al profesor '+profesor, 
            'model': 'unefa.evaluacion_estudiante', 
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
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'unefa.evaluacion_estudiante') or 'N°'
        return super(unefa_evaluacion_estudiante_docente, self).create(cr, uid, vals, context=context)

        
class unefa_evaluacion_apreciacion(osv.osv):
   
    _name ='unefa.evaluacion_apreciacion'
    _rec_name ='nombre_aprec'

    _columns = {
        'nombre_aprec': fields.char(
                            'Nombre',
                            required=True,
                            readonly=False,
                        ),
        'valor_apreci': fields.integer(
                            'Valor',
                            required=True,
                            readonly=False,
                            ),
        }


class unefa_evaluacion_competencia_profesional(osv.osv):
   
    _name ='unefa.evaluacion_competencia_profesional'
    _rec_name ='item_evaluar'

    _columns = {
        'evaluacion_id': fields.many2one('unefa.evaluacion_estudiante',
                    'Evaluación',
                    required=False,
                    readonly=True,
                    ),
                    
        'item_evaluar': fields.many2one('unefa.items_competencia_profesional',
                        'Item',
                        required=False,
                        readonly=True,
                        ),
        'apreciacion_id': fields.many2one('unefa.evaluacion_apreciacion',
                        'Apreciación',
                        required=False,
                        readonly=False,
                        ),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la evaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_evaluacion_competencia_profesional, self).create(cr, uid, vals, context=context)
    
    

class unefa_items_competencia_profesional(osv.osv):
   
    _name = 'unefa.items_competencia_profesional'
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
     

class unefa_evaluacion_interaccion_docente_estudiante(osv.osv):
   
    _name ='unefa.evaluacion_interaccion_docente_estudiante'
    _rec_name ='item_evaluar'

    _columns = {
        'evaluacion_id': fields.many2one('unefa.evaluacion_estudiante',
                    'Evaluación',
                    required=False,
                    readonly=True,
                    ),
                    
        'item_evaluar': fields.many2one('unefa.items_interaccion_docente_estudiante_2',
                        'Item',
                        required=False,
                        readonly=True,
                        ),
        'apreciacion_id': fields.many2one('unefa.evaluacion_apreciacion',
                        'Apreciación',
                        required=False,
                        readonly=False,
                        ),
         'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la evaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_evaluacion_interaccion_docente_estudiante, self).create(cr, uid, vals, context=context)
    
    

class unefa_items_interaccion_docente_estudiante(osv.osv):
   
    _name = 'unefa.items_interaccion_docente_estudiante_2'
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
     

class unefa_evaluacion_estrategias_ensenanza(osv.osv):
   
    _name ='unefa.evaluacion_estrategia_ensenanza_2'
    _rec_name ='item_evaluar'

    _columns = {
        'evaluacion_id': fields.many2one('unefa.evaluacion_estudiante',
                    'Evaluación',
                    required=False,
                    readonly=True,
                    ),
                    
        'item_evaluar': fields.many2one('unefa.items_estrategia_ensenanza_2',
                        'Item',
                        required=False,
                        readonly=True,
                        ),
        'apreciacion_id': fields.many2one('unefa.evaluacion_apreciacion',
                        'Apreciación',
                        required=False,
                        readonly=False,
                        ),
         'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la evaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_evaluacion_estrategias_ensenanza, self).create(cr, uid, vals, context=context)
    
    

class unefa_items_interaccion_estrategia_ensenanza(osv.osv):
   
    _name = 'unefa.items_estrategia_ensenanza_2'
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
    
    
    
     
class unefa_evaluacion_recursos(osv.osv):
   
    _name ='unefa.evaluacion_recursos'
    _rec_name ='item_evaluar'

    _columns = {
        'evaluacion_id': fields.many2one('unefa.evaluacion_estudiante',
                    'Evaluación',
                    required=False,
                    readonly=True,
                    ),
                    
        'item_evaluar': fields.many2one('unefa.items_recursos',
                        'Item',
                        required=False,
                        readonly=True,
                        ),
        'apreciacion_id': fields.many2one('unefa.evaluacion_apreciacion',
                        'Apreciación',
                        required=False,
                        readonly=False,
                        ),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la evaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_evaluacion_recursos, self).create(cr, uid, vals, context=context)
    
    

class unefa_items_recursos(osv.osv):
   
    _name = 'unefa.items_recursos'
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
     
     
     
class unefa_evaluacion_aprendizajes(osv.osv):
   
    _name ='unefa.evaluacion_aprendizajes_2'
    _rec_name ='item_evaluar'

    _columns = {
        'evaluacion_id': fields.many2one('unefa.evaluacion_estudiante',
                    'Evaluación',
                    required=False,
                    readonly=True,
                    ),
                    
        'item_evaluar': fields.many2one('unefa.items_aprendizajes_2',
                        'Item',
                        required=False,
                        readonly=True,
                        ),
        'apreciacion_id': fields.many2one('unefa.evaluacion_apreciacion',
                        'Apreciación',
                        required=False,
                        readonly=False,
                        ),
        'state':fields.selection([('espera','En espera'),('aprobado','Aprobado')],'Estatus', help='Estatus de la evaluación'),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'state':'espera',
                })
        return super(unefa_evaluacion_aprendizajes, self).create(cr, uid, vals, context=context)
    
    

class unefa_items_aprendizajes(osv.osv):
   
    _name = 'unefa.items_aprendizajes_2'
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
     

