import pytest
from app.services.TeamHandler import TeamHandler
from app.models.team_membership import Role
from app.models.todo_list import TodoList


# ─── create_team ─────────────────────────────────────────────────────────────

# Happy Path: Team wird erstellt und Ersteller als OWNER eingetragen
def test_create_team_saves_team_and_owner_membership(session, sample_user):
    # Arrange
    handler = TeamHandler(session)

    # Act
    team = handler.create_team(name="Entwicklung", creator_id=sample_user.id)

    # Assert
    assert team.id is not None
    assert team.name == "Entwicklung"
    assert team.created_by_id == sample_user.id
    memberships = handler.session.get.__self__ if False else None
    members = handler.get_members(team.id)
    assert any(u.id == sample_user.id for u in members)


# Happy Path: Ersteller erhält automatisch die Rolle OWNER
def test_create_team_assigns_owner_role_to_creator(session, sample_user):
    # Arrange
    handler = TeamHandler(session)

    # Act
    team = handler.create_team(name="Design", creator_id=sample_user.id)

    # Assert
    from sqlmodel import select
    from app.models.team_membership import Membership
    membership = session.exec(
        select(Membership)
        .where(Membership.team_id == team.id)
        .where(Membership.user_id == sample_user.id)
    ).first()
    assert membership is not None
    assert membership.role == Role.OWNER


# Edge Case: Leerer Name wirft ValueError
def test_create_team_raises_value_error_for_empty_name(session, sample_user):
    # Arrange
    handler = TeamHandler(session)

    # Act & Assert
    with pytest.raises(ValueError):
        handler.create_team(name="   ", creator_id=sample_user.id)


# ─── update ──────────────────────────────────────────────────────────────────

# Happy Path: Name und Beschreibung werden aktualisiert
def test_update_changes_team_fields(session, sample_team):
    # Arrange
    handler = TeamHandler(session)

    # Act
    updated = handler.update(sample_team.id, name="Neues Team", description="Neue Beschreibung")

    # Assert
    assert updated is not None
    assert updated.name == "Neues Team"
    assert updated.description == "Neue Beschreibung"


# Edge Case: Unbekannte ID gibt None zurück
def test_update_returns_none_for_unknown_team(session):
    # Arrange
    handler = TeamHandler(session)

    # Act
    result = handler.update(9999, name="Ghost")

    # Assert
    assert result is None


# Edge Case: Leerer Name wirft ValueError
def test_update_raises_value_error_for_empty_name(session, sample_team):
    # Arrange
    handler = TeamHandler(session)

    # Act & Assert
    with pytest.raises(ValueError):
        handler.update(sample_team.id, name="")


# ─── add_member ──────────────────────────────────────────────────────────────

# Happy Path: Neues Mitglied wird als MEMBER hinzugefügt
def test_add_member_adds_user_to_team(session, sample_team, sample_user_2):
    # Arrange
    handler = TeamHandler(session)

    # Act
    membership = handler.add_member(team_id=sample_team.id, user_id=sample_user_2.id)

    # Assert
    assert membership is not None
    assert membership.user_id == sample_user_2.id
    assert membership.role == Role.MEMBER


# Edge Case: Bereits vorhandenes Mitglied wirft ValueError
def test_add_member_raises_value_error_for_duplicate(session, sample_team, sample_user):
    # Arrange
    handler = TeamHandler(session)

    # Act & Assert
    with pytest.raises(ValueError):
        handler.add_member(team_id=sample_team.id, user_id=sample_user.id)


# Edge Case: Unbekanntes Team gibt None zurück
def test_add_member_returns_none_for_unknown_team(session, sample_user_2):
    # Arrange
    handler = TeamHandler(session)

    # Act
    result = handler.add_member(team_id=9999, user_id=sample_user_2.id)

    # Assert
    assert result is None


# ─── remove_member ───────────────────────────────────────────────────────────

# Happy Path: Mitglied wird erfolgreich entfernt
def test_remove_member_removes_user_from_team(session, sample_team, sample_user_2):
    # Arrange
    handler = TeamHandler(session)
    handler.add_member(team_id=sample_team.id, user_id=sample_user_2.id)

    # Act
    result = handler.remove_member(team_id=sample_team.id, user_id=sample_user_2.id)

    # Assert
    assert result is True
    members = handler.get_members(sample_team.id)
    assert not any(u.id == sample_user_2.id for u in members)


