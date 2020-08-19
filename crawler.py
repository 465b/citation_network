from scholarly import scholarly
import itertools
from fp.fp import FreeProxy

def set_new_proxy():
    while True:
        proxy = FreeProxy(rand=True, timeout=1).get()
        proxy_works = scholarly.use_proxy(http=proxy, https=proxy)
        if proxy_works:
            break
    print("Working proxy:", proxy)
    return proxy


def proxied_search_query(query):
	while True:
		try:
			search_query = scholarly.search_pubs(query)
			print("Got the results of the query")
			return search_query
		except Exception as e:
			print(e)
			print("Trying new proxy")
			set_new_proxy()


def proxied_search_author(author):
	while True:
		try:
			search_query = scholarly.search_author(author)
			print("Got the results of the query")
			return search_query
		except Exception as e:
			print(e)
			print("Trying new proxy")
			set_new_proxy()

def proxied_pub_fill(pub):
	while True:
		try:
			filled = pub.fill()
			print("Filled the publication")
			return filled
		except Exception as e:
			print(e)
			print("Trying new proxy")
			set_new_proxy()

def proxied_author_fill(author):
	while True:
		try:
			filled = author.fill()
			print("Filled the author")
			return filled
		except Exception as e:
			print(e)
			print("Trying new proxy")
			set_new_proxy()

def fetch_query_results(query,num=10):
	search_query = scholarly.search_pubs(query)
	results = itertools.islice(search_query, num)
	return list(results)


def fetch_author_by_name(author,num=10):
	search_query = scholarly.search_author(author)
	results = itertools.islice(search_query, num)
	return list(results)


def fill_and_clean(query_results):
	for item in query_results:
		item.fill()
		item = item.bib
	return query_results


def network_by_authors(authors):
	""" Based a list of authors a network containing authors who
		cited on ..
	
	Parameters:
	-----------

	authors : list

	Returns:
	-------

	network : 
	"""

	# for every author:
	dict_author_citer = {}

	for item in authors:
		citer = fetch_citer_by_author(item)
		dict_author_citer[item] = citer
	
	print(dict_author_citer)


def fetch_citer_by_author(author):
	# first, get the author entry

	# check if item is a name or an id
	#if name
	if True:
		author_gen = proxied_search_author(author)
	#else (if id)
	else:
		author_gen = scholarly.search_author_id(author)

	# what happens if there is more then one other?
	# check for that and throw an error
	matches = list(author_gen)
	
	assert (len(matches) == 1), "Author query not unique"
	author = matches[0]
	author = proxied_author_fill(author)
	
	# second, fetch all publications

	#authors_publications = [pub.bib['title'] for pub in author.publications]
	#print(authors_publications)

	# third, use these publications to query for citations
	for kk,pub in enumerate(author.publications):
		print(kk)
		# fetch the full publictation entry to get citations
		pub = proxied_pub_fill(pub)
		citers = [citation.bib['title'] for citation in pub.citedby]

	return citers

def network_by_query(query):
	pass
