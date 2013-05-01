#!/usr/bin/env python
from bottle import route, run

global	_cache
_cache = {}

@route('/<key>/<value>')
def setvalue(key, value):	#XXX limit to setting from localhost only?
	global	_cache
	_cache[key] = value

@route('/<key>')
def getvalue(key):
	global	_cache
	return _cache[key]

run(host = '0.0.0.0', port = 8083)
