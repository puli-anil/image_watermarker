from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

# Global variable to store the original image
original_image = None

def upload_image():
    global original_image
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_path:
        try:
            with Image.open(file_path) as img:
                original_image = img.convert("RGBA")
            show_preview(original_image)
            status_label.config(text="Image uploaded successfully!", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{e}")

def add_watermark():
    if original_image is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return

    watermark_text = watermark_entry.get().strip()
    if not watermark_text:
        messagebox.showerror("Error", "Please enter watermark text.")
        return

    img = original_image.copy()
    width, height = img.size

    watermark_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark_layer)

    font_size = int(height / 15)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(watermark_text, font=font)
    x = width - text_width - 20
    y = height - text_height - 20

    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    watermarked = Image.alpha_composite(img, watermark_layer)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
    )
    if save_path:
        try:
            watermarked.convert("RGB").save(save_path)
            status_label.config(text="Watermarked image saved!", fg="green")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save image:\n{e}")

def show_preview(image):
    preview = image.resize((4000, 4000))
    preview = ImageTk.PhotoImage(preview)
    image_label.config(image=preview)
    image_label.image = preview

# GUI setup
window = Tk()
window.title("Image Watermarking Tool")
window.geometry("400x550")
window.resizable(False, False)

title_label = Label(window, text="Image Watermarking Tool", font=("Helvetica", 16, "bold"))
title_label.pack(pady=15)

upload_button = Button(window, text="Upload Image", command=upload_image, width=20)
upload_button.pack(pady=10)

watermark_entry = Entry(window, width=40, font=("Helvetica", 12))
watermark_entry.pack(pady=10)
watermark_entry.insert(0, "Enter watermark text here")

add_button = Button(window, text="Add Watermark", command=add_watermark, width=20)
add_button.pack(pady=10)

image_label = Label(window)
image_label.pack(pady=10)

status_label = Label(window, text="", fg="green", font=("Helvetica", 10))
status_label.pack()

window.mainloop()
