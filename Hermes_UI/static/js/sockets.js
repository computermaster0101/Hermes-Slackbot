const socket = io();

socket.on('new_rule_set', (rule_set) => {
    console.log('got new rule set');
    populateRulesTable(rule_set);
});

socket.on('rules_updated', (updatedRules) => {
    console.log("Received updated rules:", updatedRules);
    populateRulesTable(updatedRules);
});

socket.on('update_history', (history) => {
    populateHistoryTable(history);
});

socket.on('rule_details', function (ruleDetails) {
    const ruleForm = buildFormFromObject(ruleDetails);
    $('#rule-form-container').html(ruleForm);
    $('#ruleModal').modal('show');
});

function requestRuleDetails(fileName) {
    socket.emit('request_rule', fileName);
}
