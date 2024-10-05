// Function to populate the table with rules
function populateRulesTable(rule_set) {
    const rulesTableBody = $('#rules-table-body');
    rulesTableBody.empty(); // Clear existing rows

    // Iterate over the rules in the provided rule set
    $.each(rule_set.rules, function (fileName, ruleDetails) {
        // Instead of parsing strings, we directly use the structured ruleDetails object
        const ruleData = {
            name: ruleDetails.name,
            patterns: ruleDetails.patterns.join(', '), // Assuming patterns is an array
            actions: ruleDetails.actions.join(', '), // Assuming actions is an array
            active: ruleDetails.active,
        };

        // Create a row for each rule
        const row = `<tr>
                        <td>${ruleData.name}</td>
                        <td>${ruleData.patterns}</td>
                        <td>${ruleData.actions}</td>
                        <td>${ruleData.active ? 'Active' : 'Inactive'}</td>
                        <td>
                            <button class="btn btn-success btn-sm edit-rule-btn" data-rule="${fileName}">Edit</button>
                            <button class="btn btn-danger btn-sm delete-rule-btn" data-rule="${fileName}">Delete</button>
                            <button class="btn btn-warning btn-sm toggle-rule-btn" data-rule="${fileName}">${ruleData.active ? 'Deactivate' : 'Activate'}</button>
                        </td>
                    </tr>`;
        rulesTableBody.append(row);
    });

    // Attach click event for edit buttons after the new rows are added
    $('.edit-rule-btn').click(function () {
        const ruleFileName = $(this).data('rule');
        openEditRuleModal(ruleFileName);
    });
}

// Function to open the edit rule modal
function openEditRuleModal(fileName) {
    socket.emit('request_rule', fileName); // Request rule details via WebSocket
}
