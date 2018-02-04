# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools import float_round

def float_round_custom(value, precision_digits=None, precision_rounding=None, rounding_method='HALF-UP'):
	result = float_round(value, precision_digits, precision_rounding, rounding_method)
	if precision_rounding == 1:
		return int(result)
	return result

class ResCurrency(models.Model):
    _inherit = "res.currency"

    code = fields.Char(
            string="Código",
        )
    abreviatura = fields.Char(
            string="Abreviatura",
        )

    @api.v8
    def round(self, amount):
        """ Return `amount` rounded according to currency `self`. """
        return float_round_custom(amount, precision_rounding=self.rounding)

    @api.v7
    def round(self, cr, uid, currency, amount):
        """Return ``amount`` rounded  according to ``currency``'s
           rounding rules.

           :param Record currency: currency for which we are rounding
           :param float amount: the amount to round
           :return: rounded float
        """
        return float_round_custom(amount, precision_rounding=currency.rounding)
