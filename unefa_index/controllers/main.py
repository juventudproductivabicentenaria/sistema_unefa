# -*- coding: utf-8 -*-

from openerp import http
from openerp.addons.web.controllers import main
from openerp import SUPERUSER_ID
from openerp.addons.web.http import request
from openerp.addons.website_blog.controllers import main as main_blog

QueryURL=main_blog.QueryURL
class index(main.Home):
    @http.route('/', auth='public', website=True)
    def index(self):
        velocidad=60
        return http.request.website.render('unefa_index.index', {'edit':False
        })
   

        
    
    
    
    
    
    
    
    
    
