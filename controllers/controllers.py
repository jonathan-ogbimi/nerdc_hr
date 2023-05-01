# -*- coding: utf-8 -*-
from odoo import http

# class ManagerSupervisor(http.Controller):
#     @http.route('/manager_supervisor/manager_supervisor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manager_supervisor/manager_supervisor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('manager_supervisor.listing', {
#             'root': '/manager_supervisor/manager_supervisor',
#             'objects': http.request.env['manager_supervisor.manager_supervisor'].search([]),
#         })

#     @http.route('/manager_supervisor/manager_supervisor/objects/<model("manager_supervisor.manager_supervisor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manager_supervisor.object', {
#             'object': obj
#         })