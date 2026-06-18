"""Unit tests for the sakshi_bhatia module."""

import pytest

from sakshi_bhatia import SakshiBhatia


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def profile():
    """Return a fresh SakshiBhatia instance."""
    return SakshiBhatia()


# ---------------------------------------------------------------------------
# Initialization / default attributes
# ---------------------------------------------------------------------------

class TestInit:
    def test_role(self, profile):
        assert profile.role == "Full-Stack Developer & Software Engineer"

    def test_education_entries(self, profile):
        assert len(profile.education) == 2
        assert "IIIT Jabalpur" in profile.education[0]
        assert "IIT Madras" in profile.education[1]

    def test_stack_is_list(self, profile):
        assert isinstance(profile.stack, list)
        assert len(profile.stack) > 0

    def test_ml_tools_is_list(self, profile):
        assert isinstance(profile.ml_tools, list)
        assert len(profile.ml_tools) > 0

    def test_superpower_contains_chess(self, profile):
        assert any("Chess" in s for s in profile.superpower)

    def test_values(self, profile):
        assert "Ship fast" in profile.values

    def test_open_to(self, profile):
        assert "Internships" in profile.open_to

    def test_fun_fact_is_string(self, profile):
        assert isinstance(profile.fun_fact, str)
        assert len(profile.fun_fact) > 0

    def test_currently_is_string(self, profile):
        assert isinstance(profile.currently, str)


# ---------------------------------------------------------------------------
# greet()
# ---------------------------------------------------------------------------

class TestGreet:
    def test_greet_returns_string(self, profile):
        result = profile.greet()
        assert isinstance(result, str)

    def test_greet_content(self, profile):
        assert "build something great" in profile.greet()


# ---------------------------------------------------------------------------
# has_skill()
# ---------------------------------------------------------------------------

class TestHasSkill:
    def test_known_stack_skill(self, profile):
        assert profile.has_skill("React") is True

    def test_known_ml_tool(self, profile):
        assert profile.has_skill("PyTorch") is True

    def test_case_insensitive(self, profile):
        assert profile.has_skill("react") is True
        assert profile.has_skill("PYTORCH") is True

    def test_unknown_skill(self, profile):
        assert profile.has_skill("Ruby on Rails") is False


# ---------------------------------------------------------------------------
# is_open_to()
# ---------------------------------------------------------------------------

class TestIsOpenTo:
    def test_known_opportunity(self, profile):
        assert profile.is_open_to("Internships") is True

    def test_case_insensitive(self, profile):
        assert profile.is_open_to("internships") is True
        assert profile.is_open_to("RESEARCH") is True

    def test_unknown_opportunity(self, profile):
        assert profile.is_open_to("Acting") is False


# ---------------------------------------------------------------------------
# add_skill()
# ---------------------------------------------------------------------------

class TestAddSkill:
    def test_add_new_stack_skill(self, profile):
        result = profile.add_skill("Rust", category="stack")
        assert result is True
        assert "Rust" in profile.stack

    def test_add_new_ml_skill(self, profile):
        result = profile.add_skill("TensorFlow", category="ml_tools")
        assert result is True
        assert "TensorFlow" in profile.ml_tools

    def test_add_duplicate_returns_false(self, profile):
        assert profile.add_skill("React", category="stack") is False

    def test_invalid_category_raises(self, profile):
        with pytest.raises(ValueError, match="Unknown category"):
            profile.add_skill("Go", category="languages")

    def test_default_category_is_stack(self, profile):
        profile.add_skill("Svelte")
        assert "Svelte" in profile.stack


# ---------------------------------------------------------------------------
# remove_skill()
# ---------------------------------------------------------------------------

class TestRemoveSkill:
    def test_remove_from_stack(self, profile):
        cat = profile.remove_skill("React")
        assert cat == "stack"
        assert "React" not in profile.stack

    def test_remove_from_ml_tools(self, profile):
        cat = profile.remove_skill("PyTorch")
        assert cat == "ml_tools"
        assert "PyTorch" not in profile.ml_tools

    def test_remove_nonexistent_returns_none(self, profile):
        assert profile.remove_skill("COBOL") is None


# ---------------------------------------------------------------------------
# summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def test_summary_contains_role(self, profile):
        assert profile.role in profile.summary()

    def test_summary_contains_counts(self, profile):
        s = profile.summary()
        assert f"{len(profile.stack)} stack items" in s
        assert f"{len(profile.ml_tools)} ML tools" in s


# ---------------------------------------------------------------------------
# education_count()
# ---------------------------------------------------------------------------

class TestEducationCount:
    def test_default_count(self, profile):
        assert profile.education_count() == 2

    def test_after_append(self, profile):
        profile.education.append("MIT — PhD (2030–2034)")
        assert profile.education_count() == 3


# ---------------------------------------------------------------------------
# all_skills()
# ---------------------------------------------------------------------------

class TestAllSkills:
    def test_returns_sorted_list(self, profile):
        skills = profile.all_skills()
        assert skills == sorted(skills)

    def test_no_duplicates(self, profile):
        skills = profile.all_skills()
        assert len(skills) == len(set(skills))

    def test_contains_items_from_both(self, profile):
        skills = profile.all_skills()
        assert "React" in skills
        assert "PyTorch" in skills

    def test_union_size(self, profile):
        expected = len(set(profile.stack + profile.ml_tools))
        assert len(profile.all_skills()) == expected
