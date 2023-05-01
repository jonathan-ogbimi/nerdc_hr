
import logging
import re

from binascii import Error as binascii_error
from operator import itemgetter
from openerp.http import request

from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import groupby, formataddr

_logger = logging.getLogger(__name__)
_image_dataurl = re.compile(r'(data:image/[a-z]+?);base64,([a-z0-9+/\n]{3,}=*)\n*([\'"])(?: data-filename="([^"]*)")?', re.I)


class Message(models.Model):
    _inherit = "mail.message"
    
    @api.model
    def _get_default_from(self):
        default_email = 'erp@ccb.gov.ng'
        if self.env.user.email:
            return formataddr((self.env.user.name, self.env.user.email))
            #return formataddr((self.env.user.name, default_email))
        raise UserError(_("Unable to post message, please configure the sender's email address."))