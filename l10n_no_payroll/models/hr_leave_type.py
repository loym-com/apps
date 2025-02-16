from odoo import fields, models


class LeaveType(models.Model):
    _inherit = "hr.leave.type"

    json = fields.Serialized()
    l10n_no_type = fields.Selection(
        string="Leave / Layoff",
        sparse="json",
        selection=[
            ("permisjon", "Permisjon"),
            ("permittering", "Permittering"),
        ],
    )

    # PERMISJON

    l10n_no_PermisjonsOgPermitteringsBeskrivelse = fields.Selection(
        string="Permisjonsbeskrivelse",
        sparse="json",
        selection=[
            ("permisjonMedForeldrepenger", "Permisjon med foreldrepenger"),
            ("permisjonVedMilitaertjeneste", "Permisjon ved militærtjeneste"),
            ("utdanningspermisjonLovfestet", "Utdanningspermisjon, lovfestet"),
            ("utdanningspermisjonIkkeLovfestet", "Utdanningspermisjon, ikke lovfestet"),
            ("andreLovfestedePermisjoner", "Andre lovfestede permisjoner"),
            ("andreIkkeLovfestedePermisjoner", "Andre ikke lovfestede permisjoner"),
        ],
    )
    l10n_no_PermisjonLoennetUloennet = fields.Selection(
        string="PermisjonLoennetUloennet",
        sparse="json",
        selection=[
            ("permisjonLoennet", "permisjonLoennet"),
            ("permisjonUloennet", "permisjonUloennet"),
        ],
    )

    # PERMITTERING

    l10n_no_PermitteringsBeskrivelse = fields.Selection(
        string="Permitteringsbeskrivelse",
        sparse="json",
        selection=[
            ("mangelPaaArbeidEllerOppdrag", "Mangel på arbeid eller oppdrag"),
            ("raastoffmangel", "Råstoffmangel"),
            ("arbeidskonfliktEllerStreik", "Arbeidskonflikt eller streik"),
            ("brann", "Brann"),
            ("paaleggFraOffentligMyndighet", "Pålegg fra offentlig myndighet"),
            ("andreAarsaker", "Andre årsaker"),
        ],
    )
