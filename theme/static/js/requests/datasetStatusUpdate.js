function updateStatus() {
    const processingDataset = document.querySelector('.status-processing');
    if (processingDataset) {
        const datasetId = processingDataset.getAttribute('data-dataset-id');
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                location.reload();
            }
        };
        xhr.open('GET', '/api/get_dataset_status/?dataset_id=' + encodeURIComponent(datasetId), true);
        xhr.send();
    }
    
}
setInterval(updateStatus, 6000);