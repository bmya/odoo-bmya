# -*- coding: utf-8 -*-
# from __future__ import print_function
import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class PickingLineDescription(models.Model):
    _inherit = 'stock.move'

    move_description = fields.Char('Motivo del Movimiento')
