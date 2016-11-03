import uuid

from flask import session, render_template, request, jsonify

from app import app, euretos, randomcolor
from app.scripts.enrichment import Enrichment


random_color = randomcolor.RandomColor()


def find_triples(concepts):
    triples = euretos.find_triples(concepts)
    all_predicates = {}
    colors = random_color.generate(count=len(triples), luminosity='dark')
    for i, triple in enumerate(triples):
        if all_predicates.get(triple['id']) is None:
            t = {'name': triple['name'], 'id': triple['id'],
                 'color': colors[i]}
            all_predicates[t['id']] = t
            triple['color'] = t['color']
        else:
            triple['color'] = all_predicates[triple['id']]['color']
    return triples, list(all_predicates.values())


@app.route('/concepts', methods=['GET', 'POST'])
def concepts():
    metabolites = set(request.form.get('metabolites', '').split(','))
    genes = set(request.form.get('genes', '').split(','))
    concepts_ = euretos.chebis_to_concepts(metabolites, flatten=True)
    concepts_.extend(euretos.entrez_to_concepts(genes, flatten=True))
    triples, all_predicates = find_triples([c['id'] for c in concepts_])
    return jsonify({'concepts': concepts_, 'predicates': triples,
        'all': all_predicates})


@app.route('/enrichment', methods=['GET', 'POST'])
def enrichment():
    concepts_ = request.form.getlist('concepts[]')
    en = Enrichment(euretos, concepts_, request.form['go'])
    return jsonify({'gos': en.sorted_concepts})


@app.route('/disorders')
def disorders():
    disorder_concepts = euretos.search_disorders(request.args['term'])
    return jsonify({'concepts': disorder_concepts})


@app.route('/connected', methods=['GET', 'POST'])
def connected():
    concepts_ = request.form.getlist('concepts[]')
    connected_ = euretos.find_connected(concepts_, request.form['concept'])
    return jsonify({'connected': connected_})
    

@app.route('/connections', methods=['GET', 'POST'])
def connections():
    concept_ = request.form.get('concept')
    type_ = request.form.get('type')
    if concept_ is None or type_ is None:
        return jsonify({})
    if type_ == 'Inhibitors':
        euretos.find_inhibitors(concept_)
    return jsonify({})

