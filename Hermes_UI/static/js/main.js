$(document).ready(function () {
    // Initial population of the rules table
    $.getJSON('/rules', function (data) {
        populateRulesTable(data);
    });

    // Handle Add New Rule button click
    $('#add-rule-btn').click(function () {
        const newRule = {}; // This can be populated as needed
        const ruleForm = buildFormFromObject(newRule);
        $('#rule-form-container').html(ruleForm);
        $('#ruleModal').modal('show');
    });

    // Save Rule button functionality
    $('#save-rule-btn').click(function () {
        const formData = $('#rule-form-container form').serializeArray();
        const jsonData = formToJson(formData);

        // Send the data to the server (modify endpoint as needed)
        $.ajax({
            url: '/rules',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(jsonData),
            success: function (response) {
                $('#ruleModal').modal('hide');
            },
            error: function (error) {
                console.error('Error saving rule:', error);
            }
        });
    });

    // Populate the history table initially
    $.getJSON('/history', function (data) {
        populateHistoryTable(data);
    });

    // Attach click event for edit buttons
    $(document).on('click', '.edit-rule-btn', function () {
        const ruleFileName = $(this).data('rule');
        requestRuleDetails(ruleFileName); // Request rule details
    });
});
