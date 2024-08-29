function enableDPOOptions() {
  const contactMethod = document.getElementById('id_dpo_contact_method');
  if (contactMethod.value !== 'NO' && contactMethod.value !== 'UD') {
    [
      'id_dpo_name',
      'id_dpo_value'
    ].forEach(id => {
      const field = document.getElementById(id);
      field.style.display = "block";
      field.previousElementSibling.style.display = "block";
    });
  }
}

function disableDPOOptions() {
  [
    'id_dpo_name',
    'id_dpo_value'
  ].forEach(id => {
    const field = document.getElementById(id);
    field.style.display = "none";
    field.previousElementSibling.style.display = "none";
  });
}

function enableSupportOptions() {
  const contactMethod = document.getElementById('id_support_contact_method');
  if (contactMethod.value !== 'NO') {
    [
      'id_support_name',
      'id_support_value'
    ].forEach(id => {
      const field = document.getElementById(id);
      field.style.display = "block";
      field.previousElementSibling.style.display = "block";
    });
  }
}

function disableSupportOptions() {
  [
    'id_support_name',
    'id_support_value'
  ].forEach(id => {
    const field = document.getElementById(id);
    field.style.display = "none";
    field.previousElementSibling.style.display = "none";
  });
}

function hideSupportOption() {
  [
    'form__row--support',
    'form__row--dpo'
  ].forEach(cNames => {
    const field = document.getElementsByClassName(cNames)[0];
    field.style.display = "none";
  });
}

function showSupportOption() {
  [
    'form__row--support',
    'form__row--dpo'
  ].forEach(cNames => {
    const field = document.getElementsByClassName(cNames)[0];
    field.style.display = "block";
  });
  enableDPOOptions();
  enableSupportOptions();
}

function supportOptionChange(checkmark) {
  if (checkmark.checked) {
    showSupportOption();
  } else {
    hideSupportOption();
  }
}

function DPOOptionChange(input) {
  if (input.value === 'NO' || input.value === 'UD') {
    disableDPOOptions();
  } else {
    enableDPOOptions();
  }
}

function SupportOptionChange(input) {
  if (input.value === 'NO') {
    disableSupportOptions();
  } else {
    enableSupportOptions();
  }
  const supportValueField = document.getElementById('id_support_value');
  if (input.value === 'NO') {
    supportValueField.setAttribute('placeholder', '');
  } else if (input.value === 'WS') {
    supportValueField.setAttribute('placeholder', 'https://www.website.org');
  } else if (input.value === 'EM') {
    supportValueField.setAttribute('placeholder', 'user@email.net');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const showSupportButtonCheck = document.getElementById('id_show_support_button');
  supportOptionChange(showSupportButtonCheck);
  showSupportButtonCheck.addEventListener('change', () => {
    supportOptionChange(showSupportButtonCheck);
  });

  const DPOMethodInput = document.getElementById('id_dpo_contact_method');
  DPOOptionChange(DPOMethodInput);
  DPOMethodInput.addEventListener('change', () => {
    DPOOptionChange(DPOMethodInput);
  });

  const SupportMethodInput = document.getElementById('id_support_contact_method');
  SupportOptionChange(SupportMethodInput);
  SupportMethodInput.addEventListener('change', () => {
    SupportOptionChange(SupportMethodInput);
  });
});