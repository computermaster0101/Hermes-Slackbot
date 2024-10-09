function escapeHTML(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function populateRulesTable(rule_set) {
    const rulesTableBody = $('#rules-table-body');
    rulesTableBody.empty();

    $.each(rule_set.rules, function (fileName, ruleDetails) {
        const ruleData = {
            name: escapeHTML(ruleDetails.name),
            patterns: escapeHTML(ruleDetails.patterns.join(', ')),
            actions: escapeHTML(ruleDetails.actions.join(', ')),
            active: ruleDetails.active,
        };

        const row = `<tr>
                        <td>${ruleData.name}</td>
                        <td class="wrap-content">${ruleData.patterns}</td>
                        <td class="wrap-content">${ruleData.actions}</td>
                        <td>${ruleData.active ? 'Active' : 'Inactive'}</td>
                        <td class="center-button">
                            <button class="btn btn-info btn-sm view-details-btn" data-rule="${fileName}">View Details</button>
                        </td>
                    </tr>`;
        rulesTableBody.append(row);
    });

    $('.view-details-btn').click(function () {
        const ruleFileName = $(this).data('rule');
        openEditRuleModal(ruleFileName);
    });
}



function openEditRuleModal(fileName) {
    socket.emit('request_rule', fileName);

    socket.on('receive_rule', function (ruleDetails) {
        const formHtml = getFormFromJSON(ruleDetails); // Create the form using formBuilder
        $('#editRuleModal .modal-body').html(formHtml); // Insert the form into the modal

        // Lock all inputs by adding the readonly attribute
        $('#editRuleModal .modal-body input').attr('readonly', true);

        // Lock all dropdowns by adding the disabled attribute
        $('#editRuleModal .modal-body select').attr('disabled', true);

        $('#editRuleModal').modal('show'); // Show the modal

        // Attach form submit event
        $('#editRuleModal form').on('submit', function (e) {
            e.preventDefault();
            const updatedRule = jsonBuilder($(this).serializeArray()); // Convert the form to JSON
            socket.emit('update_rule', { fileName, updatedRule });
            $('#editRuleModal').modal('hide');
        });
    });
}
