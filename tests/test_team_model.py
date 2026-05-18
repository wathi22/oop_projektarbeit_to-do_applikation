import pytest
from app.models.team import Team
from app.models.team_membership import Membership, Role


# ─── Team.__str__ ────────────────────────────────────────────────────────────

# Happy Path: __str__ gibt Name und ID zurück
def test_str_returns_name_and_id():
    # Arrange
    team = Team(id=1, name="Entwicklung")

    # Act
    result = str(team)

    # Assert
    assert "Entwicklung" in result
    assert "1" in result


# ─── Team.__repr__ ───────────────────────────────────────────────────────────

# Happy Path: __repr__ enthält alle wichtigen Felder
def test_repr_contains_key_fields():
    # Arrange
    team = Team(id=1, name="Entwicklung", description="Backend-Team")

    # Act
    result = repr(team)

    # Assert
    assert "Team(" in result
    assert "id=1" in result
    assert "name='Entwicklung'" in result
    assert "description='Backend-Team'" in result


# ─── Team.__eq__ ─────────────────────────────────────────────────────────────

# Happy Path: gleiche ID → gleich, auch wenn andere Felder abweichen
def test_eq_returns_true_for_same_id():
    # Arrange
    team1 = Team(id=1, name="Entwicklung")
    team2 = Team(id=1, name="Design")

    # Act
    result = team1 == team2

    # Assert
    assert result is True


# Happy Path: unterschiedliche ID → ungleich
def test_eq_returns_false_for_different_id():
    # Arrange
    team1 = Team(id=1, name="Entwicklung")
    team2 = Team(id=2, name="Entwicklung")

    # Act
    result = team1 == team2

    # Assert
    assert result is False


# Edge Case: Vergleich mit einem anderen Typ gibt NotImplemented zurück
def test_eq_with_different_type_returns_not_implemented():
    # Arrange
    team = Team(id=1, name="Entwicklung")

    # Act
    result = team.__eq__("kein Team")

    # Assert
    assert result is NotImplemented


# ─── Team.get_member_ids ─────────────────────────────────────────────────────

# Happy Path: get_member_ids gibt die IDs aller Mitglieder zurück
def test_get_member_ids_returns_all_user_ids(session, sample_team, sample_user, sample_user_2):
    # Arrange
    membership = Membership(
        team_id=sample_team.id,
        user_id=sample_user_2.id,
        role=Role.MEMBER,
    )
    session.add(membership)
    session.commit()
    session.refresh(sample_team)

    # Act
    result = sample_team.get_member_ids()

    # Assert
    assert sample_user.id in result
    assert sample_user_2.id in result


# Edge Case: Team ohne Mitglieder gibt leere Liste zurück
def test_get_member_ids_returns_empty_list_for_team_without_members():
    # Arrange
    team = Team(id=99, name="Leeres Team")

    # Act
    result = team.get_member_ids()

    # Assert
    assert result == []


# ─── Membership.__repr__ ─────────────────────────────────────────────────────

# Happy Path: __repr__ enthält alle wichtigen Felder
def test_membership_repr_contains_key_fields():
    # Arrange
    membership = Membership(id=1, team_id=10, user_id=5, role=Role.OWNER)

    # Act
    result = repr(membership)

    # Assert
    assert "Membership(" in result
    assert "id=1" in result
    assert "team_id=10" in result
    assert "user_id=5" in result


# ─── Membership.__eq__ ───────────────────────────────────────────────────────

# Happy Path: gleiche Felder → gleich
def test_membership_eq_returns_true_for_equal_objects():
    # Arrange
    m1 = Membership(id=1, team_id=10, user_id=5, role=Role.MEMBER)
    m2 = Membership(id=1, team_id=10, user_id=5, role=Role.MEMBER)

    # Act
    result = m1 == m2

    # Assert
    assert result is True


# Edge Case: unterschiedliche Rolle → ungleich
def test_membership_eq_returns_false_for_different_role():
    # Arrange
    m1 = Membership(id=1, team_id=10, user_id=5, role=Role.OWNER)
    m2 = Membership(id=1, team_id=10, user_id=5, role=Role.MEMBER)

    # Act
    result = m1 == m2

    # Assert
    assert result is False


# Edge Case: Vergleich mit anderem Typ gibt NotImplemented zurück
def test_membership_eq_with_different_type_returns_not_implemented():
    # Arrange
    membership = Membership(id=1, team_id=10, user_id=5, role=Role.MEMBER)

    # Act
    result = membership.__eq__("kein Membership")

    # Assert
    assert result is NotImplemented
