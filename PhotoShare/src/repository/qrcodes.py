import qrcode as qr

img_url = 'https://res.cloudinary.com/dfaj6dvo4/image/upload/v1696583325/avatars/byehupbpkaqxayo3dwng.jpg'
name = 'John Doe'  # Ваше ім'я чи інша інформація


async def generate_qr_code(img_url, name):
    combined_data = f"{name}\n{img_url}"

    qr_code = qr.QRCode(
        error_correction=qr.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr_code.add_data(combined_data)
    qr_code.make(fit=True)

    return qr_code

if __name__ == "__main__":
    import asyncio

    async def main():
        data = await generate_qr_code(img_url, name)
        data.print_ascii(tty=True, invert=True)
    asyncio.run(main())
