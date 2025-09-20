# Method 1: Simple string formatting
def create_basic_html():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Python Generated Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Python Generated Website</h1>
        <div class="card">
            <h2>About This Page</h2>
            <p>This HTML page was generated using Python! Pretty cool, right?</p>
        </div>
        <div class="card">
            <h2>Features</h2>
            <ul>
                <li>Modern gradient background</li>
                <li>Responsive design</li>
                <li>Glass morphism effects</li>
            </ul>
        </div>
    </div>
</body>
</html>
    """

    with open('index.html', 'w') as f:
        f.write(html_content)
    print("Basic HTML file created: index.html")


# Method 2: Dynamic content with templates
def create_dynamic_html(title, content_items):
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background: #1a1a2e;
            color: #eee;
        }}
        .header {{
            background: linear-gradient(45deg, #16213e, #0f3460);
            padding: 40px 20px;
            text-align: center;
        }}
        .content {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .item {{
            background: #16213e;
            margin: 20px 0;
            padding: 25px;
            border-left: 4px solid #e94560;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        h1 {{ color: #00d4ff; }}
        h3 {{ color: #e94560; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
    </div>
    <div class="content">
        {content}
    </div>
</body>
</html>
    """

    content_html = ""
    for item in content_items:
        content_html += f"""
        <div class="item">
            <h3>{item['title']}</h3>
            <p>{item['description']}</p>
        </div>
        """

    final_html = html_template.format(
        title=title,
        content=content_html
    )

    with open('index.html', 'w') as f:
        f.write(final_html)
    print("Dynamic HTML file created: index.html")


# Method 3: Using a class-based approach
class HTMLGenerator:
    def __init__(self, title="My Website"):
        self.title = title
        self.head_content = []
        self.body_content = []

    def add_css(self, css):
        self.head_content.append(f"<style>{css}</style>")

    def add_element(self, tag, content="", attributes="", self_closing=False):
        if self_closing:
            element = f"<{tag} {attributes}>"
        else:
            element = f"<{tag} {attributes}>{content}</{tag}>"
        self.body_content.append(element)

    def generate(self, filename="generated.html"):
        css = """
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { color: #333; text-align: center; }
        .highlight { background: #ffeb3b; padding: 2px 6px; border-radius: 3px; }
        """

        self.add_css(css)

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    {''.join(self.head_content)}
</head>
<body>
    <div class="container">
        {''.join(self.body_content)}
    </div>
</body>
</html>
        """

        with open(filename, 'w') as f:
            f.write(html)
        print(f"Class-based HTML file created: {filename}")


# Method 4: Using Jinja2 templates (requires: pip install jinja2)
def create_with_jinja2():
    try:
        from jinja2 import Template

        template_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }}</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: #121212;
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }
        .card {
            background: #1e1e1e;
            border-radius: 12px;
            padding: 24px;
            margin: 16px 0;
            border: 1px solid #333;
        }
        h1 { color: #bb86fc; }
        .user { color: #03dac6; font-weight: bold; }
    </style>
</head>
<body>
    <h1>{{ page_title }}</h1>
    {% for user in users %}
    <div class="card">
        <p><span class="user">{{ user.name }}</span> - {{ user.role }}</p>
        <p>{{ user.bio }}</p>
    </div>
    {% endfor %}
</body>
</html>
        """

        template = Template(template_string)

        data = {
            'page_title': 'Team Directory',
            'users': [
                {'name': 'Alice', 'role': 'Developer', 'bio': 'Full-stack developer with 5 years experience'},
                {'name': 'Bob', 'role': 'Designer', 'bio': 'UI/UX designer passionate about user experience'},
                {'name': 'Carol', 'role': 'Manager', 'bio': 'Project manager keeping everything on track'}
            ]
        }

        html_output = template.render(data)

        with open('jinja_template.html', 'w') as f:
            f.write(html_output)
        print("Jinja2 template HTML file created: jinja_template.html")

    except ImportError:
        print("Jinja2 not installed. Run: pip install jinja2")


# Example usage
if __name__ == "__main__":
    # Method 1: Basic HTML generation
    create_basic_html()

    # Method 2: Dynamic content
    content_data = [
        {'title': 'Python Web Development', 'description': 'Build amazing web applications with Python'},
        {'title': 'Data Science', 'description': 'Analyze and visualize data using Python libraries'},
        {'title': 'Machine Learning', 'description': 'Create intelligent applications with ML algorithms'}
    ]
    create_dynamic_html("Python Programming Topics", content_data)

    # Method 3: Class-based approach
    generator = HTMLGenerator("My Generated Site")
    generator.add_element("h1", "Welcome to My Site!")
    generator.add_element("p", "This page was created using a <span class='highlight'>Python class</span>!")
    generator.add_element("h2", "Features")
    generator.add_element("ul",
                          "<li>Object-oriented design</li><li>Modular approach</li><li>Easy to extend</li>")
    generator.generate("class_based.html")

    # Method 4: Jinja2 templates
    create_with_jinja2()

    print("\nAll HTML files have been generated successfully!")
    print("Open any of these files in your web browser:")
    print("- index.html (basic)")
    print("- index.html (dynamic content)")
    print("- class_based.html (class-based)")
    print("- jinja_template.html (Jinja2, if available)")