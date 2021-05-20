#!/usr/bin/env python3
import logging

from src.api.v1 import RouteHandler


class ControllerApi(object):

    log = logging.getLogger(__name__)

    def __init__(self, app):
        self._app = app
        self._rhandler = RouteHandler()
        self._init_controller_app()

    def _init_controller_app(self):
        self._load_controller_api()

    def _add_url_route(self, endpoint, rule, view_func, method):
        self.log.info(
            "Adding API %s: %s %s to Controller app" % (endpoint, method, rule))
        self._app.add_url_rule(
            rule, endpoint, view_func, methods=[method])

    def _load_controller_api(self):
        # Welcome Message"
        self._add_url_route('home', '/',
                            self._rhandler.hello, 'GET')

        self._add_crud_routes()
        self._add_admin_routes()

    def _add_admin_routes(self):
        """
        Admin only endpoints which may not be enabled in actual
        production run.
        """
        # USERS
        self._add_url_route('get_all_users', '/admin/users',
                            self._rhandler.get_all_users, 'GET')
        self._add_url_route('delete_all_users', '/admin/users/',
                            self._rhandler.delete_all_users, 'DELETE')


    def _add_crud_routes(self):
        self._add_url_route('signup', '/signup',
                            self._rhandler.signup, 'POST')
        self._add_url_route('login', '/login',
                            self._rhandler.login, 'POST')