<template>
      <div class="tooltip">
        <ul>
            <p @click="closeOptions">X</p>
            <li @click="highlight">Highlight</li>
            <li>Mark Incorrect</li>
        </ul>
    </div>
</template>

<script>
import rangy from 'rangy-updated'


export default {
    name: "tooltip",
    data() {
        return {
            selectedKanji: "",
            showKanjiForm: false,
            highlighter: null,
        }
    },
    methods: {
        showOptions(e){
            const tooltipMenu = document.querySelector(".tooltip");
            this.selectedKanji = window.getSelection().getRangeAt(0).cloneRange()
  
            tooltipMenu.style.display = "inline-block";
            tooltipMenu.style.top = e.screenY + "px";
            tooltipMenu.style.left = e.screenX + "px";

        },
        highlight(){
            // Highlight a given kanji or part of sentence
            // const highlightArr = [];
            // const span = document.createElement("span");
            // span.style.fontWeight = "bold";
            // span.style.color = "green";
            
            // const saveNode = this.selectedKanji.startContainer;
            // const startOffSet = this.selectedKanji.startOffset;
            // const endOffset = this.selectedKanji.endOffset;
            // // const nodeHTML = saveNode.parentElement.innerHTML;
            // // const nodeTagName = saveNode.parentElement.tagName;

            // const range = document.createRange();

            // range.setStart(saveNode, startOffSet);
            // range.setEnd(saveNode, endOffset)
            // range.surroundContents(span)

            // highlightArr.push({
            //     "saveNode": saveNode,
            //     "startOff": startOffSet,
            //     "endOff": endOffset
            // })
            // this.$emit('highlight-submit', highlightArr)

            
        },
        closeOptions(){
            const tooltipMenu = document.querySelector(".tooltip");
            tooltipMenu.style.display = "none"
        },
        loadHighlight(){

            rangy.init();
            this.highlighter = rangy.createHighlighter();

            this.highlighter.addClassApplier(rangy.createClassApplier("highlight", {
            ignoreWhiteSpace: true,
            tagNames: ["span", "a"]
            }));
        },
    },
    created(){
        this.loadHighlight()
    }
}
</script>

<style>

</style>