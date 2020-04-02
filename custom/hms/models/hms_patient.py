from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError, UserError
from datetime import date


class HmsPatient(models.Model):
    _name = "hms.patient"
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birthday = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([("a", "A"), ("b", "B"), ("ab", "AB"), ("o", "O")])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    department_id = fields.Many2one(comodel_name="hms.department")
    doctors_ids = fields.Many2many(comodel_name="hms.doctor")
    department_capacity = fields.Integer(related="department_id.capacity")
    logs = fields.One2many(comodel_name="hms.log", inverse_name="patient_id")

    state = fields.Selection([
        ("undetermined", "Undetermined"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("serious", "Serious")
    ], default="undetermined")
    email = fields.Char()
    full_name = fields.Char(compute="_full_name", store=True)
    age = fields.Integer(compute="calc_age", store=True)

    @api.depends("first_name", "last_name")
    def _full_name(self):
        for rec in self:
            if rec.first_name and rec.last_name:
                rec.full_name = rec.first_name + " " + rec.last_name
            else:
                raise UserError("Enter your (first and last) name")

    @api.depends("birthday")
    def calc_age(self):
        for rec in self:
            if rec.birthday:
                rec.age = date.today().year - rec.birthday.year
            else:
                raise UserError("Don't forget to enter your birthday")

    @api.multi
    def change_state(self):
        if self.state == "undetermined":
            self.state = "good"
        elif self.state == "good":
            self.state = "fair"
        elif self.state == "fair":
            self.state = "serious"
        elif self.state == "serious":
            self.state = "undetermined"
        self.logs.create({
            "patient_id": self.id,
            "description": self.first_name + "'s state has changed to " + self.state,
        })

    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    "title": "PCR",
                    "message": "The PCR is checked"
                }
            }
        else:
            self.pcr = False

    @api.constrains("email")
    def _check_email(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match is None:
                raise ValidationError('Not a valid E-mail ID')

    _sql_constraints = [
        ("Duplicated Email", "unique(email)", "This is E-mail is already exists!")
    ]
