import tkinter as tk
import webbrowser

class App:
    def __init__(self, root, urls):
        self.text_widget = tk.Text(root, wrap='word')
        self.text_widget.pack(expand=1, fill='both')

        for link in urls:
            self.text_widget.insert(tk.END, link + "\n", ('link', link))
            # Bind each URL to a separate tag
            self.text_widget.tag_bind(link, '<Button-1>', lambda event, url=link: webbrowser.open_new(url))

        # Configure the 'link' tag once
        self.text_widget.tag_config('link', foreground='blue', underline=True)

# Example usage
urls = ["https://www.openai.com", "https://www.python.org"]

root = tk.Tk()
app = App(root, urls)
root.mainloop()