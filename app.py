from flask import Flask, render_template, request, jsonify
from serpapi import GoogleSearch

app = Flask(__name__)  # Fixed here

# Function to search question papers
def search_question_papers(class_level, subject, topic=None, board=None, num_results=10):
    api_key = '026eba56b522c73aed476101bc5a284f5da3da0853557836efc1a2f8b0df762a'  # Replace with your SerpAPI key
    # Constructing the query based on provided inputs
    query = f"{class_level} {subject} question papers"

    # Add topic to the query if provided
    if topic:
        query += f" on {topic}"

    # If a specific board is selected, add it to the query
    if board and board != "All":
        query += f" {board}"

    engines = ["google", "bing", "yahoo"]
    all_links = []

    for engine in engines:
        page_number = 0
        while len(all_links) < num_results:
            params = {
                "engine": engine,
                "q": query,
                "api_key": api_key,
                "num": 20,
                "start": page_number * 20,
                "hl": "en",
            }

            search = GoogleSearch(params)
            results = search.get_dict()

            if 'organic_results' not in results:
                break

            for result in results['organic_results']:
                title = result.get('title')
                link = result.get('link')
                snippet = result.get('snippet', '')

                if any(keyword in title.lower() for keyword in ['question paper', 'exam paper', 'past paper']):
                    all_links.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })

                if len(all_links) >= num_results:
                    break

            page_number += 1

    return all_links[:num_results]

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/search', methods=['POST'])
def search():
    class_level = request.form['class_level']
    subject = request.form['subject']
    topic = request.form.get('topic')  # Get topic input
    board = request.form.get('board')  # Get board input
    num_results = int(request.form['num_results'])

    # Ensure num_results is within the allowed range (1 to 100)
    if num_results < 1:
        num_results = 1
    elif num_results > 100:
        num_results = 100

    # Perform the search
    results = search_question_papers(class_level, subject, topic, board, num_results=num_results)

    return jsonify(results)

if __name__ == "__main__":  # Fixed here
    app.run(debug=True)
