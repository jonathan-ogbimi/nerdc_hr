import logging
from os import utime
from os.path import getmtime
from time import time

from odoo import api, http,fields,models
from odoo.http import SessionExpiredException

_logger = logging.getLogger(__name__)

class Users(models.Model):
    _inherit = "res.users"
    _sql_constraints = [
        ('uniq_login_ref', 'unique(login)', "A User already exists with this login"),
    ]
    
    @api.model
    def _auth_timeout_check(self):
        """Perform session timeout validation and expire if needed."""

        if not http.request:
            return

        session = http.request.session

        # Calculate deadline
        deadline = self._auth_timeout_deadline_calculate()

        # Check if past deadline
        expired = False
        if deadline is not False:
            path = http.root.session_store.get_session_filename(session.sid)
            try:

                expired = getmtime(path) < deadline
            except OSError:
                _logger.exception(
                    "Exception reading session file modified time.",
                )
                # Force expire the session. Will be resolved with new session.
                expired = True

        # Try to terminate the session
        terminated = False
        if expired:
            terminated = self._auth_timeout_session_terminate(session)

        # If session terminated, all done
        if terminated:
            # redirect to login
            return {
                "type": "ir.actions.act_url",
                "url": "/web/login",
                "target": "self",
            }
            #raise SessionExpiredException("Session expired")

        # Else, conditionally update session modified and access times
        ignored_urls = self._auth_timeout_get_ignored_urls()

        if http.request.httprequest.path not in ignored_urls:
            if "path" not in locals():
                path = http.root.session_store.get_session_filename(
                    session.sid,
                )
            try:
                utime(path, None)
            except OSError:
                _logger.exception(
                    "Exception updating session file access/modified times.",
                )
