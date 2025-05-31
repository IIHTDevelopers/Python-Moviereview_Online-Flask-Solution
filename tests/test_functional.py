import unittest
import requests
from app import *
from tests.TestUtils import TestUtils

class FunctionalMovieReviewTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.test_obj = TestUtils()
        self.base_url = "http://127.0.0.1:5000"

    def test_default_movies_db_count(self):
        try:
            response = self.client.get('/movies')
            data = response.get_json()
            result = (
                response.status_code == 200 and
                isinstance(data, list) and
                len(data) >= 2
            )
            self.test_obj.yakshaAssert("TestDefaultMoviesDbCount", result, "functional")
            print("TestDefaultMoviesDbCount = Passed" if result else "TestDefaultMoviesDbCount = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestDefaultMoviesDbCount", False, "functional")
            print(f"TestDefaultMoviesDbCount = Failed | Exception: {e}")

    def test_get_movie_by_id(self):
        try:
            response = self.client.get('/movie/1')
            data = response.get_json()
            result = (
                response.status_code == 200 and
                data.get("title") == "Inception"
            )
            self.test_obj.yakshaAssert("TestGetMovieById", result, "functional")
            print("TestGetMovieById = Passed" if result else "TestGetMovieById = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestGetMovieById", False, "functional")
            print(f"TestGetMovieById = Failed | Exception: {e}")

    def test_postman_added_movie_exists(self):
        try:
            response = requests.get(f"{self.base_url}/movies")
            movies = response.json()
            movie = next((m for m in movies if m["id"] == 3 and m["title"] == "Dune"), None)
            result = movie is not None
            self.test_obj.yakshaAssert("TestPostmanAddedMovieExists", result, "functional")
            print("TestPostmanAddedMovieExists = Passed" if result else "TestPostmanAddedMovieExists = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestPostmanAddedMovieExists", False, "functional")
            print(f"TestPostmanAddedMovieExists = Failed | Exception: {e}")

    def test_postman_added_rating_five_exists(self):
        try:
            response = requests.get(f"{self.base_url}/api/reviews")
            reviews = response.json()
            review = next(
                (r for r in reviews if r["movie_id"] == 1 and r.get("rating") == 5),
                None
            )
            result = review is not None
            self.test_obj.yakshaAssert("TestPostmanAddedRatingFiveExists", result, "functional")
            print("TestPostmanAddedRatingFiveExists = Passed" if result else "TestPostmanAddedRatingFiveExists = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestPostmanAddedRatingFiveExists", False, "functional")
            print(f"TestPostmanAddedRatingFiveExists = Failed | Exception: {e}")


    def test_home_page_loads(self):
        try:
            response = self.client.get('/')
            result = response.status_code == 200 and b'Inception' in response.data
            self.test_obj.yakshaAssert("TestHomePageLoads", result, "functional")
            print("TestHomePageLoads = Passed" if result else "TestHomePageLoads = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestHomePageLoads", False, "functional")
            print(f"TestHomePageLoads = Failed | Exception: {e}")

    def test_login_form_success(self):
        try:
            response = self.client.post('/login', data={
                'username': 'admin',
                'password': 'secret'
            })
            result = response.status_code == 200 and b"Logged in as admin" in response.data
            self.test_obj.yakshaAssert("TestLoginFormSuccess", result, "functional")
            print("TestLoginFormSuccess = Passed" if result else "TestLoginFormSuccess = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestLoginFormSuccess", False, "functional")
            print(f"TestLoginFormSuccess = Failed | Exception: {e}")

    def test_rating_form_loads(self):
        try:
            response = self.client.get('/rate_movies')
            result = response.status_code == 200
            self.test_obj.yakshaAssert("TestRatingFormLoads", result, "functional")
            print("TestRatingFormLoads = Passed" if result else "TestRatingFormLoads = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestRatingFormLoads", False, "functional")
            print(f"TestRatingFormLoads = Failed | Exception: {e}")

    def test_submit_rating_five_exists_from_url(self):
        try:
            # Step 1: Fetch existing reviews from the live URL
            response = requests.get(f"{self.base_url}/api/reviews")
            # Step 2: Parse the JSON response
            reviews = response.json()

            # Step 3: Check if any review has movie_id=1 and rating=5
            match = next(
                (r for r in reviews if int(r.get("movie_id")) == 1 and int(r.get("rating")) == 5),
                None
            )

            result = match is not None

            # Step 4: Assert the result
            self.test_obj.yakshaAssert("TestRatingFiveExistsFromURL", result, "functional")
            print("TestRatingFiveExistsFromURL = Passed" if result else "TestRatingFiveExistsFromURL = Failed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestRatingFiveExistsFromURL", False, "functional")
            print(f"TestRatingFiveExistsFromURL = Failed | Exception: {e}")


if __name__ == '__main__':
    unittest.main()
