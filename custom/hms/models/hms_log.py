from odoo import models, fields


class PatientLog(models.Model):
    _name = "hms.log"

    patient_id = fields.Many2one(comodel_name="hms.patient")
    description = fields.Char()
    create_uid = fields.Many2one('res.users', 'by User', readonly=True)
    create_date = fields.Datetime('Date Created', readonly=True)
