# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from iuem.cargo import _

class IProfilMembre(form.Schema):
    """Un profil de membre cargo
    """
    nomprenom = schema.TextLine(
            title=_(u"Nom Prénom"),
            required=False
        )
    description = schema.TextLine(
            title=_(u"Description"),
            description=_(u"Rapide description..."),
            required=False
        )
    mail = schema.TextLine(
            title=_(u"Mail"),
            description=_(u"Adresse mail"),
            required=False
        )
    unite = schema.TextLine(
            title=_(u"Unité"),
            required=False
        )
    organisme = schema.TextLine(
            title=_(u"Organisme"),
            description=_(u"CNRS, université..."),
            required=False
        )
    site_internet = schema.TextLine(
            title=_(u"Site Internet"),
            required=False
        )
    telephone = schema.TextLine(
            title=_(u"Téléphone"),
            required=False
        )
    competences = RichText(
            title=_(u"Compétences"),
            description=_(u"Domaine d'expertise (liste non-exhaustive)"),
            required=False
        )
    projets = RichText(
            title=_(u"Projets"),
            description=_(u"Projets passés ou en cours..."),
            required=False
        )
    attentes_de_formations = RichText(
            title=_(u"Attentes de formation"),
            description=_(u"Les formations qui pourraient vous être utiles."),
            required=False
        )
    portrait = NamedImage(
            title=_(u"Portrait"),
            description=_(u"Votre portrait"),
            required=False,
        )
    logo = NamedImage(
            title=_(u"Logo"),
            description=_(u"Le logo de votre unité"),
            required=False,
        )
    nb_service = schema.Int(
            title=_(u"Nombre de personne dans votre service."),
            required=False
        )
    nb_asr = schema.Int(
            title=_(u"Nombre d'ASR dans votre service."),
            required=False
        )
    responsable_de_service = schema.TextLine(
            title=_(u"Responsable de service"),
            required=False
        )
    
class View(grok.View):
    grok.context(IProfilMembre)
    grok.require('zope2.View')