<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>

<script>
import 'multiple-select'
</script>

<style>
@import "../../node_modules/purecss/build/pure-min.css";
@import "../../node_modules/font-awesome/css/font-awesome.min.css";
@import "../../node_modules/multiple-select/multiple-select.css";

body {
    background-color: #eee;
    font-size: .8em;
    font-family: "Lato", "Helvetica", "Arial", sans-serif;
    color: #444;
}

h1,
h2 {
  color: #333;
}

h3 {
    margin-bottom: .5em;
    text-align: center;
}

h4 {
    margin-top: 0;
    color: #660000;
}

hr {
    border-color: #fff;
}

strong {
    color: #555;
}

textarea {
    border: 1px solid #ddd;
    max-width: 100%;
    padding: 0;
}

table {
    background-color: white;
    border: 1px solid #ddd;
    width: 100%;
}

td,
th {
    padding: .3em;
}

a:link {
  color: #e81c4f;
  text-decoration: none;
}

a:hover { color: #a20029; }

a:visited { color: #67041d; }

/* PURE CSS */
.pure-g > div {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}

/* MULTIPLE SELECT */
.ms-drop > ul > li {
    padding: .3em;
}

.ms-drop > ul > li > label {
    color: #111;
}

.ms-drop > ul > li > label > input {
    margin-right: .5em;
}

.ms-parent {
  width: 100% !important;
}

.ms-choice, .ms-drop {
    border-radius: 0;
}

/* CUSTOM */
.panel {
    background-color: white;
    border: 1px solid #ddd;
    padding: 1em;
}

.button {
    padding: .5em 1em;
    background-color: white;
    border: 1px solid #ddd;
    color: #333;
}

.button:focus {
    outline: 0;
}

.button:disabled {
    cursor: not-allowed !important;
    box-shadow: none !important;
    opacity: .65;
}

.button-primary {
    background-color: #d41a48;
    color: white;
    font-weight: bold;
    border: 1px solid #ab0830;
}

.button-styled {
    cursor: pointer;
}

.button-styled:hover {
    border-color: #ddd;
    color: #e81c4f;
}

.button-styled:disabled {
    color: grey;
    border-color: white;
}

.button-selected {
    color: #ab0830;
    font-weight: bold;
    border: 1px solid #ab0830;
}

.button-transparent {
    background-color: transparent;
    border: 0;
    color: #555;
}

.button-strong {
    font-weight: bold;
}

.button-flexible {
    padding: 0;
    width: 100%;
    height: 100%;
    display: inline-block;
}

.button-primary:hover {
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.3);
}

.button-block {
    width: 100%;
    height: 100%;
}
</style>