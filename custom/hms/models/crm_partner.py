from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class CrmPartner(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one(comodel_name="hms.patient")
    vat = fields.Char(required=True)

    @api.constrains("email")
    def _check_email(self):
        if self.env["hms.patient"].search([("email", "=", self.email)]):
            raise ValidationError("This email is already exists!")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("You can't delete this customer because he linked with patient account")
        super().unlink()
