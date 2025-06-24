import pytest
from unittest.mock import patch

def test_contact_form_submission(client):
    """Test that the contact form submits successfully."""
    with patch('beram.main.routes.mail.send') as mock_send:
        response = client.post('/contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'inquiry_type': 'general',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }, follow_redirects=True)
        
        # Check that the form submission was successful
        assert response.status_code == 200
        assert b'Thank you for your message' in response.data
        
        # Check that the mail.send method was called twice (notification and confirmation)
        assert mock_send.call_count == 2

def test_contact_form_validation(client):
    """Test that the contact form validates input."""
    # Test with missing name
    response = client.post('/contact', data={
        'email': 'test@example.com',
        'inquiry_type': 'general',
        'subject': 'Test Subject',
        'message': 'This is a test message.'
    }, follow_redirects=True)
    
    # Form should not submit successfully
    assert b'Thank you for your message' not in response.data
    
    # Test with invalid email
    response = client.post('/contact', data={
        'name': 'Test User',
        'email': 'invalid-email',
        'inquiry_type': 'general',
        'subject': 'Test Subject',
        'message': 'This is a test message.'
    }, follow_redirects=True)
    
    # Form should not submit successfully
    assert b'Thank you for your message' not in response.data
