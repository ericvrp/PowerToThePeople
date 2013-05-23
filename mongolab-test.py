#!/usr/bin/env python

import random
import pymongo  #http://api.mongodb.org/python/current/tutorial.html
from config import mongodb_uri


def	main():
	connection = pymongo.Connection(mongodb_uri)
	test = connection.mongolab001db.test

	seed = random.random()
	print 'seed:', seed
	for i in range(10):
		test.insert({'seed' : seed, 'i' : i})

	print 'Now %d documents in the test collection of which %d with the current seed' % (\
		test.count(),
		test.find({'seed':seed}).count() )

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'Interrupted by user'
