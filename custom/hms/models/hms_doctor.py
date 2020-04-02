from odoo import models, fields, api


class HmsPatient(models.Model):
    _name = "hms.doctor"
    _rec_name = "first_name"

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary()
    patients_ids = fields.Many2many(comodel_name="hms.patient")
    full_name = fields.Char(compute="_full_name", store=True)

    @api.depends("first_name", "last_name")
    def _full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + " " + rec.last_name
