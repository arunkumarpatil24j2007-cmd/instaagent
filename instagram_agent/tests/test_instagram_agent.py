"""
Unit and Integration Tests for Instagram Specialist Agent.
Verifies contract conformity, sub-component execution, and mock tool pipelines.
"""

import unittest
from instagram_agent.agent.instagram_agent import InstagramSpecialistAgent
from instagram_agent.schemas.input_contract import (
    InstagramAgentInput,
    BrandContext,
    TaskSpec,
    Constraints,
)
from instagram_agent.schemas.output_contract import InstagramAgentOutput


class TestInstagramSpecialistAgent(unittest.TestCase):

    def setUp(self):
        self.agent = InstagramSpecialistAgent()

    def test_missing_context_validation(self):
        """Should detect missing brand_name and topic/objective and return missing_context status."""
        input_data = InstagramAgentInput(
            brand=BrandContext(brand_name=""),
            task=TaskSpec(topic="", objective=""),
            constraints=Constraints(content_type="carousel"),
        )
        output = self.agent.run(input_data)
        self.assertEqual(output.status, "missing_context")
        self.assertIsNotNone(output.missing_context)
        self.assertIn("brand.brand_name", output.missing_context.missing_fields)

    def test_reels_coming_soon(self):
        """Should return coming_soon status when content_type or task target_format is reel."""
        input_data = InstagramAgentInput(
            brand=BrandContext(brand_name="BrandX"),
            task=TaskSpec(topic="Fast Reels", target_format="reel"),
            constraints=Constraints(content_type="reel"),
        )
        output = self.agent.run(input_data)
        self.assertEqual(output.status, "coming_soon")
        self.assertEqual(output.content_type, "reel")
        self.assertIsNotNone(output.reels_notice)
        self.assertTrue(output.reels_notice.coming_soon)

    def test_carousel_generation(self):
        """Should produce multi-slide carousel with valid SVGs, hooks, and captions."""
        input_data = InstagramAgentInput(
            brand=BrandContext(
                brand_name="DevFlow",
                industry="Tech",
                target_audience="Developers",
                account_handle="@devflow",
                colors=["#0F172A", "#3B82F6", "#10B981"],
            ),
            task=TaskSpec(
                type="create_content",
                topic="5 Microservices Anti-Patterns",
                objective="authority",
                target_format="carousel",
            ),
            constraints=Constraints(
                content_type="carousel",
                max_slides=5,
                approval_required=True,
            ),
        )
        output = self.agent.run(input_data)
        self.assertEqual(output.status, "ready_for_review")
        self.assertEqual(output.content_type, "carousel")
        self.assertIsNotNone(output.carousel)
        self.assertGreaterEqual(output.carousel.total_slides, 3)
        self.assertLessEqual(output.carousel.total_slides, 5)

        # Check slide SVGs
        for slide in output.carousel.slides:
            self.assertIn("<svg", slide.graphic_svg)
            self.assertIn("1080", slide.graphic_svg)

        # Check creative summary
        self.assertTrue(output.creative.required)
        self.assertGreaterEqual(len(output.creative.assets), 3)

        # Check hooks & captions
        self.assertGreater(len(output.hooks), 0)
        self.assertGreater(len(output.captions), 0)

        # Check quality
        self.assertIsNotNone(output.quality)
        self.assertGreaterEqual(output.quality.overall_score, 8.0)

    def test_static_post_generation(self):
        """Should produce 1:1 branded static post graphic and caption."""
        input_data = InstagramAgentInput(
            brand=BrandContext(
                brand_name="SereneTea",
                industry="Beverage",
                target_audience="Tea Enthusiasts",
                account_handle="@serenetea",
                colors=["#1B4332", "#52B788", "#D8F3DC"],
            ),
            task=TaskSpec(
                type="create_content",
                topic="The 3 Rituals of Mindful Mornings",
                objective="engagement",
                target_format="static_post",
            ),
            constraints=Constraints(content_type="static_post"),
        )
        output = self.agent.run(input_data)
        self.assertEqual(output.status, "ready_for_review")
        self.assertEqual(output.content_type, "static_post")
        self.assertIsNotNone(output.static_post)
        self.assertIn("<svg", output.static_post.graphic_svg)
        self.assertEqual(len(output.creative.assets), 1)
        self.assertEqual(output.creative.assets[0].dimensions, "1080x1080")

    def test_story_sequence_generation(self):
        """Should produce 9:16 story sequence frames with interactive elements."""
        input_data = InstagramAgentInput(
            brand=BrandContext(
                brand_name="FitFlow",
                industry="Fitness",
                target_audience="Athletes",
                account_handle="@fitflow",
                colors=["#18181B", "#EF4444", "#F59E0B"],
            ),
            task=TaskSpec(
                type="create_content",
                topic="Flash Drop: Elite Grip Socks",
                objective="sales",
                target_format="story_sequence",
            ),
            constraints=Constraints(content_type="story_sequence", max_stories=4),
        )
        output = self.agent.run(input_data)
        self.assertEqual(output.status, "ready_for_review")
        self.assertEqual(output.content_type, "story_sequence")
        self.assertIsNotNone(output.story_sequence)
        self.assertGreaterEqual(output.story_sequence.total_stories, 3)

        for story in output.story_sequence.stories:
            self.assertIn("<svg", story.graphic_svg)
            self.assertIn("1920", story.graphic_svg)

    def test_content_calendar_generation(self):
        """Should create multi-week post calendar without crashing or requiring critique."""
        input_data = InstagramAgentInput(
            brand=BrandContext(
                brand_name="SaaSMetrics",
                industry="Software",
                target_audience="Founders",
                account_handle="@saasmetrics",
            ),
            task=TaskSpec(
                type="create_content_calendar",
                topic="Product Retention Masterclass",
                objective="lead_generation",
                target_format="content_calendar",
            ),
            constraints=Constraints(
                content_type="content_calendar",
                calendar_duration="2_weeks",
                posts_per_week=4,
            ),
        )
        output = self.agent.run(input_data)
        self.assertEqual(output.status, "ready_for_review")
        self.assertEqual(output.content_type, "content_calendar")
        self.assertIsNotNone(output.calendar)
        self.assertEqual(output.calendar.duration, "2 Weeks")
        self.assertEqual(output.calendar.total_posts, 8)
        self.assertEqual(len(output.calendar.calendar_entries), 8)

    def test_run_raw_dict_conformance(self):
        """Raw dictionary input must return valid dictionary conformant to contract."""
        payload = {
            "brand": {
                "brand_name": "Acme Tools",
                "industry": "Hardware",
                "account_handle": "@acmetools",
            },
            "task": {
                "type": "create_content",
                "topic": "Power Drills Maintenance",
                "target_format": "carousel",
            },
            "constraints": {
                "content_type": "carousel",
                "max_slides": 4,
            },
        }
        res = self.agent.run_raw(payload)
        self.assertIsInstance(res, dict)
        self.assertEqual(res.get("status"), "ready_for_review")
        self.assertEqual(res.get("platform"), "instagram")
        self.assertIn("carousel", res)
        self.assertIn("quality", res)


if __name__ == "__main__":
    unittest.main()
