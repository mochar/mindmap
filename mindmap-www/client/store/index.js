import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    // Data
    concepts: [],
    predicates: [],
    allPredicates: [],
    selectedConcept: null,

    // Graph settings
    publicationCount: 1,
    publicationMax: 100,
    oneColor: false,
    sameWidth: false,
    lonelyConcepts: false,
    dirty: false
}

const getters = {
    metabolites: state => {
        return state.concepts.filter(concept => concept.type === 'metabolite')
    },
    genes: state => {
        return state.concepts.filter(concept => concept.type === 'gene')
    }
}

const mutations = {
    updateStateObject(state, { object, value }) {
        state[object] = value
    },
    setData(state, { concepts, predicates, all }) {
        state.concepts = concepts.map(concept => {
            concept.show = true
            return concept
        })
        state.predicates = predicates
        state.allPredicates = all.map(p => {
            p.show = true
            return p
        })
        state.publicationMax = Math.max(...predicates.map(p => p.publicationCount))
    },
    filterPredicates(state, { all, visibilities }) {
        if (all != null) state.allPredicates.forEach(p => p.show = all)
        else state.allPredicates.forEach((p, i) => p.show = visibilities[i] )
    }
}

const actions = {
    getConcepts({ commit, getters }, { metabolites, genes }) {
        metabolites = metabolites || []
        genes = genes || []
        let formData = new FormData()
        formData.append('metabolites', [...metabolites, ...getters.metabolites.map(c => c.sourceId)])
        formData.append('genes', [...genes, ...getters.genes.map(c => c.sourceId)])
        return Vue.http.post(`${ROOTURL}/concepts`, formData)
    }
}

const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})

export default store
