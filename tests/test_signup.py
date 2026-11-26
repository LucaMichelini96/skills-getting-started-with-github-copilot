"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_successful(client, fresh_activities):
    """Test successful signup to an activity."""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up" in data["message"]
    assert new_email in data["message"]


def test_signup_adds_participant_to_list(client, fresh_activities):
    """Test that signup adds the student to the participants list."""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    initial_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    
    # Assert - Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    participants = activities[activity_name]["participants"]
    
    assert new_email in participants
    assert len(participants) == initial_count + 1


def test_signup_activity_not_found(client, fresh_activities):
    """Test signup to non-existent activity returns 404."""
    # Arrange
    invalid_activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_already_registered(client, fresh_activities):
    """Test that signing up twice with same email returns 400."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act - Try to signup with an already registered email
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_decreases_available_spots(client, fresh_activities):
    """Test that available spots decrease after signup."""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    response_before = client.get("/activities")
    chess_before = response_before.json()[activity_name]
    spots_before = chess_before["max_participants"] - len(chess_before["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    
    # Assert
    response_after = client.get("/activities")
    chess_after = response_after.json()[activity_name]
    spots_after = chess_after["max_participants"] - len(chess_after["participants"])
    
    assert spots_after == spots_before - 1

