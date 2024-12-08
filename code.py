from flask import Flask, request, redirect, jsonify
from urllib.parse import urlparse
import string

app = Flask(__name__)

class URLShortener:
    def __init__(self):
        self.url_to_code = {}
        self.code_to_url = {}
        self.base62_chars = string.ascii_letters + string.digits
        self.counter = 0

    def encode(self, long_url):
        """Encodes a URL to a shortened URL."""
        if long_url in self.url_to_code:
            return self.url_to_code[long_url]
        
        short_code = self._generate_code()
        self.url_to_code[long_url] = short_code
        self.code_to_url[short_code] = long_url
        return short_code

    def decode(self, short_code):
        """Decodes a shortened URL to its original URL."""
        return self.code_to_url.get(short_code)

    def _generate_code(self):
        """Generates a unique Base62 code."""
        code = []
        num = self.counter
        self.counter += 1

        while num > 0 or not code:
            code.append(self.base62_chars[num % 62])
            num //= 62

        return ''.join(reversed(code))


shortener = URLShortener()

def is_valid_url(url):
    """Validate if the URL is properly formatted."""
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except:
        return False


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """API endpoint to shorten a URL."""
    long_url = request.json.get('long_url')
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = shortener.encode(long_url)
    short_url = f"http://192.168.162.59:5000/{short_code}"   # Replace <your-domain> with actual domain
    return jsonify({"short_url": short_url})


@app.route('/')
def home():
    """Basic homepage for your URL shortener."""
    return "Welcome to the URL Shortener! Use /shorten to shorten URLs."


    
@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect from short URL to original URL."""
    long_url = shortener.decode(short_code)
    if long_url:
        return redirect(long_url)
    return jsonify({"error": "Shortened URL not found"}), 404




import tkinter as tk
from tkinter import messagebox
import requests
from threading import Thread

def run_flask():
    app.run(host='0.0.0.0', port=5000)
class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener")
        self.backend_url = "http://127.0.0.1:5000"
        
        # Long URL input
        self.long_url_label = tk.Label(root, text="Enter Long URL:")
        self.long_url_label.grid(row=0, column=0, padx=10, pady=5)
        self.long_url_entry = tk.Entry(root, width=50)  # Entry box for long URL
        self.long_url_entry.grid(row=0, column=1, padx=10, pady=5)

        # Shortened URL input
        self.short_url_label = tk.Label(root, text="Shortened URL:")
        self.short_url_label.grid(row=1, column=0, padx=10, pady=5)
        self.short_url_entry = tk.Entry(root, width=50)  # Entry box for shortened URL
        self.short_url_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        self.shorten_button = tk.Button(root, text="Shorten", command=self.shorten_url)
        self.shorten_button.grid(row=2, column=0, padx=10, pady=10)

        self.retrieve_button = tk.Button(root, text="Retrieve", command=self.retrieve_url)
        self.retrieve_button.grid(row=2, column=1, padx=10, pady=10)

    def shorten_url(self):
        long_url = self.long_url_entry.get().strip()  # Get URL from entry box
        if not self.is_valid_url(long_url):
            messagebox.showerror("Error", "Please enter a valid URL.")
            return
        
        try:
            response = requests.post(f"{self.backend_url}/shorten", json={"long_url": long_url})
            if response.status_code == 200:
                shortened_url = response.json()["short_url"]
                self.short_url_entry.delete(0, tk.END)  # Clear the entry box
                self.short_url_entry.insert(0, shortened_url)  # Insert the shortened URL
                messagebox.showinfo("Success", "URL Shortened Successfully!")
            else:
                error_message = response.json().get("error", "Failed to shorten URL.")
                messagebox.showerror("Error", error_message)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def retrieve_url(self):
        messagebox.showinfo("Info", "Use the shortened URL directly in your browser!")

    @staticmethod
    def is_valid_url(url):
        """Validate URL format."""
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        except:
            return False
            
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True 
    flask_thread.start()


    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()