from flask import Blueprint, render_template, abort
from beram import NEWS_DATA # Import shared data

news_bp = Blueprint('news', __name__)

@news_bp.route('/')
def list_news():
    """Displays the page listing all news articles."""
    # In a real app, you'd likely sort by date here
    # articles = sorted(NEWS_DATA, key=lambda item: item['date'], reverse=True)
    articles = NEWS_DATA # Using the current order for simplicity
    return render_template('news.html',
                           title='News & Updates',
                           articles=articles)

@news_bp.route('/<slug>')
def news_article(slug):
    """Displays a single news article based on its slug."""
    article = next((item for item in NEWS_DATA if item['slug'] == slug), None)
    if not article:
        # If no article with that slug is found, return 404
        abort(404)
    # You might add full content later:
    # article['full_content'] = "This is the full text of the news article..."
    return render_template('news_article.html',
                           title=article['title'],
                           article=article)