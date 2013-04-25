# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from iuem.cargo import _

# for events handlers
from zope.lifecycleevent.interfaces import IObjectCreatedEvent,IObjectModifiedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from collective.geo.geographer.event import IObjectGeoreferencedEvent
# END for events handlers
from collective.geo.geographer.interfaces import IGeoreferenced
from collective.geo.geographer.interfaces import IWriteGeoreferenced
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.contentlocations.interfaces import IGeoManager

from pygeoif.geometry import from_wkt
import transaction

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName


class IProfilMembre(form.Schema):
    """Un profil de membre cargo
    """
    title = schema.TextLine(
            title=u"Nom prénom",
            default=u"lelogin"
        )
    form.mode(title='hidden')

    description = schema.Text(
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
    form.widget(lLcoordinates='collective.z3cform.mapwidget.widget.MapFieldWidget')
    # form.omitted('coordinates')
    lLcoordinates = schema.Text(
                         title=_(u"Coordinates"),
                         description=_(u"Modify geographical data for this content"),
                         required=False,
                         )
    
alsoProvides(IProfilMembre, IFormFieldProvider)

@form.default_value(field=IProfilMembre['title'])
def default_title(data):
    membership = getToolByName(data.context, 'portal_membership')
    user = getSecurityManager().getUser()
    leuser=membership.getMemberById(user.getUserName())
    return leuser.getProperty('id')

@form.default_value(field=IProfilMembre['description'])
def default_description(data):
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

class ProfilMembre(dexterity.Item):
    grok.implements(IProfilMembre, IGeoreferenceable)
    grok.name('profilmembre')

@grok.subscribe(IProfilMembre, IObjectAddedEvent)
def newProfilMembre(context , event):
    #logger.info("Cargo Member Created !")
    if context.lLcoordinates is None:
        return
    #import pdb;pdb.set_trace()

    geo = IGeoManager(context)
    geom = from_wkt(context.lLcoordinates)
    coords = geom.__geo_interface__
    geo.setCoordinates(coords['type'], coords['coordinates'])
    transaction.commit()
    context.reindexObject(idxs=['zgeo_geometry'])
    # import pdb;pdb.set_trace()

@grok.subscribe(IProfilMembre, IObjectModifiedEvent)
def modifZabriProject(context , event):
    if context.lLcoordinates is None:
        return
    geo = IGeoManager(context)
    prev_coords = geo.getCoordinates()
    geom = from_wkt(context.lLcoordinates)
    coords = geom.__geo_interface__
    if (prev_coords[0] != coords['type']) or (prev_coords[1] != coords['coordinates']):
        geo.setCoordinates(coords['type'], coords['coordinates'])
        transaction.commit()
        context.reindexObject(idxs=['zgeo_geometry'])

class View(grok.View):
    grok.context(IProfilMembre)
    grok.require('zope2.View')