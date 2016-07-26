# -*- coding: utf-8 -*-


from cStringIO import StringIO
import os
import zipfile
from shutil import rmtree

from openerp.osv import fields, osv
from openerp.addons.web.http import request
from openerp import http
from openerp.addons.web.controllers import main
from openerp import SUPERUSER_ID



class unefa_generar_lista_semestre(osv.TransientModel):
    """
        Este wizard es para crear listas por semestre de todos los estudiantes.
    """
    _name = "unefa.generar_lista_semestre"
    _description = "Crear lista de estudiantes por semesre"


         
    _columns = {
        'carrera_id': fields.many2one('unefa.carrera', 'Carrera',required=True,readonly=True,),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO')],'Turno', readonly=True),
        'periodo_id': fields.many2one('unefa.conf.periodo_academico','Período Académico',required=True),
        'pensum_id':fields.many2one('unefa.pensum', 'Pensum', required=True),
        'semestre_ids':fields.many2many('unefa.semestre','unefa_list_semestre_rel','lista_id','semestre_id','Semestres')
    }
    
    def carrera_turno_default(self,cr,uid,ids,context=None):
        coordinador_obj=self.pool.get('res.users')
        coordinador_data=coordinador_obj.browse(cr,uid,uid)
        carrera_id=coordinador_data['coordinacion_id']['carrera_id']['id']
        turno=coordinador_data['coordinacion_id']['regimen']
        value={
            'carrera_id':carrera_id,
            'turno':turno,
            }
        return {'value':value}
        
    def domain_semestre_ofertados(self,cr,uid,ids,carrera_id,turno,pensum_id,periodo_id,context=None):
        if pensum_id:
            list_semestres_ids=[]
            oferta_obj=self.pool.get('unefa.oferta_academica')
            oferta_ids=oferta_obj.search(cr,uid,[('carrera_id','=',carrera_id),('turno','=',turno),('periodo_id','=',periodo_id),])
            oferta_data=oferta_obj.browse(cr,uid,oferta_ids)
            for oferta in oferta_data:
                for pensum in oferta.pensum_ids:
                    if pensum.pensum_id.id==pensum_id:
                        for semestre in pensum.semestres_ids:
                            list_semestres_ids.append(semestre.semestre_id.id)
            domain={'semestre_ids': [('id', '=', list([6, False, list_semestres_ids]))]}
            return {'domain':domain}
        
        
    def generar_listas_semestres(self, cr, uid, ids, context=None):
        url='/descargar/listas_estudiantes_semestre/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }  
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'carrera_id':self.carrera_turno_default(cr,uid,[])['value']['carrera_id'],
            'turno':self.carrera_turno_default(cr,uid,[])['value']['turno'],
            })
        return super(unefa_generar_lista_semestre,self).create(cr,uid,vals,context=context)
       

    
