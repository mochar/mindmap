<template>
<div>
    <div class="panel">
        <h4>Graph settings</h4>
        
        <div class="pure-g" style="margin-bottom: .5em">
            <div class="pure-u-2-5"><label>Min. # publications</label></div>
            <div class="pure-u-3-5">
                <input type="number" min="1" :max="publicationMax" v-model="publicationCount" />
                <span>
                    /
                    <span>{{ publicationMax }}</span>
                </span>
            </div>
        </div>

        <div class="pure-g" style="margin-bottom: .5em">
            <div class="pure-u-2-5"><label>Predicates</label></div>
            <div class="pure-u-3-5">
                <select multiple="multiple" id="predicates-filter">
                    <option v-for="predicate in allPredicates" :value="predicate.id">
                        {{ predicate.name }}
                    </option>
                </select>
            </div>
        </div>
            
        <div class="pure-g">
            <div class="pure-u-1-2">
                <label>
                    <input type="checkbox" v-model="oneColor" />
                    One color
                </label>
            </div>
            <div class="pure-u-1-2"></div>
        </div>
            
        <div class="pure-g">
            <div class="pure-u-1-2">
                <label>
                    <input type="checkbox" v-model="sameWidth" />
                    One link width
                </label>
            </div>
            <div class="pure-u-1-2"></div>
        </div>
            
        <div class="pure-g">
            <div class="pure-u-1-2">
                <label>
                    <input type="checkbox" v-model="lonelyConcepts" />
                    Show all concepts
                </label>
            </div>
            <div class="pure-u-1-2"></div>
        </div>
        
        <button class="button button-strong" style="margin-top: 1em" @click="updateChart()"
                :disabled="!dirty">Update</button>
    </div>


    <div class="panel" style="margin-top: 1em">
        <h4>Enrichment</h4>
        
        <form @submit.prevent="enrich">
            <div class="pure-g">
                <div class="pure-u-2-5">
                    <label>Gene ontology</label>
                </div>
                <div class="pure-u-3-5">
                    <select name="go" class="ms-choice">
                        <option value="mf">Molecular function</option>
                        <option value="bp">Biological process</option>
                    </select>
                </div>
            </div>
            
            <button class="button button-strong" type="submit" :disabled="enriching">
                <span class="fa fa-refresh fa-spin" v-show="enriching"></span>
                Submit
            </button>
        </form>
        
        <table v-if="gos.length > 0" style="margin-top: .5em; border-width: 1px 0 1px;">
            <thead>
                <tr>
                    <th width="80%">Name</th>
                    <th width="20%">Score</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="go in gos">
                    <td>{{ go.name }}</td>
                    <td>{{ go.score }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    data() {
        return {
            enriching: false,
            gos: []
        }
    },

    methods: {
        enrich() {
            console.log('enrich')
        }
    },
    
    computed: {
        publicationCount: { 
            get() { return this.$store.state.publicationCount },
            set(value) { 
                this.$store.commit('updateStateObject', { value, object: 'publicationCount' }) 
                this.$store.commit('updateStateObject', { value: true, object: 'dirty' }) 
            }
        },
        oneColor: { 
            get() { return this.$store.state.oneColor },
            set(value) { 
                this.$store.commit('updateStateObject', { value, object: 'oneColor' }) 
                this.$store.commit('updateStateObject', { value: true, object: 'dirty' }) 
            }
        },
        sameWidth: { 
            get() { return this.$store.state.sameWidth },
            set(value) { 
                this.$store.commit('updateStateObject', { value, object: 'sameWidth' }) 
                this.$store.commit('updateStateObject', { value: true, object: 'dirty' }) 
            }
        },
        lonelyConcepts: { 
            get() { return this.$store.state.lonelyConcepts },
            set(value) { 
                this.$store.commit('updateStateObject', { value, object: 'lonelyConcepts' }) 
                this.$store.commit('updateStateObject', { value: true, object: 'dirty' }) 
            }
        },
        dirty: { 
            get() { return this.$store.state.dirty },
            set(value) { this.$store.commit('updateStateObject', { value, object: 'dirty' }) }
        },
        ...mapState([
            'publicationMax',
            'allPredicates'
        ])
    },

    mounted() {
        $('#predicates-filter').multipleSelect({
            filter: true,
            placeholder: 'Predicates',
            styler: value => {
                for(var i = 0; i < this.allPredicates.length; i++) {
                    if (this.allPredicates[i].id != value) continue
                    return 'border-left: 5px solid ' + this.allPredicates[i].color + ';'
                }
            },
            onClick: view => {
                let selected = $('#predicates-filter').multipleSelect('getSelects')
                if (selected.length === 0) {
                    // this.allPredicates.forEach(p => p.show = true)
                    this.$store.commit('filterPredicates', { all: true })
                } else {
                    // this.allPredicates.forEach(predicate => {
                    //     predicate.show = selected.indexOf(predicate.id) > -1
                    // })
                    let visibilities = this.allPredicates.map(p => selected.indexOf(p.id) > -1)
                    this.$store.commit('filterPredicates', { visibilities })
                }
                this.dirty = true
            },
            onCheckAll: () => {
                // this.allPredicates.forEach(p => p.show = true)
                this.$store.commit('filterPredicates', { all: true })
                this.dirty = true
            },
            onUncheckAll: () => {
                this.allPredicates.forEach(p => p.show = true)
                this.$store.commit('filterPredicates', { all: true })
                this.dirty = true
            }
        })
    }
}
</script>

<style>
</style>
