import qrcode

def generate_qr(data, filename="queue_qr.png"):
    qr = qrcode.make(data)
    qr.save(filename)
    return filename
