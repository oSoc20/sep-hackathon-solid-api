import requests
from os import environ


def lblod_id_exists(lblod_id):
    query = """
    PREFIX ams: <http://www.w3.org/ns/adms#>
    SELECT DISTINCT ?id
    WHERE {
        ?id ams:identifier <%s>.
    }""" % lblod_id
    return bool(make_query(query))


def get_lblod_cities():
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns1: <http://data.vlaanderen.be/ns/mandaat#>
    PREFIX ns2: <http://data.vlaanderen.be/ns/besluit#>
    SELECT DISTINCT ?cityURI ?cityName
    WHERE {
        ?list rdf:type ns1:Kandidatenlijst;
        ns1:behoortTot ?election.
        ?election ns1:steltSamen ?bestuursOrgaan.
        ?bestuursOrgaan ns1:isTijdspecialisatieVan ?bestuursOrgaan2.
        ?bestuursOrgaan2 ns2:bestuurt ?bestuursEenheid.
        ?bestuursEenheid ns2:werkingsgebied ?cityURI.
        ?cityURI rdfs:label ?cityName.
    }"""

    return make_query(query)


def get_lblod_lists(city_url):
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX core: <http://www.w3.org/2004/02/skos/core#>
        PREFIX ns1: <http://data.vlaanderen.be/ns/mandaat#>
        PREFIX ns2: <http://data.vlaanderen.be/ns/besluit#>
        SELECT DISTINCT ?listURI ?listName
        WHERE {
            ?listURI rdf:type ns1:Kandidatenlijst;
            core:prefLabel ?listName;
            ns1:behoortTot ?election.
            ?election ns1:steltSamen ?bestuursOrgaan.
            ?bestuursOrgaan ns1:isTijdspecialisatieVan ?bestuursOrgaan2.
            ?bestuursOrgaan2 ns2:bestuurt ?bestuursEenheid.
            ?bestuursEenheid ns2:werkingsgebied <%s>.
        }""" % city_url

    return make_query(query)


def get_lblod_candidates(list_url):
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX adms: <http://www.w3.org/ns/adms#>
        PREFIX ns1: <http://data.vlaanderen.be/ns/mandaat#>
        PREFIX ns2: <http://data.vlaanderen.be/ns/persoon#>
        SELECT DISTINCT ?personURI ?name ?familyName ?identifier
        WHERE {
            <%s> ns1:heeftKandidaat ?personURI.
            ?personURI ns2:gebruikteVoornaam ?name;
            foaf:familyName ?familyName;
            adms:identifier ?identifier.
        }""" % list_url

    return make_query(query)


def make_query(query):
    sparql_url = environ.get('SPARQL_URL')

    res = requests.get(
        sparql_url,
        params={
            "default-graph-uri": "http://api.sep.osoc.be/mandatendatabank",
            "format": "json",
            "query": query
        }
    )
    results = res.json()['results']['bindings']
    return results
