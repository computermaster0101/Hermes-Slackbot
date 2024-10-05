// Function to populate the table with rules
function populateRulesTable(rules) {
    const rulesTableBody = $('#rules-table-body');
    rulesTableBody.empty(); // Clear existing rows

    $.each(rules, function (fileName, ruleDetails) {
        const ruleData = parseRuleDetails(ruleDetails);

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

    // Attach click event for edit buttons
    $('.edit-rule-btn').click(function () {
        const ruleFileName = $(this).data('rule');
        openEditRuleModal(ruleFileName);
    });
}

// Function to open the edit rule modal
function openEditRuleModal(fileName) {
    socket.emit('request_rule', fileName); // Request rule details via WebSocket
}

// Parse the rule details string into a structured object
function parseRuleDetails(ruleDetails) {
    const ruleLines = ruleDetails.split('\n');
    return {
        name: ruleLines[0].split(': ')[1],
        patterns: ruleLines[1].split(': ')[1] || 'N/A',
        actions: ruleLines[2].split(': ')[1] || 'N/A',
        active: ruleLines[6].split(': ')[1] === 'True'
    };
}
