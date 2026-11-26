"""Tests for the GET /activities endpoint."""

import pytest


def test_get_activities_returns_all_activities(client, fresh_activities):
    """Test that GET /activities returns all available activities."""
    # Arrange
    expected_count = len(fresh_activities)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_count


def test_get_activities_returns_correct_structure(client, fresh_activities):
    """Test that each activity has the required fields."""
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert - Check structure of first activity
    first_activity = activities["Chess Club"]
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity


def test_get_activities_contains_participants(client, fresh_activities):
    """Test that activities include their participants."""
    # Arrange
    expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    chess_club = activities["Chess Club"]
    assert len(chess_club["participants"]) == 2
    for participant in expected_participants:
        assert participant in chess_club["participants"]


def test_get_activities_contains_all_activity_names(client, fresh_activities):
    """Test that all activities are returned with correct names."""
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Robotics Club", "Science Club",
        "Gym Class", "Basketball Team", "Soccer Club", "Drama Club", "Visual Arts Studio"
    ]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name in expected_activities:
        assert activity_name in activities

