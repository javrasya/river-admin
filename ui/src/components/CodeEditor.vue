<template>
  <codemirror :value="value" :options="cmOptions" @ready="onCmReady" @input="onCmCodeChange"></codemirror>
</template>

<script>
import { codemirror } from "vue-codemirror";
import initializePythonHints from "../helpers/python-hint";

// require styles
import "codemirror/lib/codemirror.css";
import "codemirror/mode/python/python.js";
import "codemirror/theme/base16-dark.css";

// require active-line.js
import "codemirror/addon/selection/active-line.js";
// styleSelectedText
import "codemirror/addon/selection/mark-selection.js";
import "codemirror/addon/search/searchcursor.js";
// hint
import "codemirror/addon/hint/show-hint.js";
import "codemirror/addon/hint/show-hint.css";

import "codemirror/addon/selection/active-line.js";
// highlightSelectionMatches
import "codemirror/addon/scroll/annotatescrollbar.js";
import "codemirror/addon/search/matchesonscrollbar.js";
import "codemirror/addon/search/searchcursor.js";
import "codemirror/addon/search/match-highlighter.js";
// keyMap
import "codemirror/mode/clike/clike.js";
import "codemirror/addon/edit/matchbrackets.js";
import "codemirror/addon/comment/comment.js";
import "codemirror/addon/dialog/dialog.js";
import "codemirror/addon/dialog/dialog.css";
import "codemirror/addon/search/searchcursor.js";
import "codemirror/addon/search/search.js";
import "codemirror/keymap/sublime.js";

export default {
  name: "CodeEditor",
  components: {
    codemirror
  },
  props: ["value", "read_only", "default_value", "extra_keywords"],
  mounted() {
    initializePythonHints(this.extra_keywords || []);
  },
  data: function() {
    return {
      cmOptions: {
        tabSize: 4,
        styleActiveLine: false,
        lineNumbers: true,
        styleSelectedText: false,
        line: true,
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        mode: "text/x-python",
        hintOptions: {
          completeSingle: false
        },
        keyMap: "sublime",
        matchBrackets: true,
        showCursorWhenSelecting: true,
        extraKeys: { "Ctrl-Space": "autocomplete" },
        readOnly: this.read_only ? "nocursor" : false
      }
    };
  },
  methods: {
    onCmCodeChange(newCode) {
      this.$emit("input", newCode);
    },
    onCmReady(cm) {
      cm.on("keypress", () => {
        cm.showHint();
      });
    }
  }
};
</script>