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
