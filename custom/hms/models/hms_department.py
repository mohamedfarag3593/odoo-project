from odoo import models, fields


class HmsPatient(models.Model):
    _name = "hms.department"
    _rec_name = "name"

    name = fields.Char()
    is_opened = fields.Boolean()
    capacity = fields.Integer()
    patients_ids = fields.One2many(comodel_name="hms.patient", inverse_name="department_id")
