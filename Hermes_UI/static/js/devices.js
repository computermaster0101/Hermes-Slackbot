// Existing code in devices.js
socket.emit('get_devices');

function escapeHTML(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function populateDevicesTable(deviceData) {
    const devicesTableBody = $('#devices-table-body');
    devicesTableBody.empty();

    // Check if deviceData is an array and has elements
    if (Array.isArray(deviceData) && deviceData.length > 0) {
        deviceData.forEach(item => {
            const deviceDetails = item.device_info; // Access device_info from each item

            // Ensure deviceDetails has the required properties
            if (deviceDetails && deviceDetails.SYSNAME) {
                const row = `<tr>
                                <td>${escapeHTML(deviceDetails.SYSNAME)}</td>
                                <td>${escapeHTML(deviceDetails["Last Startup"] || 'N/A')}</td>
                                <td>${escapeHTML(deviceDetails["Last Updated"] || 'N/A')}</td>
                                <td>${escapeHTML(deviceDetails.Heartbeat || 'N/A')}</td>
                                <td>
                                    <button class="btn btn-info btn-sm view-details-btn" onclick="fetchDeviceDetails('${escapeHTML(deviceDetails.SYSNAME)}')">View Details</button>
                                </td>
                            </tr>`;
                devicesTableBody.append(row);
            }
        });
    } else {
        // Handle case when no devices are available
        const noDataRow = `<tr>
                                <td colspan="5" class="text-center">No devices found</td>
                            </tr>`;
        devicesTableBody.append(noDataRow);
    }
}

function fetchDeviceDetails(deviceName) {
    $.get(`/devices/${deviceName}`, function (data) {
        // Assuming `data` contains device details, we will use formBuilder to create a form
        const formHtml = getFormFromJSON(data); // Create the form from the device details
        $('#editDeviceModal .modal-body').html(formHtml); // Insert the form into the modal
        $('#editDeviceModal').modal('show'); // Show the modal

        // Attach form submit event
        $('#editDeviceModal form').on('submit', function (e) {
            e.preventDefault();
            const updatedDevice = jsonBuilder($(this).serializeArray()); // Convert the form to JSON
            $.ajax({
                url: `/devices/${deviceName}`,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(updatedDevice),
                success: function (response) {
                    $('#editDeviceModal').modal('hide');
                    // Optionally, refresh the table or show a success message
                },
                error: function () {
                    console.error('Error saving device details.');
                    // Handle error case
                }
            });
        });
    }).fail(function () {
        console.error('Error fetching device details');
        $('#details-content').text('Error fetching device details.');
        $('#editDeviceModal').modal('show');
    });
}

// Existing event listener for updated devices
socket.on('updated_devices', (devices) => {
    populateDevicesTable(devices);
});
