from django.test import TestCase
from django.utils.dateparse import parse_datetime
from pytz import UTC
from rest_framework import status
from rest_framework.test import APIRequestFactory

from ..models import Choice, Question
from .views import QuestionViewSet


class QuestionViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create some sample data for testing
        self.question1 = Question.objects.create(question_text="Question 1")
        self.question2 = Question.objects.create(question_text="Question 2")
        self.choice1 = Choice.objects.create(
            question=self.question1, choice_text="Choice 1", votes=5
        )
        self.choice2 = Choice.objects.create(
            question=self.question1, choice_text="Choice 2", votes=3
        )

    def execute_list_request(self, params=None):
        """Execute the list request on the QuestionViewSet with optional parameters."""
        request = self.factory.get("/api/questions/", data=params)
        view = QuestionViewSet.as_view({"get": "list"})
        return view(request)

    def execute_retrieve_request(self, question_id, params=None):
        """Execute the retrieve request on the QuestionViewSet with optional parameters."""
        request = self.factory.get(f"/api/questions/{question_id}/", data=params)
        view = QuestionViewSet.as_view({"get": "retrieve"})
        return view(request, question_id=question_id)

    def check_response_common(self, response):
        """Check the common response attributes for the list request."""
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response_pub_dates = [
            parse_datetime(question_data["pub_date"]).astimezone(UTC)
            for question_data in response.data
        ]
        self.assertEqual(response_pub_dates, sorted(response_pub_dates, reverse=True))
        return response.data

    def check_question_data(self, params):
        """
        Check the question data in the response against the given question.
        Params:
            - question_data: dict, question data in the response
            - question: Question, the expected question object
            - choices_count: int, number of expected choices
            - include_votes: bool, whether votes should be included in the response
        """
        question_data = params["question_data"]
        question = params["question"]
        choices_count = params["choices_count"]
        include_votes = params["include_votes"]

        self.assertEqual(question_data["id"], question.id)
        self.assertEqual(question_data["question_text"], question.question_text)

        response_pub_date = parse_datetime(question_data["pub_date"]).astimezone(UTC)
        question_pub_date = question.pub_date.astimezone(UTC)
        self.assertAlmostEqual(response_pub_date, question_pub_date)

        self.assertEqual(len(question_data["choices"]), choices_count)

        for choice_data in question_data["choices"]:
            choice = Choice.objects.get(id=choice_data["id"])
            self.assertEqual(choice_data["choice_text"], choice.choice_text)

            self.assertEqual("votes" in choice_data, include_votes)
            if include_votes:
                self.assertEqual(choice_data["votes"], choice.votes)

    def test_list_questions(self):
        """Test the list request without including votes."""
        response = self.execute_list_request()
        response_data = self.check_response_common(response)

        # Test question1 data
        question1_data = response_data[1]  # The question with the older pub_date
        self.check_question_data(
            {
                "question_data": question1_data,
                "question": self.question1,
                "choices_count": 2,
                "include_votes": False,
            }
        )

        # Test question2 data
        question2_data = response_data[0]  # The question with the latest pub_date
        self.check_question_data(
            {
                "question_data": question2_data,
                "question": self.question2,
                "choices_count": 0,
                "include_votes": False,
            }
        )

    def test_list_questions_with_votes(self):
        """Test the list request including votes."""
        response = self.execute_list_request(params={"include_votes": "true"})
        response_data = self.check_response_common(response)

        # Test question1 data
        question1_data = response_data[1]  # The question with the older pub_date
        self.check_question_data(
            {
                "question_data": question1_data,
                "question": self.question1,
                "choices_count": 2,
                "include_votes": True,
            }
        )

        # Test question2 data
        question2_data = response_data[0]  # The question with the latest pub_date
        self.check_question_data(
            {
                "question_data": question2_data,
                "question": self.question2,
                "choices_count": 0,
                "include_votes": False,
            }
        )

    def test_retrieve_question(self):
        """Test the retrieve request without including votes."""
        response = self.execute_retrieve_request(self.question1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test question1 data
        self.check_question_data(
            {
                "question_data": response.data,
                "question": self.question1,
                "choices_count": 2,
                "include_votes": False,
            }
        )

    def test_retrieve_question_with_votes(self):
        """Test the retrieve request including votes."""
        response = self.execute_retrieve_request(
            self.question1.id, params={"include_votes": "true"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test question1 data
        self.check_question_data(
            {
                "question_data": response.data,
                "question": self.question1,
                "choices_count": 2,
                "include_votes": True,
            }
        )
