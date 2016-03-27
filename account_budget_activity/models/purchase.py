# -*- coding: utf-8 -*-
from openerp import api, fields, models
from openerp.exceptions import except_orm, Warning


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

#     @api.multi
#     def _invoice_budget_check(self):
#         AccountBudget = self.env['account.budget']
#         for invoice in self:
#             if invoice.type != 'in_invoice':
#                 continue
#             # Get fiscal year and budget level for this group
#             fiscal_id, budgeting_level = AccountBudget.\
#                 get_fiscal_and_budgeting_level(invoice.date_invoice)
#             # Find amount in this invoice to check against budget
#             self._cr.execute("""
#                 select %(budgeting_level)s,
#                 coalesce(sum(price_subtotal), 0.0) amount
#                 from account_invoice_line where invoice_id = %(invoice_id)s
#                 group by %(budgeting_level)s
#             """ % {'budgeting_level': budgeting_level,
#                    'invoice_id': invoice.id}
#             )
#             # Check budget at this budgeting level
#             for r in self._cr.dictfetchall():
#                 res = AccountBudget.check_budget(r['amount'],
#                                                  r[budgeting_level],
#                                                  fiscal_id,
#                                                  budgeting_level)
#                 if not res['budget_ok']:
#                     raise Warning(res['message'])
#         return True

#     @api.multi
#     def action_date_assign(self):
#         self._invoice_budget_check()
#         return super(AccountInvoice, self).action_date_assign()

    @api.multi
    def wkf_confirm_order(self):
        for purchase in self:
            for line in purchase.order_line:
                Analytic = self.env['account.analytic.account']
                line.account_analytic_id = \
                    Analytic.create_matched_analytic(line)
        return super(PurchaseOrder, self).wkf_confirm_order()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    activity_group_id = fields.Many2one(
        'account.activity.group',
        string='Activity Group',
        required=True,
        compute='_compute_activity_group',
        store=True,
    )
    activity_id = fields.Many2one(
        'account.activity',
        string='Activity',
        required=False,
    )
    requisition_line_id = fields.Many2one(
        'purchase.requisition.line',
        string='Purchase Requisition Line',
    )

    @api.one
    @api.depends('product_id', 'activity_id')
    def _compute_activity_group(self):
        if self.product_id and self.activity_id:
            self.product_id = self.activity_id = False
            self.name = False
        if self.product_id:
            account_id = self.product_id.property_account_expense.id or \
                self.product_id.categ_id.property_account_expense_categ.id
            activity_group = self.env['account.activity.group'].\
                search([('account_id', '=', account_id)])
            self.activity_group_id = activity_group
        elif self.activity_id:
            self.activity_group_id = self.activity_id.activity_group_id
            self.name = self.activity_id.name

    @api.multi
    def onchange_product_id(
            self, pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft'):
        res = super(PurchaseOrderLine, self).onchange_product_id(
            pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=date_order, fiscal_position_id=fiscal_position_id,
            date_planned=date_planned, name=name,
            price_unit=price_unit, state=state)
        if not res['value'].get('date_planned', False):
            date_planned = date_planned or fields.Date.today()
            res['value'].update({'date_planned': date_planned})
        return res
