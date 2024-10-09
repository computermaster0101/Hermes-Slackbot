function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function populateHistoryTable(history) {
    const historyTableBody = $('#history-table-body');
    historyTableBody.empty();
    history.sort().reverse();

    $.each(history, function (index, entry) {
        const escapedMessage = escapeHtml(JSON.stringify(entry.message));
        const fileNameWithoutExt = entry.filename.replace('.txt', '');

        const row = `<tr>
                        <td>${fileNameWithoutExt}</td>
                        <td>${escapedMessage}</td>
                        <td>
                            <button class="btn btn-info btn-sm view-details-btn" data-filename="${entry.filename}">View Details</button>
                        </td>
                    </tr>`;
        historyTableBody.append(row);
    });

    $('.view-details-btn').click(function () {
        const fileName = $(this).data('filename');
        fetchFileContents(fileName);
    });
}

function fetchFileContents(filename) {
    $.get(`/history/${filename}`, function (data) {
        $('#details-content').text(data);
        $('#detailsModal').modal('show');
    }).fail(function () {
        console.error('Error fetching file contents');
        $('#details-content').text('Error fetching file contents.');
        $('#detailsModal').modal('show');
    });
}
