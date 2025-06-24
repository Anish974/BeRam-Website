import pytest

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'BeRAM' in response.data

def test_about_page(client):
    """Test that the about page loads successfully."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_contact_page(client):
    """Test that the contact page loads successfully."""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact' in response.data

def test_projects_page(client):
    """Test that the projects page loads successfully."""
    response = client.get('/projects/')
    assert response.status_code == 200
    assert b'Projects' in response.data

def test_solutions_page(client):
    """Test that the solutions page loads successfully."""
    response = client.get('/solutions/')
    assert response.status_code == 200
    assert b'Solutions' in response.data

def test_news_page(client):
    """Test that the news page loads successfully."""
    response = client.get('/news/')
    assert response.status_code == 200
    assert b'News' in response.data

def test_mission_statement_page(client):
    """Test that the mission statement page loads successfully."""
    response = client.get('/mission-statement')
    assert response.status_code == 200
    assert b'Mission' in response.data

def test_404_page(client):
    """Test that the 404 page loads correctly."""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b'404' in response.data
