import pandas as pd
import rdfpandas
from rdflib import Graph, Namespace
from rdflib.namespace import NamespaceManager, SKOS, DCTERMS

df = pd.read_csv('anzsic.csv', index_col = '@id', keep_default_na = True, dtype = {
   '@id': str, 
   'rdf:type': str, 
   'skos:prefLabel': str, 
   'skos:notation': str, 
   'skos:topConceptOf': str,
   'skos:inScheme': str, 
   'skos:broader' : str, 
   'skos:note': str, 
   'dcterms:source': str,
   'pav:version': str })

namespace_manager = NamespaceManager(Graph())
namespace_manager.bind('skos', SKOS, override = True)
namespace_manager.bind('dcterms', DCTERMS, override = True)
namespace_manager.bind('anzsic', Namespace('https://dalstonsemantics.com/ns/au/gov/abs/anzsic/'), override = True)
namespace_manager.bind('pav', Namespace('http://purl.org/pav/'), override = True)

g = rdfpandas.to_graph(df, namespace_manager)

# Turtle version of ANZSIC
ttl = g.serialize(format = 'turtle')
with open('anzsic.ttl', 'w') as file:
   file.write(ttl)

# JSON-LD version of ANZSIC
context = {'source': {'@id': 'http://purl.org/dc/terms/source', '@type': '@id'},
           'broader': {'@id': 'http://www.w3.org/2004/02/skos/core#broader', '@type': '@id'},
           'inScheme': {'@id': 'http://www.w3.org/2004/02/skos/core#inScheme', '@type': '@id'},
           'topConceptOf': {'@id': 'http://www.w3.org/2004/02/skos/core#topConceptOf', '@type': '@id'},
           'version': {'@id': 'http://purl.org/pav/version'},
           '@vocab': 'http://www.w3.org/2004/02/skos/core#'}
jsonld = g.serialize(format = 'json-ld', context = context, indent = 2)
with open('anzsic.jsonld', 'w') as file:
   file.write(jsonld)