# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp import http,tools, api,SUPERUSER_ID

class unefa_supervision_clase(osv.osv):
   
    _name ='unefa.supervision.clase'
    _rec_name ='profesor_id'
    
    def calculo_sub_total_planif(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        suma=0
        for i in self.browse(cr,uid,ids):
            for n in i.planif_registro_control_ids:
                eval_planif_registro_control_obj=self.pool.get('unefa.eval.planif.registro_control')
                eval_planif_registro_control_ids=eval_planif_registro_control_obj.search(cr,uid,[('id','=',int(n.evaluacion))],context=context)
                eval_planif_registro_control_datos=eval_planif_registro_control_obj.browse(cr,uid,eval_planif_registro_control_ids,context=context)
                suma+=eval_planif_registro_control_datos['valor_opcion']
        res[i.id]=suma,
        for a in res[i.id]:
            res[i.id]=a
        return res
        
    def calculo_sub_total_asis(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        suma=0
        for i in self.browse(cr,uid,ids):
            for n in i.asistencia_puntualidad_ids:
                eval_asistencia_puntualidad_obj=self.pool.get('unefa.eval.asistencia.puntualidad')
                eval_asistencia_puntualidad_ids=eval_asistencia_puntualidad_obj.search(cr,uid,[('id','=',int(n.evaluacion))],context=context)
                eval_asistencia_puntualidad_datos=eval_asistencia_puntualidad_obj.browse(cr,uid,eval_asistencia_puntualidad_ids,context=context)
                suma+=eval_asistencia_puntualidad_datos['valor_opcion']
        res[i.id]=suma,
        for a in res[i.id]:
            res[i.id]=a
        return res
        
    def calculo_sub_total_inicio(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        suma=0
        for i in self.browse(cr,uid,ids):
            for n in i.inicio_clase_ids:
                eval_inicio_clase_obj=self.pool.get('unefa.eval.inicio.clase')
                eval_inicio_clase_ids=eval_inicio_clase_obj.search(cr,uid,[('id','=',int(n.evaluacion))],context=context)
                eval_inicio_clase_datos=eval_inicio_clase_obj.browse(cr,uid,eval_inicio_clase_ids,context=context)
                suma+=eval_inicio_clase_datos['valor_opcion']
        res[i.id]=suma,
        for a in res[i.id]:
            res[i.id]=a
        return res
        
    def calculo_sub_total_desarrollo(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        suma=0
        for i in self.browse(cr,uid,ids):
            for n in i.desarrollo_clase_ids:
                eval_desarrollo_clase_obj=self.pool.get('unefa.eval.desarrollo.clase')
                eval_desarrollo_clase_ids=eval_desarrollo_clase_obj.search(cr,uid,[('id','=',int(n.evaluacion))],context=context)
                eval_desarrollo_clase_datos=eval_desarrollo_clase_obj.browse(cr,uid,eval_desarrollo_clase_ids,context=context)
                suma+=eval_desarrollo_clase_datos['valor_opcion']
        res[i.id]=suma,
        for a in res[i.id]:
            res[i.id]=a
        return res
        
    def calculo_sub_total_recursos(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        suma=0
        for i in self.browse(cr,uid,ids):
            for n in i.recursos_didacticos_ids:
                eval_recursos_didacticos_obj=self.pool.get('unefa.eval.recursos.didacticos')
                eval_recursos_didacticos_ids=eval_recursos_didacticos_obj.search(cr,uid,[('id','=',int(n.evaluacion))],context=context)
                eval_recursos_didacticos_datos=eval_recursos_didacticos_obj.browse(cr,uid,eval_recursos_didacticos_ids,context=context)
                suma+=eval_recursos_didacticos_datos['valor_opcion']
        res[i.id]=suma,
        for a in res[i.id]:
            res[i.id]=a
        return res
        
    def calculo_sub_total_cierre(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        suma=0
        for i in self.browse(cr,uid,ids):
            for n in i.cierre_clase_ids:
                eval_cierre_clase_obj=self.pool.get('unefa.eval.cierre.clase')
                eval_cierre_clase_ids=eval_cierre_clase_obj.search(cr,uid,[('id','=',int(n.evaluacion))],context=context)
                eval_cierre_clase_datos=eval_cierre_clase_obj.browse(cr,uid,eval_cierre_clase_ids,context=context)
                suma+=eval_cierre_clase_datos['valor_opcion']
        res[i.id]=suma,
        for a in res[i.id]:
            res[i.id]=a
        return res
        
    def calculo_total(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        total=0
        for i in self.browse(cr,uid,ids):
            total=i.subtotal_planif+i.subtotal_asis+i.subtotal_inicio+i.subtotal_desarrollo+i.subtotal_cierre
        res[i.id]=total,
        for a in res[i.id]:
            res[i.id]=a
        return res
    
    def default_usuarios_coordinador(self, cr, uid, ids, context=None):
        coordinador_obj=self.pool.get('unefa.usuario_coordinador')
        coordinador_ids=coordinador_obj.search(cr,uid,[('user_id','=',uid)])
        coordinador_data=coordinador_obj.browse(cr,uid,coordinador_ids)
        if coordinador_data['is_coordinador']==True:
            return coordinador_ids[0]
    
    _columns = {
        'name': fields.char('Evaluación', required=False, copy=False,
            readonly=True,  select=True),
        'profesor_id': fields.many2one('res.users',
                    'Profesor',
                    required=True,
                    states={'publicado': [('readonly', True)]}
                    ),
        'periodo_id': fields.many2one('unefa.conf.periodo_academico',
                    'Periodo Académico',
                    required=True,
                    readonly=False,
                    ),
        'carrera_id': fields.many2one('unefa.carrera',
                    'Carrera',
                    required=False,
                    readonly=True,
                    ),
        'materia_id': fields.many2one('unefa.asignatura',
                    'Asignatura',
                    required=True,
                    readonly=False,
                    states={'publicado': [('readonly', True)]}
                    ),
        'coordinador_id': fields.many2one('unefa.usuario_coordinador',
                    'Coordinador',
                    required=False,
                    readonly=True,
                    ),
        'seccion_id': fields.many2one('unefa.oferta_academica_seccion',
                    'Sección',
                    required=True,
                    readonly=False,
                    states={'publicado': [('readonly', True)]}
                    ),
        'contenido_id': fields.many2one('unefa.contenido_unidad',
                    'Contenido',
                    required=True,
                    readonly=False,
                    states={'publicado': [('readonly', True)]}
                    ),
        'estudiantes_inscritos': fields.integer('Estudiantes Inscritos',
                    required=False,readonly=True,
                    ),
        'estudiantes_presentes': fields.integer('Estudiantes Presentes',
                    required=True,
                    states={'publicado': [('readonly', True)]}
                    ),
        'tipo': fields.selection([
                ('teorica', 'Teorica'),
                ('practica', 'Practica'),
                ('teorica_practica', 'Teorica Practica'),
                ], 'Tipo de clase',  help="", select=True,states={'publicado': [('readonly', True)]}),
        'planif_registro_control_ids': fields.one2many('unefa.planif.registro.control', 'supervision_clase_id', required=True,states={'publicado': [('readonly', True)]}),
        'asistencia_puntualidad_ids': fields.one2many('unefa.asistencia.puntualidad', 'supervision_clase_id', required=True,states={'publicado': [('readonly', True)]}),
        'inicio_clase_ids': fields.one2many('unefa.inicio.clase', 'supervision_clase_id', required=True,states={'publicado': [('readonly', True)]}),
        'desarrollo_clase_ids': fields.one2many('unefa.desarrollo.clase', 'supervision_clase_id', required=True,states={'publicado': [('readonly', True)]}),
        'recursos_didacticos_ids': fields.one2many('unefa.recursos.didacticos', 'supervision_clase_id', required=True,states={'publicado': [('readonly', True)]}),
        'cierre_clase_ids': fields.one2many('unefa.cierre.clase', 'supervision_clase_id', required=True,states={'publicado': [('readonly', True)]}),
        'cualidades_sobresalientes': fields.text('Cualidades Sobresalientes del Profesor',
                    required=False,
                    states={'publicado': [('readonly', True)]}
                    ),
        'cualidades_mejorables': fields.text('Cualidades Mejorables del Profesor',
                    required=False,
                    states={'publicado': [('readonly', True)]}
                    ),
        'observaciones_profesor': fields.text('Observaciones del Profesor',
                    required=False,
                    states={'publicado': [('readonly', True)]}
                    ),
        'subtotal_planif':fields.function(
                        calculo_sub_total_planif,
                        string="Subtotal",
                        type='integer',
                        states={'publicado': [('readonly', True)]},
                        help=''),
        'subtotal_asis':fields.function(
                        calculo_sub_total_asis,
                        string="Subtotal",
                        type='integer',
                        states={'publicado': [('readonly', True)]},
                        help=''),
        'subtotal_inicio':fields.function(
                        calculo_sub_total_inicio,
                        string="Subtotal",
                        type='integer',
                        states={'publicado': [('readonly', True)]},
                        help=''),
        'subtotal_desarrollo':fields.function(
                        calculo_sub_total_desarrollo,
                        string="Subtotal",
                        type='integer',
                        states={'publicado': [('readonly', True)]},
                        help=''),
        'subtotal_recursos':fields.function(
                        calculo_sub_total_recursos,
                        string="Subtotal",
                        type='integer',
                        states={'publicado': [('readonly', True)]},
                        help=''),
        'subtotal_cierre':fields.function(
                        calculo_sub_total_cierre,
                        string="Subtotal",
                        type='integer',
                        states={'publicado': [('readonly', True)]},
                        help=''),
        'total_evalu':fields.function(
                        calculo_total,
                        string="Total",
                        type='integer',
                        states={'publicado': [('readonly', True)]},
                        help=''),
        'state':fields.selection([('borrador','Borrador'),('publicado','Publicado')],'Estatus', help='Estatus de la supervisión'),
    }
    
    _sql_constraints = [
        ('supervision_uniq', 'unique(profesor_id,periodo_id,materia_id)', 'Ya tiene un registro para éste profesor y esta asignatura.')
        ]
    
    _defaults={
        'create_date':fields.datetime.now,
        #~ 'periodo_id':lambda self, cr, uid, context: self.pool.get('unefa.conf.periodo_academico').periodo_activo(cr,uid,[],context),
        'coordinador_id':default_usuarios_coordinador,
        'name':'N°',
    }
    
    _order = 'create_date desc, id desc'
    
    def publicar_supervision(self,cr,uid,ids,context=None):
        self.generar_registro_autoevaluacion(cr,uid,ids)
        self.generar_registro_evaluacion_estudiante(cr,uid,ids)
        return self.write(cr,uid,ids,{'state':'publicado'})
        
    def generar_registro_evaluacion_estudiante(self,cr,uid,ids,context=None):
        inscripcion_obj=self.pool.get('unefa.inscripcion_asignatura')
        list_estudiantes=[]
        list_partners=[]
        for i in self.browse(cr,uid,ids):
            profesor=i.profesor_id.nombre_completo
            periodo_id=i.periodo_id.id
            carrera_id=i.carrera_id.id
            profesor_id=i.profesor_id.id
            inscripcion_ids=inscripcion_obj.search(cr,uid,[('periodo_id','=',periodo_id)])
            inscripcion_data=inscripcion_obj.browse(cr,uid,inscripcion_ids)
            for ins in inscripcion_data:
                for asig in ins.asignaturas_inscritas_ids:
                    semestre_id=asig.semestre_id.id
                    seccion_id=asig.seccion_id.id
                    if asig.asignatura_id==i.materia_id and i.seccion_id == asig.seccion_id:
                        list_estudiantes.append(ins.user_id.id)
                        list_partners.append(ins.user_id.partner_id.id)
                        asignatura_id=asig.asignatura_id.id
        
        item_competencia_profesional_obj=self.pool.get('unefa.items_competencia_profesional')
        item_competencia_profesional_ids=item_competencia_profesional_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_competencia_profesional_datos=item_competencia_profesional_obj.browse(cr,uid,item_competencia_profesional_ids,context=context)
        item_interaccion_docente_estudiante_obj=self.pool.get('unefa.items_interaccion_docente_estudiante_2')
        item_interaccion_docente_estudiante_ids=item_interaccion_docente_estudiante_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_interaccion_unefa_estudiante_datos=item_interaccion_docente_estudiante_obj.browse(cr,uid,item_interaccion_docente_estudiante_ids,context=context)
        item_estrategia_ensenanza_obj=self.pool.get('unefa.items_estrategia_ensenanza_2')
        item_estrategia_ensenanza_ids=item_estrategia_ensenanza_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_estrategia_ensenanza_datos=item_estrategia_ensenanza_obj.browse(cr,uid,item_estrategia_ensenanza_ids,context=context)
        item_recursos_obj=self.pool.get('unefa.items_recursos')
        item_recursos_ids=item_recursos_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_recursos_datos=item_recursos_obj.browse(cr,uid,item_recursos_ids,context=context)
        item_aprendizaje_obj=self.pool.get('unefa.items_aprendizajes_2')
        item_aprendizaje_ids=item_aprendizaje_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_aprendizaje_datos=item_aprendizaje_obj.browse(cr,uid,item_aprendizaje_ids,context=context)
        items_compent=[]
        items_interac=[]
        items_estrateg=[]
        items_recur=[]
        items_aprendizaje=[]
        for i in item_competencia_profesional_datos:
            items_compent.append([0,False,{'item_evaluar':i.id }])
        for i in item_interaccion_unefa_estudiante_datos:
            items_interac.append([0,False,{'item_evaluar':i.id }])
        for i in item_estrategia_ensenanza_datos:
            items_estrateg.append([0,False,{'item_evaluar':i.id }])
        for i in item_recursos_datos:
            items_recur.append([0,False,{'item_evaluar':i.id }])
        for i in item_aprendizaje_datos:
            items_aprendizaje.append([0,False,{'item_evaluar':i.id }])
        
        
        evaluacion_estudiante_obj=self.pool.get('unefa.evaluacion_estudiante')
        mail_message_obj=self.pool.get('mail.message')
        cont=0
        for estudiante in list_estudiantes:
            val={
            'state':'espera',
            'periodo_id':periodo_id,
            'carrera_id':carrera_id,
           'competencia_profesional_ids':items_compent,
            'interaccion_docente_estudiante_ids':items_interac,
            'estrategia_ensenanza_ids':items_estrateg,
            'recursos_ids':items_recur,
            'evaluacion_aprendizaje_ids':items_aprendizaje,
            'semestre_id':semestre_id,
            'materia_id':asignatura_id,
            'seccion_id':seccion_id,
            'profesor_id':profesor_id,
            'user_id':estudiante,
            }
            evaluacion_id=evaluacion_estudiante_obj.create(cr,SUPERUSER_ID,val)
            
            
        
        
       
            values={
                'body': 'Evaluación para el profesor a la espera de ser completada.', 
                'model': 'unefa.evaluacion_estudiante', 
                'res_id': evaluacion_id, 
                'parent_id': False, 
                'subtype_id': False, 
                'author_id': uid, 
                'type': 'notification', 
                'notified_partner_ids': [[6, False, list_partners]], 
                'subject': False}
            
            mail_message_obj.create(cr,SUPERUSER_ID,values)
            cont+=1
            

            
        return True
        
        
    def generar_registro_autoevaluacion(self,cr,uid,ids,context=None):
        list_seccion=[]
        for i in self.browse(cr,uid,ids):
            partner_id=i.profesor_id.partner_id.id
            profesor=i.profesor_id.nombre_completo
            profesor_id=i.profesor_id.id
            profesores_obj=self.pool.get('res.users')
            profesores_ids=profesores_obj.search(cr,uid,[('id','=',int(profesor_id))],context=context)
            profesores_datos=profesores_obj.browse(cr,uid,profesores_ids,context=context)
            turno=''
            if profesores_datos['is_profesor'] == True:
                turno=profesores_datos['regimen']
            if profesores_datos['is_coordinador'] == True or profesores_datos['is_asistente']:
                turno=profesores_datos['coordinacion_id']['regimen']
            periodo_id=i.periodo_id.id
            coordinador_id=i.coordinador_id.id
            carrera_id=i.carrera_id.id
            asignatura_id=i.materia_id.id
            seccion_id=i.seccion_id.id
            oferta_obj=self.pool.get('unefa.oferta_academica')
            oferta_ids=oferta_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('periodo_id','=',int(periodo_id)),('turno','=',turno)],context=context)
            oferta_datos=oferta_obj.browse(cr,uid,oferta_ids,context=context)
            list_seccion=[]
            for oferta in oferta_datos:
                for pensum in oferta.pensum_ids:
                    for semestre in pensum.semestres_ids:
                        for seccion in semestre.secciones_ids:
                            for asignatura in seccion.asignaturas_ids:
                                if int(asignatura.profesor_id)==profesor_id:
                                    list_seccion.append(seccion.id)
            secciones_asignadas=len(list_seccion)
            
        autoevaluacion_obj=self.pool.get('unefa.autoevaluacion_docente')
        
        item_asis_puntualidad_obj=self.pool.get('unefa.items_asis_puntualidad')
        item_asis_puntualidad_ids=item_asis_puntualidad_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_asis_puntualidad_datos=item_asis_puntualidad_obj.browse(cr,uid,item_asis_puntualidad_ids,context=context)
        
        item_planificacion_registro_control_obj=self.pool.get('unefa.items_planificacion_registro_control')
        item_planificacion_registro_control_ids=item_planificacion_registro_control_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_planificacion_registro_control_datos=item_planificacion_registro_control_obj.browse(cr,uid,item_planificacion_registro_control_ids,context=context)
       
        item_interaccion_docente_estudiante_obj=self.pool.get('unefa.items_interaccion_docente_estudiante')
        item_interaccion_docente_estudiante_ids=item_interaccion_docente_estudiante_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_interaccion_docente_estudiante_datos=item_interaccion_docente_estudiante_obj.browse(cr,uid,item_interaccion_docente_estudiante_ids,context=context)
        
        
        item_praxis_academica_obj=self.pool.get('unefa.items_praxis_academica')
        item_praxis_academica_ids=item_praxis_academica_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_praxis_academica_datos=item_praxis_academica_obj.browse(cr,uid,item_praxis_academica_ids,context=context)
       
        item_estrategia_ensenanza_obj=self.pool.get('unefa.items_estrategia_ensenanza')
        item_estrategia_ensenanza_ids=item_estrategia_ensenanza_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_estrategia_ensenanza_datos=item_estrategia_ensenanza_obj.browse(cr,uid,item_estrategia_ensenanza_ids,context=context)
        
        item_recursos_didacticos_obj=self.pool.get('unefa.items_recur_didacticos')
        item_recursos_didacticos_ids=item_recursos_didacticos_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_recursos_didacticos_datos=item_recursos_didacticos_obj.browse(cr,uid,item_recursos_didacticos_ids,context=context)
        
        item_eval_aprendizaje_obj=self.pool.get('unefa.items_eval_aprendizaje')
        item_eval_aprendizaje_ids=item_eval_aprendizaje_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_eval_aprendizaje_datos=item_eval_aprendizaje_obj.browse(cr,uid,item_eval_aprendizaje_ids,context=context)
        
        items_asis_punt=[]
        items_planif=[]
        items_interac=[]
        items_praxis=[]
        items_estrat=[]
        items_recur=[]
        items_eval=[]
        for i in item_asis_puntualidad_datos:
            items_asis_punt.append([0,False,{'items_evaluacion':i.id }])
        for i in item_planificacion_registro_control_datos:
            items_planif.append([0,False,{'items_evaluacion':i.id }])
        for i in item_interaccion_docente_estudiante_datos:
            items_interac.append([0,False,{'items_evaluacion':i.id }])
        for i in item_praxis_academica_datos:
            items_praxis.append([0,False,{'items_evaluacion':i.id }])
        for i in item_estrategia_ensenanza_datos:
            items_estrat.append([0,False,{'items_evaluacion':i.id }])
        for i in item_recursos_didacticos_datos:
            items_recur.append([0,False,{'items_evaluacion':i.id }])
        for i in item_eval_aprendizaje_datos:
            items_eval.append([0,False,{'items_evaluacion':i.id }])
        
        val={
            'profesor_id':profesor_id,
            'periodo_id':periodo_id,
            'carrera_id':carrera_id,
            'materia_id':asignatura_id,
            'n_secciones_asignadas':secciones_asignadas,
            'seccion_evaluada':seccion_id,
            'coordinador_id':coordinador_id,
            'asistencia_puntualidad_ids':items_asis_punt,
            'planif_registro_control_ids':items_planif,
            'interaccion_doce_estu_ids':items_interac,
            'praxis_academica_ids':items_praxis,
            'estrategias_ense_ids':items_estrat,
            'recursos_didacticos':items_recur,
            'evaluacion_aprendizaje_ids':items_eval,
            'state':'espera'
            }
        
        evaluacion_id=autoevaluacion_obj.create(cr,SUPERUSER_ID,val)
        mail_message_obj=self.pool.get('mail.message')
       
        values={
            'body': 'Profesor '+profesor+'. Usted tiene una Autoevaluación a la espera de ser completada.', 
            'model': 'unefa.autoevaluacion_docente', 
            'res_id': evaluacion_id, 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, [partner_id]]], 
            'subject': False}
        mail_message_obj.create(cr,SUPERUSER_ID,values)
        return True
    
    def onchange_cargar_datos(self, cr, uid, ids, context=None):
        res={}
        item_planif_registro_control_obj=self.pool.get('unefa.items.planif.registro_control')
        item_planif_registro_control_ids=item_planif_registro_control_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_planif_registro_control_datos=item_planif_registro_control_obj.browse(cr,uid,item_planif_registro_control_ids,context=context)
        item_asistencia_control_obj=self.pool.get('unefa.items.asistencia.puntualidad')
        item_asistencia_control_ids=item_asistencia_control_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_asistencia_control_datos=item_asistencia_control_obj.browse(cr,uid,item_asistencia_control_ids,context=context)
        item_inicio_clase_obj=self.pool.get('unefa.items.inicio.clase')
        item_inicio_clase_ids=item_inicio_clase_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_inicio_clase_datos=item_inicio_clase_obj.browse(cr,uid,item_inicio_clase_ids,context=context)
        item_desarrollo_clase_obj=self.pool.get('unefa.items.desarrollo.clase')
        item_desarrollo_clase_ids=item_desarrollo_clase_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_desarrollo_clase_datos=item_desarrollo_clase_obj.browse(cr,uid,item_desarrollo_clase_ids,context=context)
        item_recursos_didacticos_obj=self.pool.get('unefa.items.recursos.didacticos')
        item_recursos_didacticos_ids=item_recursos_didacticos_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_recursos_didacticos_datos=item_recursos_didacticos_obj.browse(cr,uid,item_recursos_didacticos_ids,context=context)
        item_cierre_clase_obj=self.pool.get('unefa.items.cierre.clase')
        item_cierre_clase_ids=item_cierre_clase_obj.search(cr,uid,[('item_activo','=','True')],context=context)
        item_cierre_clase_datos=item_cierre_clase_obj.browse(cr,uid,item_cierre_clase_ids,context=context)
        items_planif=[]
        items_asis=[]
        items_inic=[]
        items_desar=[]
        items_recur=[]
        items_cierre=[]
        for i in item_planif_registro_control_datos:
            items_planif.append([0,False,{'items_evaluacion':i.id }])
        for i in item_asistencia_control_datos:
            items_asis.append([0,False,{'items_evaluacion':i.id }])
        for i in item_inicio_clase_datos:
            items_inic.append([0,False,{'items_evaluacion':i.id }])
        for i in item_desarrollo_clase_datos:
            items_desar.append([0,False,{'items_evaluacion':i.id }])
        for i in item_recursos_didacticos_datos:
            items_recur.append([0,False,{'items_evaluacion':i.id }])
        for i in item_cierre_clase_datos:
            items_cierre.append([0,False,{'items_evaluacion':i.id }])
        res={
            'planif_registro_control_ids':items_planif,
            'asistencia_puntualidad_ids':items_asis,
            'inicio_clase_ids':items_inic,
            'desarrollo_clase_ids':items_desar,
            'recursos_didacticos_ids':items_recur,
            'cierre_clase_ids':items_cierre,
            }
        return {'value':res}
        
        
    
    def onchange_profesor_id(self, cr, uid, ids,profesor_id,periodo_id, context=None):
        res={}
        profesores_obj=self.pool.get('res.users')
        profesores_ids=profesores_obj.search(cr,uid,[('id','=',int(profesor_id))],context=context)
        profesores_datos=profesores_obj.browse(cr,uid,profesores_ids,context=context)
        turno=''
        if profesores_datos['is_profesor'] == True:
            turno=profesores_datos['regimen']
        if profesores_datos['is_coordinador'] == True or profesores_datos['is_asistente']:
            turno=profesores_datos['coordinacion_id']['regimen']
       
        oferta_obj=self.pool.get('unefa.oferta_academica')
        oferta_ids=oferta_obj.search(cr,uid,[('carrera_id','=',int(profesores_datos['carrera_id'])),('periodo_id','=',int(periodo_id)),('turno','=',turno),],context=context)
        oferta_datos=oferta_obj.browse(cr,uid,oferta_ids,context=context)
        list_seccion=[]
        for oferta in oferta_datos:
            for pensum in oferta.pensum_ids:
                for semestre in pensum.semestres_ids:
                    for seccion in semestre.secciones_ids:
                        for asignatura in seccion.asignaturas_ids:
                            if int(asignatura.profesor_id)==profesor_id:
                                list_seccion.append(seccion.id)
        dominio={'seccion_id': [('id', '=', list(list_seccion))]}
        res={
            'carrera_id':int(profesores_datos['carrera_id']),
            'seccion_id':'',
            'materia_id':''
            }
        return {'value':res,'domain':dominio}
        
    def domain_asignatura (self, cr, uid, ids,profesor_id,periodo_id,seccion_id, context=None):
        res={}
        profesores_obj=self.pool.get('res.users')
        profesores_ids=profesores_obj.search(cr,uid,[('id','=',int(profesor_id))],context=context)
        profesores_datos=profesores_obj.browse(cr,uid,profesores_ids,context=context)
        turno=''
        if profesores_datos['is_profesor'] == True:
            turno=profesores_datos['regimen']
        if profesores_datos['is_coordinador'] == True or profesores_datos['is_asistente']:
            turno=profesores_datos['coordinacion_id']['regimen']
       
        oferta_obj=self.pool.get('unefa.oferta_academica')
        oferta_ids=oferta_obj.search(cr,uid,[('carrera_id','=',int(profesores_datos['carrera_id'])),('periodo_id','=',int(periodo_id)),('turno','=',turno),],context=context)
        oferta_datos=oferta_obj.browse(cr,uid,oferta_ids,context=context)
        list_asignatura=[]
        for oferta in oferta_datos:
            for pensum in oferta.pensum_ids:
                for semestre in pensum.semestres_ids:
                    for seccion in semestre.secciones_ids:
                        if int(seccion.id)==seccion_id:
                            for asignatura in seccion.asignaturas_ids:
                                if int(asignatura.profesor_id)==profesor_id:
                                    list_asignatura.append(asignatura.asignatura_id.id)
        dominio={'materia_id': [('id', '=', list(list_asignatura))]}
        
        res={
            'materia_id':''
            }
        
        return {'domain':dominio,'value':res}
        
    def buscar_cantidad_estudiantes (self, cr, uid, ids,seccion_id,asignatura_id, context=None):
        inscripcion_obj=self.pool.get('unefa.asignatura_inscritas')
        inscripcion_ids=inscripcion_obj.search(cr,uid,[('seccion_id','=',int(seccion_id)),('asignatura_id','=',int(asignatura_id))],context=context)
        value={
            'estudiantes_inscritos':len(inscripcion_ids),
        }
        return {'value':value}
        
    def comparacion_estudiantes_presentes(self, cr, uid, ids,estudiantes_inscritos,estudiantes_presentes, context=None):
        res={}
        warning={}
        if estudiantes_inscritos<estudiantes_presentes:
            warning = {
                'title': ('Aviso!'),
                'message' : ('La cantidad de alumnos presentes no puede se mayor a la de alumnos inscritos.')
                    }
            res={
                'estudiantes_presentes':'',
                }
        return {'value':res,'warning':warning}
        
        
    def button_dummy(self, cr, uid, ids, context=None):
        return True
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'state':'borrador',
            'estudiantes_inscritos':self.buscar_cantidad_estudiantes(cr,uid,[],vals['seccion_id'],vals['materia_id'])['value']['estudiantes_inscritos'],
            'carrera_id':self.onchange_profesor_id(cr, uid, [],vals['profesor_id'],1, context=None)['value']['carrera_id']
            })
        

        if vals['estudiantes_presentes']==0:
            raise osv.except_osv(('Aviso!'), ('La cantidad de alumnos presentes no puede se mayor a la de alumnos inscritos!'))
        if vals.get('Aviso', 'N°') == 'N°':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'unefa.supervision.clase') or 'N°'
        
        
        h=super(unefa_supervision_clase, self).create(cr, uid, vals, context=context)
       
        return h



    
