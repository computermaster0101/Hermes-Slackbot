// Establish socket connection
const socket = io.connect();

// Listen for updates from the server
socket.on('new_rule_set', (rule_set) => {
    //for (const [filename, rule] of Object.entries(rule_set.rules)) {
    //    console.log(`Rule file: ${filename}`);
    //    console.log(`Rule name: ${rule.name}`);
    //    console.log(`Patterns: ${rule.patterns}`);
    //    console.log(`Actions: ${rule.actions}`);
    //    console.log(`Active: ${rule.active}`);
    //}
    populateRulesTable(rule_set)
});

socket.on('rules_updated', function (updatedRules) {
    console.log("Received updated rules:", updatedRules);
    populateRulesTable(updatedRules);
});

// Listen for rule details from the server
socket.on('rule_details', function (ruleDetails) {
    // Generate the form from ruleDetails
    const ruleForm = buildFormFromObject(ruleDetails);
    $('#rule-form-container').html(ruleForm);
    $('#ruleModal').modal('show');
});

// Function to request rule details
function requestRuleDetails(fileName) {
    socket.emit('request_rule', fileName); // Request rule details via WebSocket
}
