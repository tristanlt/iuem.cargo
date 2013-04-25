# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from iuem.cargo import _

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName

from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

class IProfilMembre(form.Schema):
    """Un profil de membre cargo
    """
    title = schema.TextLine(
            title=_(u"eppn"),
         )
    form.mode(title='hidden')
    dexteritytextindexer.searchable('displayname')
    displayname = schema.TextLine(
            title=_(u"Nom prénom"),
         )
    form.mode(displayname='hidden')
    dexteritytextindexer.searchable('description')
    description = schema.Text(
            title=_(u"Description"),
            description=_(u"Une rapide description..."),
            required=False
        )
    mail = schema.TextLine(
            title=_(u"Mail"),
            description=_(u"Adresse mail"),
            required=False
        )
    form.mode(mail='hidden')
    dexteritytextindexer.searchable('unite')
    unite = schema.TextLine(
            title=_(u"Unité"),
            required=False
        )
    dexteritytextindexer.searchable('organisme')
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
    dexteritytextindexer.searchable('competences')
    competences = RichText(
            title=_(u"Compétences"),
            description=_(u"Domaine d'expertise (liste non-exhaustive)"),
            required=False
        )
    dexteritytextindexer.searchable('projets')
    projets = RichText(
            title=_(u"Projets"),
            description=_(u"Projets passés ou en cours..."),
            required=False
        )
    dexteritytextindexer.searchable('attentes_de_formations')
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

alsoProvides(IProfilMembre, IFormFieldProvider)

@form.default_value(field=IProfilMembre['title'])
def default_title(data):
    membership = getToolByName(data.context, 'portal_membership')
    user = getSecurityManager().getUser()
    leuser=membership.getMemberById(user.getUserName())
    return leuser.getProperty('id')

@form.default_value(field=IProfilMembre['displayname'])
def default_displayname(data):
    membership = getToolByName(data.context, 'portal_membership')
    user = getSecurityManager().getUser()
    leuser=membership.getMemberById(user.getUserName())
    return leuser.getProperty('fullname')

@form.default_value(field=IProfilMembre['mail'])
def default_mail(data):
    membership = getToolByName(data.context, 'portal_membership')
    user = getSecurityManager().getUser()
    leuser=membership.getMemberById(user.getUserName())
    return leuser.getProperty('email')

@form.default_value(field=IProfilMembre['organisme'])
def default_organisme(data):
    return data.request.getHeader('X_SUPANN-ETABLISSEMENT')

@form.default_value(field=IProfilMembre['telephone'])
def default_telephone(data):
    return data.request.getHeader('X_TELEPHONENUMBER')

class View(grok.View):
    grok.context(IProfilMembre)
    grok.require('zope2.View')