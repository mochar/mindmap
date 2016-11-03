<template>
<div class="pure-g">
    <div class="pure-u-1-3" id="left">
        <div class="pure-g" id="tabs">
            <div class="pure-u-1-5">
                <button class="button button-block" @click="tab = 'graph'"
                        :class="tab === 'graph' ? 'button-selected' : 'button-styled'">
                        Graph</button>
            </div>
            <div class="pure-u-2-5"></div>
            <div class="pure-u-1-5">
                <button class="button button-block" @click="tab = 'genes'"
                        :class="tab === 'genes' ? 'button-selected' : 'button-styled'">
                        Genes</button>
            </div>
            <div class="pure-u-1-5">
                <button class="button button-block" @click="tab = 'metabolites'"
                        :class="tab === 'metabolites' ? 'button-selected' : 'button-styled'">
                        Metabolites</button>
            </div>
        </div>
        
        <div id="result">
            <div v-show="tab === 'graph'">
                <graph-tab></graph-tab>
            </div>
            
            <div class="table-container" id="genes" v-show="tab === 'genes'">
                <concepts-tab
                    :concepts="genes"
                    name="genes"
                    :columns="['Gene', 'Euretos', 'Entrez']"
                    url="http://www.ncbi.nlm.nih.gov/gene/?term="
                    @updateChart="updateChart"
                ></concepts-tab>
            </div>
            
            <div class="table-container" id="metabolites" v-show="tab === 'metabolites'">
                <concepts-tab
                    :concepts="metabolites"
                    name="metabolites"
                    :columns="['Metabolite', 'Euretos', 'CHEBI']"
                    url="https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:"
                    @updateChart="updateChart"
                ></concepts-tab>
            </div>
        </div>
    </div>

    <div class="pure-u-2-3" id="right">
        <div class="panel" id="graph">
            <button class="button button-transparent button-block graph-button" 
                    style="border: 1px solid #bbb"
                    v-show="selectedConcept"
                    data-bind="click: function() { focus(!focus()); }, enable: selectedConcept">
                <span class="fa fa-eye"></span>
            </button>
            <graph></graph>
        </div>
    </div>
</div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import GraphTab from '../components/GraphTab'
import ConceptsTab from '../components/ConceptsTab'
import Graph from '../charts/Graph'

export default {
    data() {
        return {
            tab: 'graph'
        }
    },
    
    components: {
        GraphTab,
        ConceptsTab,
        Graph
    },

    methods: {
        updateChart() {
            console.log('updateChart')
        }
    },

    computed: {
        ...mapGetters([
            'metabolites', 
            'genes'
        ]),
        ...mapState([
            'selectedConcept'
        ])
    }
}
</script>

<style>
#left {
    padding: .6em;
    padding-top: .5em;
}

#right {
    padding-top: .5em;
    padding-right: .6em;
}

#graph {
    height: 90vh;
    position: relative;
    padding-top: .5em;
}

#genes {
    border-left: 3px solid black;
}

#metabolites {
    border-left: 3px solid #b30303;
}

#tabs {
    font-size: .9em;
    margin-bottom: 1em;
}

.table-container {
    margin-bottom: .5em;
}

.table-container > table {
    border-bottom: 0;
}

.graph-button {
    position: absolute;
    width: 7em;
    height: 2.2em;
    right: 1em;
}
</style>