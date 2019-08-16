"use strict";

console.clear();
window.onload = function () {

  var Model = {
    outputDisplay: "",

    deleteHandle: function deleteHandle() {
      this.outputDisplay = this.outputDisplay.length > 0 ? this.outputDisplay.substring(0, this.outputDisplay.length - 1) : "";
    },
    clearHandle: function clearHandle() {
      this.outputDisplay = "";
    },
    inputHandle: function inputHandle(key) {
      this.outputDisplay += key;
    },
  };

  var View = {
    btnEval: document.getElementById('Eval'),
    userInput: document.getElementById('UserInput'),
    deleteButton: document.getElementById('Delete'),
    clearButton: document.getElementById('Clear'),

    render: function render(M) {
      document.getElementById('UserInput').value = M.outputDisplay;
    },
    init: function init(C, M) {
      M.outputDisplay = document.getElementById('UserInput').value;
      // Evaluation buttons
      this.btnEval.onclick = function(){
        C.evalHandler();
      }
      // Delete button
      this.deleteButton.onclick = function () {
        C.handleDelete();
      };
      // Clear button
      this.clearButton.onclick = function () {
        C.handleClear();
      };
      // Digits buttons
      var digits = document.getElementsByClassName('digit');
      for (var i = 0; i < digits.length; ++i) {
        var item = digits[i].onclick = function () {
          var selectedDigit = this.getAttribute('data-val');
          C.handleInput(selectedDigit);
        };
      }
      // Non Digits buttons
      var cores = document.getElementsByClassName('core');
      for (var i = 0; i < cores.length; ++i) {
        var item = cores[i].onclick = function () {
          var selectedCore = this.getAttribute('data-val');
          C.handleInput(selectedCore);
        };
      }
      window.addEventListener("keydown", function (event) {
        if (event.keyCode == 13) {
          event.preventDefault();
          event.stopPropagation();
          document.getElementById("Eval").click();
        }
        if (event.keyCode == 8) {
          C.handleDelete();
        }
        if (event.keyCode == 46) {
          C.handleClear();
        }
      });
      window.addEventListener("keypress", function (event) {
        var keyIn = event.keyIdentifier ? parseInt(event.keyIdentifier.substr(2), 16) : event.keyCode;
        var charIn = String.fromCharCode(keyIn);

        if (/[+|-|*|\/|.|^|!|(|)|1|2|3|4|5|6|7|8|9|0|\-]/g.test(charIn)) {
          C.handleInput(charIn);
        }
      });
    }
  };

  var Controller = {
    load: function load() {
      // Singleton pattern
      if (Controller.instance){
        return;
      }
      // console.log(Controller.instance)
      Controller.instance = this;
      View.init(this, Model);
      View.render(Model);
    },
    evalHandler: function evalHandler() {
      let form = document.getElementById('form');
      form.submit();
    },
    update: function update() {
      View.render(Model);
    },
    handleDelete: function handleDelete() {
      Model.deleteHandle();
      View.render(Model);
    },
    handleClear: function handleClear() {
      Model.clearHandle();
      View.render(Model);
    },
    handleInput: function handleInput(key) {
      Model.inputHandle(key);
      View.render(Model);
    },
  };

  Controller.load();
};