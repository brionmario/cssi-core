#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 CSSI.
# (c) This file is part of the CSSI Core library and is made available under MIT license.
# (c) For more information, see https://github.com/project-cssi/cssi-core/blob/master/LICENSE.txt
# (c) Please forward any queries to the given email address. email: opensource@apareciumlabs.com

"""This module provides plugin support for the CSSI Library

Authors:
    Brion Mario

"""

import sys
import logging

from cssi.exceptions import CSSIException

logger = logging.getLogger(__name__)


class Plugins:
    """Manages all the CSSI plugins"""

    def __init__(self):
        self.order = []
        self.names = {}
        self.contributor_plugins = []
        self.current_module = None
        self.debug = None

    @classmethod
    def load_plugins(cls, modules, config, debug):
        """Loads the plugins

        Args:
            modules (list): List of plugins in the configuration file.
            config (object): An object of the Config class.
            debug (bool): Boolean specifying if debug is enabled or not.

        Returns:
            list: List of plugins.
        """
        plugins = cls()
        plugins.debug = debug

        for module in modules:
            plugins.current_module = module
            __import__(module)
            mod = sys.modules[module]

            cssi_init = getattr(mod, "cssi_init", None)
            if not cssi_init:
                raise CSSIException(
                    "The plugin module {0} doesn't contain a cssi_init function".format(
                        module)
                )

            options = config.get_plugin_options(module)
            cssi_init(plugins, options)

        plugins.current_module = None
        return plugins

    def _add_plugin(self, plugin, category):
        """Add a plugin

        Args:
            plugin (object): Object of the plugin class.
            category (list): Related plugin category.
        """
        plugin_name = "{0}.{1}".format(
            self.current_module, plugin.__class__.__name__)
        logger.debug("Loaded plugin {0}: {1}".format(
            self.current_module, plugin.get_info()["type"].name))

        plugin._cssi_plugin_name = plugin_name
        plugin._cssi_enabled = True
        self.order.append(plugin)
        self.names[plugin_name] = plugin
        if category is not None:
            category.append(plugin)

    def add_contributor_plugin(self, plugin):
        """Add a contributor plugin

        Args:
            plugin (object): Object of the plugin class.
        """
        self._add_plugin(plugin, self.contributor_plugins)

    def add_questionnaire_plugin(self, plugin):
        """Add a questionnaire plugin

        Args:
            plugin (object): Object of the plugin class.
        Todo:
            * Add support for Questionnaire Plugins
        """
        # self._add_plugin(plugin, self.questionnaire_plugins)
