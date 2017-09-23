#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 14:21:07 2017

@author: viktor
"""

class Song(object):
    
    def __init__(self, url):
        self.url = url
        self.path = None
        self.title = None
        
    def __str__(self):
        return 'Url: {}\nPath:{}\nTitle:{}'.format(self.url, self.path, self.title)
