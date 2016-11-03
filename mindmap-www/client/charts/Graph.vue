<template>
<div style="height: 100%;"></div>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import * as d3 from 'd3'

export default {
    data() {
        return {
            svg: null,
            zoom: null,
            
            linkForce: null,
            chargeForce: null,
            centerForce: null,
            simulation: null,

            link: null,
            node: null,
            nodeHeight: 20,

            conceptsById: d3.map(),
            allPredicatesById: d3.map()
        }
    },
    
    methods: {
        updatePlot() {
            let width = parseInt(d3.select(this.$el).style('width'), 10)
            let height = parseInt(d3.select(this.$el).style('height'), 10)
            let g = this.svg.select('g')
            let defs = this.svg.select('defs')
            let linkWidth = d3.scaleLog().domain([1, this.publicationMax]).range([2, 6])
            
            this.svg.attr('width', width).attr('height', height)
            
            // Update simulation
            this.simulation
                .nodes(this.concepts)
                .force('link', this.linkForce.links(this.predicates))
                .force('charge', this.chargeForce)
                .force('center', this.centerForce.x(width / 2).y(height / 2))
            
            // Create arrow-head markers per predicate-type
            let marker = defs.selectAll('marker')
                .data(['marker-default', ...this.allPredicates], d => d.id ? d.id : d)
            marker.exit().remove()
            let markerEnter = marker.enter().append('marker')
                .attr('id', d => d.id ? 'marker-' + d.id : d)
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 6)
                .attr('markerWidth', 6)
                .attr('markerHeight', 6)
                .attr('orient', 'auto')
            markerEnter.append('path')
                .attr('d', 'M0,-5L10,0L0,5')
            markerEnter.merge(marker)
                .attr('fill', d => d.id ? d.color : 'darkgrey')
                .attr('color', d => d.id ? d.color : 'darkgrey')
            
            // Links are the predicates that connect the concepts (nodes)
            this.link = g.select('g.links')
                .selectAll('.link')
                .data(this.bilinks, d => d[3].tripleId)
            this.link.exit().remove()
            let linkEnter = this.link.enter().append('path')
                .attr('class', 'link')
            linkEnter
                .on('mouseover', function(d) {
                    d3.select(this).attr('stroke-dasharray', '2,2')
                })
                .on('mouseout', function(d) {
                    d3.select(this).attr('stroke-dasharray', '0')
                })
              .append('title')
                .text(d => d[3].name)
            this.link = linkEnter.merge(this.link)
                .attr('stroke-width', d => this.sameWidth ? 2 : linkWidth(d[3].publicationCount))
                .attr('stroke', d => this.oneColor ? 'darkgrey' : d[3].color)
                .attr('marker-end', d => {
                    let id = this.oneColor ? 'default' : d[3].id
                    return 'url(#marker-' + id + ')'
                })
                
            // Nodes are the concepts
            this.node = g.select('g.nodes').selectAll('.node')
                .data(this.concepts.filter(d => d.id > 0), d => d.id)
            this.node.exit().remove()
            let that = this // unfortunately
            let nodeEnter = this.node.enter().append('g')
                .attr('class', 'node')
                .on('click', function(d, i) { 
                    if (that.selectedConcept && that.selectedConcept.id == d.id) {
                        that.selectedConcept = null
                        that.fade(d, i, 1)
                        d3.select(this).select('text').attr('font-weight', 'normal')
                    } else {
                        let connected = that.fade(d, i, .1)
                        that.selectedConcept = { id: d.id, connected }
                        d3.select(this).select('text').attr('font-weight', 'bold')
                    }
                })
                .call(d3.drag()
                    .on('start', this.dragstarted)
                    .on('drag', this.dragged)
                    .on('end', this.dragended))
                    
            // These will be removed and readded later on. First we need
            // to get the width when the text is added.
            nodeEnter.append('text')
                .text(d => d.name.substring(0, 20))
                .attr('font-weight', 'bold')
                .attr('dy', '.35em')
            
            // The width takes the text length in account.
            nodeEnter.append('rect')
                .attr('width',  function(d) { 
                    let width = this.parentNode.getBBox().width + 5
                    d.width = width
                    return width
                })
                .attr('class', d => d.type === 'gene' ? 'gene-node' : 'metabolite-node')
                .attr('rx', d => d.type === 'gene' ? 0 : 3)
                .attr('height', this.nodeHeight)
                
            // Now that we know the width, the text will be readded.
            nodeEnter.selectAll('text').remove()
            nodeEnter.append('text')
                .text(d => d.name.substring(0, 20))
                .attr('text-anchor', 'middle')
                .attr('x', d => d.width / 2)
                .attr('y', this.nodeHeight / 2)
                .attr('dy', '.35em')
                
            this.node = nodeEnter.merge(this.node)
        },

        ticked() {
            if (this.link === null || this.node === null) return
            
            this.link.attr('d', d => {
                let midX1 = d[0].width / 2
                let midX2 = d[2].width / 2
                let midY = this.nodeHeight / 2
                
                let x1 = d[1].x
                let x2 = d[2].x + midX2
                let y1 = d[1].y
                let y2 = d[2].y + midY
                    
                let adjacent = x2 - x1
                let opposite = y2 - y1
                let rad = Math.atan(opposite / adjacent)
                let degree = rad * (180 / Math.PI)
                let nodeRad = Math.atan((this.nodeHeight / 2) / (d[2].width / 2))
                let nodeDegree = nodeRad * (180 / Math.PI)
                
                let newX2, newY2, distanceFromCenter
                // Link ends at the upside or downside
                if (Math.abs(degree) > nodeDegree) {
                    if (y2 < y1) { // Downside
                        newY2 = d[2].y + this.nodeHeight
                        distanceFromCenter = (x2 - x1) / ((y1 - y2) / (this.nodeHeight / 2))
                        newX2 = x2 - distanceFromCenter
                    } else { // Upside
                        newY2 = d[2].y
                        distanceFromCenter = (x2 - x1) / ((y2 - y1) / (this.nodeHeight / 2))
                        newX2 = x2 - distanceFromCenter
                    }
                } else { // Links ends at the sides
                    if (x2 > x1) { // Left
                        newX2 = d[2].x
                        distanceFromCenter = (y1 - y2) / ((x2 - x1) / (d[2].width / 2))
                        newY2 = y2 + distanceFromCenter
                    } else { // Right
                        newX2 = d[2].x + d[2].width
                        distanceFromCenter = (y1 - y2) / ((x1 - x2) / (d[2].width / 2))
                        newY2 = y2 + distanceFromCenter
                    }
                }
                
                return 'M' + (d[0].x + midX1) + ',' + (d[0].y + midY)
                     + 'S' + d[1].x + ',' + d[1].y
                     + ' ' + newX2 + ',' + newY2
            })
            this.node.attr('transform', d => 'translate(' + d.x + ',' + d.y + ')')
        },
        
        dragstarted(d) {
            if (!d3.event.active) this.simulation.alphaTarget(0.3).restart()
            let stopOnDrag = true // TODO
            if (stopOnDrag) {
                // Stop de simulation when the first node is dragged.
                this.simulation
                    .force('charge', null)
                    .force('center', null)
                    .force('link', null)
            }
            d.fx = d.x
            d.fy = d.y
        },

        dragged(d) {
            d.fx = d3.event.x
            d.fy = d3.event.y
        },

        dragended(d) {
            if (!d3.event.active) this.simulation.alphaTarget(0)
            d.fx = null
            d.fy = null
        },

        fade(c, i, opacity) {
            let predicates_ = this.predicates.filter(p => p.tripleId && p.source.id == c.id)
            let triples = predicates_.map(p => p.tripleId)
            let connectedConcepts = predicates_.map(p => p.target.id)
                
            this.svg.selectAll('g.nodes rect, g.nodes text')
                .transition()
                .style('opacity', d => {
                    return d.id == c.id || connectedConcepts.indexOf(d.id) > -1 ? 1 : opacity
                })
            
            this.svg.selectAll('g.links path')
                .transition()
                .style('opacity', d => triples.indexOf(d[3].tripleId) > -1 ? 1 : opacity)
            
            return connectedConcepts
        }
    },
    
    mounted: function() {
        let width = parseInt(d3.select(this.$el).style('width'), 10)
        let height = parseInt(d3.select(this.$el).style('height'), 10)
        
        // Create elements
        this.svg = d3.select(this.$el).append('svg')
            .attr('width', width)
            .attr('height', height)
        this.svg.append('defs')
        let g = this.svg.append('g')
        g.append('g').attr('class', 'links')
        g.append('g').attr('class', 'nodes')
        
        // d3-force objects
        this.linkForce = d3.forceLink().distance(100)
        this.chargeForce = d3.forceManyBody().strength(-80)
        this.centerForce = d3.forceCenter()
        this.simulation = d3.forceSimulation().on('tick', this.ticked)
        
        // Zoom and drag
        this.zoom = d3.zoom()
            .scaleExtent([0.4, 8])
            .on('zoom', () => g.attr('transform', d3.event.transform))
        this.svg.call(this.zoom)
        
        this.updatePlot()
    },
    
    updated: function() {
        this.updatePlot()
    },

    computed: {
        ...mapState([
            'publicationCount',
            'publicationMax',
            'oneColor',
            'sameWidth',
            'lonelyConcepts',
            'dirty'
        ]),
        selectedConcept: { 
            get() { return this.$store.state.selectedConcept },
            set(value) { this.$store.commit('updateStateObject', { value, object: 'selectedConcept' }) }
        },
        concepts() {
            let cs = this.$store.state.concepts.filter(c => c.show)
            cs.map(concept => {
                concept.width = 1
                let c = this.conceptsById.get(concept.id)
                return c ? c : concept
            })
            // Filter out unconnected concepts if lonelyConcepts===true
            // if (!this.lonelyConcepts) {
            //     let connectedConcepts = []
            //     this.predicates.forEach(predicate => {
            //         connectedConcepts.push(predicate.source.id, predicate.target.id)
            //     })
            //     cs = cs.filter(c => connectedConcepts.indexOf(c.id) > -1)
            // } 
            this.conceptsById = d3.map(cs, d => d.id)
            // this.concepts.forEach(function(concept) {
            //     if (concept.id < 0 && 
            //         this.conceptsById.get(concept.source) && 
            //         this.conceptsById.get(concept.target)) cs.push(concept)
            // })
            return cs
        },
        allPredicates() {
            let ap = this.$store.state.allPredicates
            this.allPredicatesById = d3.map(ap, d => d.id)
            return ap
        },
        predicates() {
            this.allPredicates // force call allPredicates() first
            let ps = this.$store.state.predicates.filter(p => {
                return this.allPredicatesById.get(p.id).show && 
                   p.publicationCount >= this.publicationCount &&
                   this.conceptsById.get(p.source) &&
                   this.conceptsById.get(p.target)
            })
            ps.forEach(predicate => {
                predicate.source = this.conceptsById.get(predicate.source)
                predicate.target = this.conceptsById.get(predicate.target)
            })
            return ps
        },
        bilinks() {
            // Intermediate nodes will have a negative id to distinguish them from
            // actual nodes.
            return this.predicates.map((predicate, i_) => {
                let s = predicate.source
                let t = predicate.target
                let i = { 
                    id: -1 * (i_ + 1), 
                    source: predicate.source.id, 
                    target: predicate.target.id
                }
                this.concepts.push(i)
                this.predicates.push({source: s, target: i}, {source: i, target: t})
                return [s, i, t, predicate]
            })
        }
    },

    watch: {
        bilinks() {
            this.simulation && this.simulation.alpha(.5).restart()
            // this.updatePlot()
        },
        concepts() {
            Vue.nextTick(() => this.updatePlot())
        }
    }
}
</script>

<style>
.nodes {
    cursor: default;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.nodes rect.gene-node {
    color: #333;
    fill: #333;
    stroke: black;
}

.nodes rect.metabolite-node {
    color: #660000;
    fill: #660000;
    stroke: #3e0000;
    rx: 3;
}

.nodes rect.highlight {
    color: #ab0830;
    fill: #ab0830;
}

.node > text {
    color: white;
    fill: white;
}

.link {
  fill: none;
}
</style>