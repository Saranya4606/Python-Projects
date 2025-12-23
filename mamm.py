import tkinter as tk
import re
import math

class MathAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Math Assistant")
        self.history = []

        self.text = tk.Text(root, wrap="word", height=25, width=80)
        self.text.pack(padx=10, pady=10)
        self.text.tag_config("blue", foreground="blue")
        self.text.tag_config("black", foreground="black")
        self.text.tag_config("gray", foreground="gray")
        self.text.tag_config("red", foreground="red")

        self.entry = tk.Entry(root, width=80)
        self.entry.pack(padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.process_input)

    def process_input(self, event):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)
        self.append_text(f"You: {user_input}\n", "blue")

        try:
            result, explanation = self.handle_input(user_input)
            self.append_text(f"AI: {result}\n", "black")
            self.append_text(f"Explanation:\n{explanation}\n\n", "gray")
            self.history.append((user_input, result))
            if len(self.history) > 50:
                self.history.pop(0)
        except ZeroDivisionError:
            self.append_text("Error: Oops! Division by zero is not allowed.\n\n", "red")
        except SyntaxError:
            self.append_text("Error: Sorry, I couldn’t understand the math expression.\n\n", "red")
        except Exception as e:
            self.append_text(f"Error: {str(e)}\n\n", "red")

    def append_text(self, text, tag):
        self.text.insert(tk.END, text, tag)
        self.text.see(tk.END)

    def handle_input(self, user_input):
        # Convert spelled out numbers
        user_input = self.words_to_numbers(user_input.lower())
        # Evaluate expression
        expression = self.prepare_expression(user_input)
        result = eval(expression)
        explanation = self.generate_explanation(expression, result)
        return result, explanation

    def words_to_numbers(self, text):
        words = {
            "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
            "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
            "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
            "fourteen": "14", "fifteen": "15", "sixteen": "16",
            "seventeen": "17", "eighteen": "18", "nineteen": "19",
            "twenty": "20", "thirty": "30", "forty": "40", "fifty": "50",
            "sixty": "60", "seventy": "70", "eighty": "80", "ninety": "90"
        }
        for word, num in words.items():
            text = re.sub(rf"\\b{word}\\b", num, text)
        return text

    def prepare_expression(self, text):
        text = text.replace("plus", "+").replace("minus", "-")
        text = text.replace("times", "*").replace("multiplied by", "*")
        text = text.replace("divided by", "/").replace("over", "/")
        text = text.replace("into", "*").replace("by", "/")
        return text

    def generate_explanation(self, expr, result):
        explanation = "You entered an arithmetic expression.\n"
        try:
            expr_clean = expr.replace(" ", "")
            steps = []

            def eval_with_steps(e):
                while "(" in e:
                    inner = re.search(r'\\([^()]+\\)', e)
                    if inner:
                        val = eval(inner.group())
                        steps.append(f"Evaluate {inner.group()} = {val}")
                        e = e.replace(inner.group(), str(val), 1)
                tokens = re.split(r'([+\-*/])', e)
                tokens = list(map(str.strip, tokens))
                current = float(tokens[0])
                steps.append(f"Start with: {current}")
                i = 1
                while i < len(tokens):
                    op = tokens[i]
                    val = float(tokens[i + 1])
                    if op == '+':
                        steps.append(f"Add {val} → {current + val}")
                        current += val
                    elif op == '-':
                        steps.append(f"Subtract {val} → {current - val}")
                        current -= val
                    elif op == '*':
                        steps.append(f"Multiply by {val} → {current * val}")
                        current *= val
                    elif op == '/':
                        if val == 0:
                            raise ZeroDivisionError
                        steps.append(f"Divide by {val} → {current / val}")
                        current /= val
                    i += 2
                return current

            final = eval_with_steps(expr_clean)
            steps.append(f"Final Result: {final}")
            explanation += "\n".join(steps)
        except:
            explanation += "Step-by-step breakdown not available."
        return explanation

if __name__ == "__main__":
    root = tk.Tk()
    app = MathAssistant(root)
    root.mainloop()
