
var records;

function flushRecords(recordsBufferSize) {
    records = {
        times: Array(recordsBufferSize).fill(0.0),
        xPositions: Array(recordsBufferSize).fill(0),
        yPositions: Array(recordsBufferSize).fill(0),
        counter: 0
    }
}

function postAndFlushRecords(recordsBufferSize) {
    // This console log printout is meant to be an actual AJAX request
    console.log("POST records:");
    console.log({
        times: records.times.slice(0,records.counter),
        xPositions: records.xPositions.slice(0,records.counter),
        yPositions: records.yPositions.slice(0,records.counter)
    });
    flushRecords(recordsBufferSize);
}

function log(elapsedTimeInSeconds, x, y, recordsBufferSize) {
    if (records.counter >= recordsBufferSize)
        postAndFlushRecords(recordsBufferSize);
    records.times[records.counter] = elapsedTimeInSeconds;
    records.xPositions[records.counter] = x;
    records.yPositions[records.counter] = y;
    records.counter++;
}

function initBufferTimeout(timeLimitInSeconds, recordsBufferSize) {
    setTimeout(() => {
        postAndFlushRecords(recordsBufferSize);
        initBufferTimeout(timeLimitInSeconds, recordsBufferSize);
    }, timeLimitInSeconds*1000);
}

function init() {
    const startTime = Date.now();
    const recordsBufferSize = 2500;
    flushRecords(recordsBufferSize);
    onmousemove = event => log((Date.now()-startTime)/1000, event.clientX, event.clientY);
    initBufferTimeout(10, recordsBufferSize);
}

init();
