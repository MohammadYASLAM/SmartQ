// user.js
function listenForQueueUpdates(queueId) {
    const queueRef = firebase.firestore().collection('queues').doc(queueId);
    queueRef.onSnapshot((doc) => {
        const data = doc.data();
        if (data) {
            updateUserPosition(data.users);
            updateEstimatedWaitTime(data.estimatedWaitTime);
        }
    });
}

function updateUserPosition(users) {
    const user = users.find(user => user.userId === firebase.auth().currentUser.uid);
    if (user) {
        document.getElementById("user-position").innerText = `Your position: ${user.position}`;
    }
}

function updateEstimatedWaitTime(waitTime) {
    document.getElementById("estimated-wait-time").innerText = `Estimated wait time: ${waitTime} minutes`;
}

function generateQR(queueId) {
    new QRCode(document.getElementById("qrcode"), {
        text: `${window.location.origin}/user-queue.html?queueId=${queueId}`,
        width: 200,
        height: 200
    });
}
