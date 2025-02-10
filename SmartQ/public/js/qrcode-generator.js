// qrcode-generator.js
function generateQR(queueId) {
    const qr = new QRCode(document.getElementById("qrcode"), {
      text: `${window.location.origin}/user-queue.html?queueId=${queueId}`,
      width: 200,
      height: 200
    });
  }
  