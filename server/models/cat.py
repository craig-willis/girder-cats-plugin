#!/usr/bin/env python
# -*- coding: utf-8 -*-


from girder.constants import AccessType
from girder.models.model_base import AccessControlledModel
from girder.models.user import User
import datetime


class Cat(AccessControlledModel):

    def initialize(self):
        self.name = 'cat'
        
        self.exposeFields(level=AccessType.READ, fields={
            '_id', 'name', 'created', 'qualities', 'creatorId'})

        
    def validate(self, cat):
        return cat        

    def list(self, user=None, limit=0, offset=0,
             sort=None, currentUser=None):
        """
        List a page of jobs for a given user.

        :param user: The user who owns the job.
        :type user: dict or None
        :param limit: The page limit.
        :param offset: The page offset
        :param sort: The sort field.
        :param currentUser: User for access filtering.
        """
        cursor_def = {}
        if user is not None:
            cursor_def['creatorId'] = user['_id']

        cursor = self.find(cursor_def, sort=sort)
        for r in self.filterResultsByPermission(
                cursor=cursor, user=currentUser, level=AccessType.READ,
                limit=limit, offset=offset):
            yield r

    def deleteCat(self, cat, token):
        self.remove(cat)

    def createCat(self, cat=None, creator=None, save=True):
        now = datetime.datetime.utcnow()
        
        obj = {
            'name': cat['name'],
            'qualities': cat['qualities'],
            'created': now,
            'creatorId': creator['_id']
        }

        if save:
            cat = self.save(cat)

        return cat