# Edge Case: Nicht-Mitglied entfernen gibt False zurück
def test_remove_member_returns_false_for_non_member(session, sample_team, sample_user_2):
    # Arrange
    handler = TeamHandler(session)

    # Act
    result = handler.remove_member(team_id=sample_team.id, user_id=sample_user_2.id)

    # Assert
    assert result is False


# ─── get_members ─────────────────────────────────────────────────────────────

# Happy Path: Alle Mitglieder werden zurückgegeben
def test_get_members_returns_all_members(session, sample_team, sample_user, sample_user_2):
    # Arrange
    handler = TeamHandler(session)
    handler.add_member(team_id=sample_team.id, user_id=sample_user_2.id)

    # Act
    members = handler.get_members(sample_team.id)

    # Assert
    member_ids = [u.id for u in members]
    assert sample_user.id in member_ids
    assert sample_user_2.id in member_ids


# Edge Case: Team ohne weitere Mitglieder gibt nur Owner zurück
def test_get_members_returns_only_owner_for_new_team(session, sample_team, sample_user):
    # Arrange
    handler = TeamHandler(session)

    # Act
    members = handler.get_members(sample_team.id)

    # Assert
    assert len(members) == 1
    assert members[0].id == sample_user.id


# ─── get_teams_for_user ──────────────────────────────────────────────────────

# Happy Path: Alle Teams eines Users werden zurückgegeben
def test_get_teams_for_user_returns_teams(session, sample_user, sample_team):
    # Arrange
    handler = TeamHandler(session)

    # Act
    teams = handler.get_teams_for_user(sample_user.id)

    # Assert
    assert len(teams) >= 1
    assert any(t.id == sample_team.id for t in teams)


# Edge Case: User ohne Teams gibt leere Liste zurück
def test_get_teams_for_user_returns_empty_list_for_user_without_teams(session, sample_user_2):
    # Arrange
    handler = TeamHandler(session)

    # Act
    teams = handler.get_teams_for_user(sample_user_2.id)

    # Assert
    assert teams == []


# ─── get_team_lists ──────────────────────────────────────────────────────────

# Happy Path: TodoListen eines Teams werden zurückgegeben
def test_get_team_lists_returns_todo_lists(session, sample_team):
    # Arrange
    handler = TeamHandler(session)
    todo_list = TodoList(name="Sprint 1", team_id=sample_team.id)
    session.add(todo_list)
    session.commit()

    # Act
    lists = handler.get_team_lists(sample_team.id)

    # Assert
    assert len(lists) == 1
    assert lists[0].name == "Sprint 1"


# Edge Case: Team ohne TodoListen gibt leere Liste zurück
def test_get_team_lists_returns_empty_list_when_no_lists(session, sample_team):
    # Arrange
    handler = TeamHandler(session)

    # Act
    lists = handler.get_team_lists(sample_team.id)

    # Assert
    assert lists == []


# ─── is_owner ────────────────────────────────────────────────────────────────

# Happy Path: Ersteller wird als Owner erkannt
def test_is_owner_returns_true_for_creator(session, sample_team, sample_user):
    # Arrange
    handler = TeamHandler(session)

    # Act
    result = handler.is_owner(team_id=sample_team.id, user_id=sample_user.id)

    # Assert
    assert result is True


# Happy Path: Normales Mitglied wird nicht als Owner erkannt
def test_is_owner_returns_false_for_member(session, sample_team, sample_user_2):
    # Arrange
    handler = TeamHandler(session)
    handler.add_member(team_id=sample_team.id, user_id=sample_user_2.id)

    # Act
    result = handler.is_owner(team_id=sample_team.id, user_id=sample_user_2.id)

    # Assert
    assert result is False


# Edge Case: Unbekanntes Team gibt False zurück
def test_is_owner_returns_false_for_unknown_team(session, sample_user):
    # Arrange
    handler = TeamHandler(session)

    # Act
    result = handler.is_owner(team_id=9999, user_id=sample_user.id)

    # Assert
    assert result is False
