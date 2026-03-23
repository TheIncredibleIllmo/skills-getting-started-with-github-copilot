"""
FastAPI tests for Mergington High School API using AAA (Arrange-Act-Assert) pattern
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Create a test client for the FastAPI app
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Fixture: Reset activities to initial state before each test
    Ensures test isolation - prevents test cross-contamination
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and visual arts exploration",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Learn instruments and perform in school concerts",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots for competitions",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["david@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["rachel@mergington.edu", "christopher@mergington.edu"]
        }
    }
    
    # Clear and repopulate activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup: restore original state after test
    activities.clear()
    activities.update(original_activities)


def test_get_activities(client, fresh_activities):
    """
    Test: GET /activities endpoint returns all activities
    
    AAA Pattern:
    - Arrange: Test client and fresh activities ready
    - Act: Make GET request to /activities
    - Assert: Verify 200 status, correct count, and required fields
    """
    # Arrange: Nothing additional needed, fixtures provide client and fresh_activities
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities_data = response.json()
    
    # Verify all 9 activities are returned
    assert len(activities_data) == 9
    
    # Verify each activity has required fields
    for activity_name, activity_details in activities_data.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)


def test_signup_for_activity(client, fresh_activities):
    """
    Test: POST /activities/{activity_name}/signup endpoint signs up a new student
    
    AAA Pattern:
    - Arrange: Prepare test data (activity name and new email)
    - Act: Make POST request to signup endpoint
    - Assert: Verify 200 status, confirmation message, and participant added
    """
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
    response_data = response.json()
    assert "message" in response_data
    assert new_email in response_data["message"]
    assert activity_name in response_data["message"]
    
    # Verify participant was actually added to the activity
    assert new_email in activities[activity_name]["participants"]


def test_unregister_from_activity(client, fresh_activities):
    """
    Test: POST /activities/{activity_name}/unregister endpoint removes a student
    
    AAA Pattern:
    - Arrange: Identify activity and existing participant
    - Act: Make POST request to unregister endpoint
    - Assert: Verify 200 status, success message, and participant removed
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Known to be in Chess Club
    
    # Verify participant exists before removal
    assert existing_email in activities[activity_name]["participants"]
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert existing_email in response_data["message"]
    assert activity_name in response_data["message"]
    
    # Verify participant was actually removed from the activity
    assert existing_email not in activities[activity_name]["participants"]
