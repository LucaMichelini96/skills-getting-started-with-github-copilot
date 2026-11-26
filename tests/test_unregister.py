"""Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

import pytest


def test_unregister_successful(client, fresh_activities):
    """Test successful unregister from an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_removes_participant(client, fresh_activities):
    """Test that unregister removes the student from participants list."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    initial_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    
    # Assert - Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    participants = activities[activity_name]["participants"]
    
    assert email not in participants
    assert len(participants) == initial_count - 1


def test_unregister_activity_not_found(client, fresh_activities):
    """Test unregister from non-existent activity returns 404."""
    # Arrange
    invalid_activity = "Nonexistent Activity"
    email = "michael@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_student_not_signed_up(client, fresh_activities):
    """Test unregister of student not signed up returns 400."""
    # Arrange
    activity_name = "Chess Club"
    unregistered_email = "notstudent@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": unregistered_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up for this activity"


def test_unregister_increases_available_spots(client, fresh_activities):
    """Test that available spots increase after unregister."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    response_before = client.get("/activities")
    chess_before = response_before.json()[activity_name]
    spots_before = chess_before["max_participants"] - len(chess_before["participants"])
    
    # Act
    client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    
    # Assert
    response_after = client.get("/activities")
    chess_after = response_after.json()[activity_name]
    spots_after = chess_after["max_participants"] - len(chess_after["participants"])
    
    assert spots_after == spots_before + 1


def test_unregister_then_signup_same_student(client, fresh_activities):
    """Test that a student can signup again after unregistering."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act - Unregister
    client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    
    # Act - Try to signup again
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Signup should succeed
    assert response.status_code == 200
    
    # Assert - Verify student is in participants again
    response = client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    assert email in participants

