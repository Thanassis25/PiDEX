import qrcode  # Import QR code library

def generate_qr(username, amount):
    """ Generate a QR code for payments """
    data = f"pi_wallet:{username}:{amount}"  # Format QR data
    qr = qrcode.make(data)  # Create QR code
    qr.save("payment_qr.png")  # Save QR as an image

# Example usage
generate_qr("user1", 10)  # Generate QR for user1 sending 10 Pi

