<template>
<div>
    <div v-if="!adding">
        <div class="panel panel-toolbar">
            <div class="pure-g">
                <div class="pure-u-3-5">
                    <span class="fa fa-search"></span>
                    <input type="text" v-model="searchWord" />
                </div>
                <div class="pure-u-1-5"></div>
                <div class="pure-u-1-5">
                    <button class="button button-block" @click="adding = true">Add</button>
                </div>
            </div>
        </div>

        <table class="result-table">
            <thead>
                <tr>
                    <th width="5%"><span class="fa fa-eye"></span></th>
                    <th width="75%">{{ columns[0] }}</th>
                    <th width="10%">{{ columns[1] }}</th>
                    <th width="10%">{{ columns[2] }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="concept in filteredConcepts">
                    <td>
                        <input type="checkbox" v-model="concept.show" @click.prevent="updateChart()" />
                    </td>
                    <td>
                        <span v-show="!concept.show">{{ concept.name }}</span>
                        <a href="#" v-show="concept.show" @click="">{{ concept.name }}</a>
                    </td>
                    <td>{{ concept.id }}</td>
                    <td>
                        <a :href="url + concept.sourceId">{{ concept.sourceId }}</a>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <div class="pure-g pagination-control">
            <div class="pure-u-1-5">
                <button class="button button-styled" style="width: 100%"
                        data-bind="enable: pagination.canPrev, click: pagination.prev">
                    Prev
                </button>
            </div>
            <div class="pure-u-1-5">
                <button class="button button-styled" style="width: 100%"
                        data-bind="enable: pagination.canNext, click: pagination.next">
                    Next
                </button>
            </div>
            <div class="pure-u-3-5"></div>
        </div>
    </div>

    <div v-if="adding">
        <div class="panel panel-toolbar">
            <div class="pure-g">
                <div class="pure-u-3-5"></div>
                <div class="pure-u-1-5" style="padding-right: .3em;">
                    <button class="button button-block" @click="adding = false" 
                            v-show="concepts.length > 0" :disabled="loading">
                        Cancel</button>
                </div>
                <div class="pure-u-1-5">
                    <button class="button button-block button-primary" style="font-size: .9em;"
                            :disabled="loading" @click="getConcepts">
                        Submit
                    </button>
                </div>
            </div>
        </div>
        
        <div class="panel" style="border-top-style: dashed">
            <textarea rows="20" style="width: 100%;" :name="name" v-model="inputConcepts"></textarea>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'

export default {
    data() {
        return {
            adding: true,
            searchWord: '',
            loading: false,
            inputConcepts: ''
        }
    },
    
    props: ['concepts', 'name', 'columns', 'url'],

    methods: {
        getConcepts() {
            this.loading = true
            let data = { [this.name]: this.inputConcepts.split(/\n/) }
            this.$store.dispatch('getConcepts', data).then(response => { // success
                this.$store.commit('setData', response.body)
                this.$store.commit('updateStateObject', { value: false, object: 'dirty' })
                this.loading = false
                this.adding = false
                this.inputConcepts = ''
                Vue.nextTick(() => $('#predicates-filter').multipleSelect('refresh'))
            }, response => { // error
                console.log(response)
                this.loading = false
            })
        },
        updateChart() {
            this.$emit('updateChart')
        }
    },

    computed: {
        filteredConcepts() {
            return this.concepts.filter(concept => {
                return concept.name.lastIndexOf(this.searchWord, 0) === 0
            })
        }
    }
}
</script>

<style>
.result-table {
    border-top: 0;
}

.pagination-control {
    background-color: white;
    border: 1px solid #ddd;
    border-top: 0;
}

.pagination-control .button {
    border-color: white;
}

.panel-toolbar {
    padding: .3em;
    border-bottom: 0;
}
</style>