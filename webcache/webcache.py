#!/usr/bin/env python
from bottle import route, run, view

global	_cache
_cache = {}

@route('/<key>/<value>')
def setvalue(key, value):	#XXX limit to setting from localhost only?
	global	_cache
	_cache[key] = value

@route('/<key>')
@view('index')
def getvalue(key):
	global	_cache
	if not _cache.has_key(key):
		return ''
	return dict(key=key, value=_cache[key])

run(host = '0.0.0.0', port = 8083)
