function setDropdownEvent() {
  Array.prototype.forEach.call(document.querySelectorAll('.dropdown > select'), function (dropdown) {
    dropdown.addEventListener('change', function (e) {
      if (e.target.hasAttribute('data-autosubmit')) {
        var form = e.target.form;
        if (form) {
          form.submit();
        }
      }
    });
  });
}

function clearFilter(elementid) { // jshint ignore:line
  var element = document.querySelector('#' + elementid + ' [value="all"]').selected = true;
  document.getElementById("filter_form", element).submit();
}
function checkedBox() {
  var checkbox = document.getElementById('30-days-toggle');
  var thirtyDays = document.getElementById('30-days');
  if (checkbox.checked) {
    thirtyDays.value = 'true';
  } else {
    thirtyDays.value = 'false';
  }
}
function setCheckEvent() { // jshint ignore:line
  var toggle = document.getElementById('30-days-toggle');
  if (toggle) {
    toggle.addEventListener('click', checkedBox);
  }
}

function toggleOptionbox() { // jshint ignore:line
  let filterButton = document.getElementById("org_structure_filter_options");
  filterButton.style.display = (filterButton.style.display === "none") ? "block" : "none";
}

function toggleCheckbox(e, checkboxId) { // jshint ignore:line
  e.preventDefault();
  let checkbox = document.getElementById(checkboxId);
  checkbox.checked = !checkbox.checked;
}

function disableDistributeButton() {
  const distributeSelect = document.getElementById('distribute-to');
  let chosenOptions = [];
  for (const option of distributeSelect.options) {
    if (option.selected) {
      chosenOptions.push(option);
    }
  }
  const distributeButton = document.getElementById('distribute-matches');
  if (chosenOptions.length > 0) {
    distributeButton.disabled = false;
  } else {
    distributeButton.disabled = true;
  }
}

function setDistributeSelectEvent() {
  const distributeSelect = document.getElementById('distribute-to');
  if (distributeSelect) {
    distributeSelect.addEventListener('click', disableDistributeButton);
    disableDistributeButton();
  }
}

document.addEventListener('DOMContentLoaded', function () {
  setDropdownEvent();
  setCheckEvent();
  setDistributeSelectEvent();
});

htmx.onLoad(function () {
  // When content is loaded with HTMX, reinstantiate dropdown and checkbox code
  setDropdownEvent();
  setCheckEvent();
  setDistributeSelectEvent();
});