# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import speech_recognition as sr
import pyttsx3


class CustomerServiceClient(models.Model):
    _name = "customerservice.client"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Customer Service Client"
    _order = "id desc"

    @api.model
    def default_get(self, fields):
        res = super(CustomerServiceClient, self).default_get(fields)
        res['note'] = 'NEW Client Card'
        return res

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    image = fields.Binary(string="Client Image")

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Client'
        res = super(CustomerServiceClient, self).create(vals)
        return res

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            clients = self.env['customerservice.client'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if clients:
                raise ValidationError(_("Name %s Already Exists" % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_("Age Cannot Be Zero .. !"))

    def action_record_and_convert(self):
        sr.Microphone(device_index=1)
        r = sr.Recognizer()
        r.energy_threshold = 4000
        r.dynamic_energy_threshold = False

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                phrase = r.recognize_google(audio, language='en-US')
                self.note = phrase
            except TimeoutError as msg:
                print(msg)
