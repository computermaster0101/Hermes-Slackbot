$(document).ready(function () {
    const socket = io.connect();

    // Function to populate the table with rules
    function populateTable(rules) {
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
                // Optionally handle success response
                $('#ruleModal').modal('hide');
            },
            error: function (error) {
                console.error('Error saving rule:', error);
            }
        });
    });

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

    // Listen for updates from the server
    socket.on('rules_updated', function (updatedRules) {
        console.log("Received updated rules:", updatedRules);
        populateTable(updatedRules);
    });

    // Listen for rule details from the server
    socket.on('rule_details', function (ruleDetails) {
        // Generate the form from ruleDetails
        const ruleForm = buildFormFromObject(ruleDetails);
        $('#rule-form-container').html(ruleForm);
        $('#ruleModal').modal('show');
    });

    // Initial population of the table
    $.getJSON('/rules', function (data) {
        populateTable(data);
    });

    // Populate History Table
    function populateHistoryTable(history) {
        const historyTableBody = $('#history-table-body');
        historyTableBody.empty(); // Clear existing rows

        $.each(history, function (index, entry) {
            const message = JSON.stringify(entry.message); // Convert message object to JSON string for display
            const fileNameWithoutExt = entry.filename.replace('.txt', ''); // Remove .txt from filename

            const row = `<tr>
                        <td>${fileNameWithoutExt}</td>
                        <td>${message}</td>
                        <td>
                            <button class="btn btn-info btn-sm view-details-btn" data-filename="${entry.filename}">View Details</button>
                        </td>
                    </tr>`;
            historyTableBody.append(row);
        });

        // Attach click event for the View Details buttons
        $('.view-details-btn').click(function () {
            const fileName = $(this).data('filename');
            fetchFileContents(fileName);
        });
    }

    // Fetch and display the contents of the .txt file
    function fetchFileContents(filename) {
        // Make an AJAX call to fetch the contents
        $.get(`/history/${filename}`, function (data) {
            $('#details-content').text(data); // Set the text of the pre tag
            $('#detailsModal').modal('show'); // Show the modal
        }).fail(function () {
            console.error('Error fetching file contents');
            $('#details-content').text('Error fetching file contents.');
            $('#detailsModal').modal('show'); // Show the modal with error message
        });
    }





    // Example call to populate the history table
    // Replace with your actual implementation to fetch history data
    $.getJSON('/history', function (data) {
        populateHistoryTable(data);
    });
});