class unefa_planif_registro_control(osv.osv):
   
    _name = 'unefa.planif.registro.control'
    _rec_name = 'items_evaluacion'

    _columns = {
        
        'supervision_clase_id': fields.many2one('unefa.supervision.clase', 'Supervisión',),
        'items_evaluacion': fields.many2one('unefa.items.planif.registro_control', 'Items de evaluación', readonly=True,),
        'evaluacion': fields.many2one('unefa.eval.planif.registro_control', 'Evaluación', required=True),
        }

class unefa_eval_planif_registro_control(osv.osv):
   
    _name = 'unefa.eval.planif.registro_control'
    _rec_name = 'evaluacion'

    _columns = {
        
        'evaluacion': fields.char('Opción de Evaluación',
                    required=True,
                    help="",
                    ),
        'valor_opcion': fields.integer('Valor',
                        help="",
                    ),
    }

class unefa_items_planif_registro_control(osv.osv):
   
    _name = 'unefa.items.planif.registro_control'
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


class unefa_asistencia_puntualidad(osv.osv):
   
    _name = 'unefa.asistencia.puntualidad'
    _rec_name = 'items_evaluacion'

    _columns = {
        
        'supervision_clase_id': fields.many2one('unefa.supervision.clase', 'Supervisión',),
        'items_evaluacion': fields.many2one('unefa.items.asistencia.puntualidad', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.many2one('unefa.eval.asistencia.puntualidad', 'Evaluación', required=True),
    }

class unefa_eval_asistencia_puntualidad(osv.osv):
   
    _name = 'unefa.eval.asistencia.puntualidad'
    _rec_name = 'evaluacion'

    _columns = {
        
        'evaluacion': fields.char('Opción de Evaluación',
                    required=True,
                    help="",
                    ),
        'valor_opcion': fields.integer('Valor',
                        help="",
                    ),
    }
    
class unefa_items_asistencia_puntualidad(osv.osv):
   
    _name = 'unefa.items.asistencia.puntualidad'
    _rec_name = 'item_evaluacion'

    _columns = {
        
        'item_evaluacion': fields.char('Item de evaluación',
                    required=False,
                    help="",
                    ),
        'item_activo': fields.boolean('Item Activo',
                        help="",
                    ),
    }
    
    _defaults={
        'item_activo':True,
    }
    
    
class unefa_inicio_clase(osv.osv):
   
    _name = 'unefa.inicio.clase'
    _rec_name = 'items_evaluacion'

    _columns = {
        
        'supervision_clase_id': fields.many2one('unefa.supervision.clase', 'Supervisión',),
        'items_evaluacion': fields.many2one('unefa.items.inicio.clase', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.many2one('unefa.eval.inicio.clase', 'Evaluación',required=True),
    }

class unefa_eval_inicio_clase(osv.osv):
   
    _name = 'unefa.eval.inicio.clase'
    _rec_name = 'evaluacion'

    _columns = {
        
        'evaluacion': fields.char('Opción de Evaluación',
                    required=True,
                    help="",
                    ),
        'valor_opcion': fields.integer('Valor',
                        help="",
                    ),
    }
    
class unefa_items_inicio_clase(osv.osv):
   
    _name = 'unefa.items.inicio.clase'
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
    
    
class unefa_desarrollo_clase(osv.osv):
   
    _name = 'unefa.desarrollo.clase'
    _rec_name = 'items_evaluacion'

    _columns = {
        
        'supervision_clase_id': fields.many2one('unefa.supervision.clase', 'Supervisión',),
        'items_evaluacion': fields.many2one('unefa.items.desarrollo.clase', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.many2one('unefa.eval.desarrollo.clase', 'Items de evaluación',required=True),
    }

class unefa_eval_desarrollo_clase(osv.osv):
   
    _name = 'unefa.eval.desarrollo.clase'
    _rec_name = 'evaluacion'

    _columns = {
        
        'evaluacion': fields.char('Opción de Evaluación',
                    required=True,
                    help="",
                    ),
        'valor_opcion': fields.integer('Valor',
                        help="",
                    ),
    }
    
class unefa_items_desarrollo_clase(osv.osv):
   
    _name = 'unefa.items.desarrollo.clase'
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
    
    
class unefa_recursos_didacticos(osv.osv):
   
    _name = 'unefa.recursos.didacticos'
    _rec_name = 'items_evaluacion'

    _columns = {
        
        'supervision_clase_id': fields.many2one('unefa.supervision.clase', 'Supervisión',),
        'items_evaluacion': fields.many2one('unefa.items.recursos.didacticos', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.many2one('unefa.eval.recursos.didacticos', 'Items de evaluación',required=True),
    }

class unefa_eval_recursos_didacticos(osv.osv):
   
    _name = 'unefa.eval.recursos.didacticos'
    _rec_name = 'evaluacion'

    _columns = {
        
        'evaluacion': fields.char('Opción de Evaluación',
                    required=True,
                    help="",
                    ),
        'valor_opcion': fields.integer('Valor',
                        help="",
                    ),
    }
    
class unefa_items_recursos_didacticos(osv.osv):
   
    _name = 'unefa.items.recursos.didacticos'
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


    
    
class unefa_cierre_clase(osv.osv):
   
    _name = 'unefa.cierre.clase'
    _rec_name = 'items_evaluacion'

    _columns = {
        
        'supervision_clase_id': fields.many2one('unefa.supervision.clase', 'Supervisión',),
        'items_evaluacion': fields.many2one('unefa.items.cierre.clase', 'Items de evaluación',readonly=True,),
        'evaluacion': fields.many2one('unefa.eval.cierre.clase', 'Items de evaluación',required=True),
    }

class unefa_eval_cierre_clase(osv.osv):
   
    _name = 'unefa.eval.cierre.clase'
    _rec_name = 'evaluacion'

    _columns = {
        
        'evaluacion': fields.char('Opción de Evaluación',
                    required=True,
                    help="",
                    ),
        'valor_opcion': fields.integer('Valor',
                        help="",
                    ),
    }
    
class unefa_itens_cierre_clase(osv.osv):
   
    _name = 'unefa.items.cierre.clase'
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
