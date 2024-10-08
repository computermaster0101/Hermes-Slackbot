$(document).ready(function () {
    const socket = io();

    $('#add-rule-btn').click(function () {
        const newRule = {};
        const ruleForm = buildFormFromObject(newRule);
        $('#rule-form-container').html(ruleForm);
        $('#ruleModal').modal('show');
    });
});
