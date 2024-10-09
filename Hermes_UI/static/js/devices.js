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
                                    <button class="btn btn-info btn-sm view-details-btn" onclick="openEditDeviceModal('${escapeHTML(deviceDetails.SYSNAME)}')">View Details</button>
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


function openEditDeviceModal(deviceName) {
    if (deviceName) {
        // Fetch existing device details to edit
        socket.emit('request_device', deviceName);
        socket.on('receive_device', function (deviceDetails) {
            const formHtml = getFormFromJSON(deviceDetails);
            $('#editDeviceModal .modal-body').html(formHtml);
            $('#editDeviceModal').modal('show');

            $('#saveDeviceBtn').off('click').on('click', function () {
                const updatedDevice = jsonBuilder($('#editDeviceModal .modal-body form').serializeArray());
                socket.emit('update_device', { deviceName, updatedDevice });
                $('#editDeviceModal').modal('hide');
            });
        });
    } else {
        // Prepare the modal for adding a new device
        $('#editDeviceModal .modal-body').html(getEmptyForm());
        $('#editDeviceModal').modal('show');

        $('#saveDeviceBtn').off('click').on('click', function () {
            const newDevice = jsonBuilder($('#editDeviceModal .modal-body form').serializeArray());
            socket.emit('add_device', newDevice);
            $('#editDeviceModal').modal('hide');
        });
    }
}

socket.on('updated_devices', (devices) => {
    populateDevicesTable(devices);
});
