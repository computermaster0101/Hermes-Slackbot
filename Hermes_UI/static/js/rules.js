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
                        <td>
                            <button class="btn btn-info btn-sm view-details-btn" data-rule="${fileName}">View Details</button>
                            <button class="btn btn-warning btn-sm toggle-rule-btn" data-rule="${fileName}">${ruleData.active ? 'Deactivate' : 'Activate'}</button>
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
        const formHtml = getFormFromJSON(ruleDetails);
        $('#editRuleModal .modal-body').html(formHtml);
        $('#editRuleModal').modal('show');

        $('#editRuleModal form').on('submit', function (e) {
            e.preventDefault();
            const updatedRule = jsonBuilder($(this).serializeArray());
            socket.emit('update_rule', { fileName, updatedRule });
            $('#editRuleModal').modal('hide');
        });
    });
}
