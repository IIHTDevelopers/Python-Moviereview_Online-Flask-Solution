import unittest
import requests
from app import *
from tests.TestUtils import TestUtils

class FunctionalMovieReviewTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.test_obj = TestUtils()

    def test_default_movies_db_count(self):
        try:
            response = self.client.get('/movies')
            data = response.get_json()
            result = (
                response.status_code == 200 and
                isinstance(data, list) and
                len(data) >= 2 and
                all("id" in movie and "title" in movie and "director" in movie for movie in data)
            )
            self.test_obj.yakshaAssert("TestDefaultMoviesDbCount", result, "functional")
            print("TestDefaultMoviesDbCount = Passed" if result else "TestDefaultMoviesDbCount = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestDefaultMoviesDbCount", False, "functional")
            print(f"TestDefaultMoviesDbCount = Failed | Exception: {e}")

    def test_get_all_movies(self):
        try:
            response = self.client.get("/movies")
            json_data = response.get_json()
            result = (
                response.status_code == 200 and
                isinstance(json_data, list) and
                len(json_data) >= 2 and
                all("id" in movie and "title" in movie and "director" in movie for movie in json_data)
            )
            self.test_obj.yakshaAssert("TestGetAllMovies", result, "functional")
            print("TestGetAllMovies = Passed" if result else "TestGetAllMovies = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestGetAllMovies", False, "functional")
            print(f"TestGetAllMovies = Failed | Exception: {e}")

    def test_get_movie_by_id(self):
        try:
            response = self.client.get('/movie/1')
            json_data = response.get_json()
            result = (
                response.status_code == 200 and
                isinstance(json_data, dict) and
                json_data.get("title") == "Inception"
            )
            self.test_obj.yakshaAssert("TestGetMovieById", result, "functional")
            print("TestGetMovieById = Passed" if result else "TestGetMovieById = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestGetMovieById", False, "functional")
            print(f"TestGetMovieById = Failed | Exception: {e}")

    def test_post_review_valid_movie_id_yaksha(self):
        try:
            valid_review = {
                "movie_id": 1,
                "review": "Amazing cinematography!",
                "rating": 5
            }
            response = self.client.post('/api/reviews', json=valid_review)
            data = response.get_json()
            result = (
                response.status_code == 201 and
                isinstance(data, dict) and
                any(r.get("review") == "Amazing cinematography!" and r.get("movie_id") == 1 for r in reviews_db)
            )
            self.test_obj.yakshaAssert("TestPostReviewValidMovieID", result, "functional")
            print("TestPostReviewValidMovieID = Passed" if result else "TestPostReviewValidMovieID = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestPostReviewValidMovieID", False, "functional")
            print(f"TestPostReviewValidMovieID = Failed | Exception: {e}")

    def test_login_page_load_and_success(self):
        try:
            get_response = self.client.get('/login')
            get_success = get_response.status_code == 200 and b"<form" in get_response.data

            post_response = self.client.post('/login', data={
                'username': 'admin',
                'password': 'secret'
            })
            post_success = post_response.status_code == 200 and b"Logged in as admin" in post_response.data

            result = get_success and post_success
            self.test_obj.yakshaAssert("TestLoginPageLoadAndSuccess", result, "functional")
            print("TestLoginPageLoadAndSuccess = Passed" if result else "TestLoginPageLoadAndSuccess = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestLoginPageLoadAndSuccess", False, "functional")
            print(f"TestLoginPageLoadAndSuccess = Failed | Exception: {e}")

    def test_home_page_loads(self):
        try:
            response = self.client.get('/')
            result = response.status_code == 200 and b'Inception' in response.data
            self.test_obj.yakshaAssert("TestHomePageLoads", result, "functional")
            print("TestHomePageLoads = Passed" if result else "TestHomePageLoads = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestHomePageLoads", False, "functional")
            print(f"TestHomePageLoads = Failed | Exception: {e}")

    def test_add_third_movie_success(self):
        try:
            new_movie = {
                "id": 3,
                "title": "Dune",
                "director": "Denis Villeneuve"
            }
            response = self.client.post('/movies', json=new_movie)
            result = (
                response.status_code == 201 and
                any(m["id"] == 3 and m["title"] == "Dune" for m in movies_db)
            )
            self.test_obj.yakshaAssert("TestAddThirdMovieSuccess", result, "functional")
            print("TestAddThirdMovieSuccess = Passed" if result else "TestAddThirdMovieSuccess = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestAddThirdMovieSuccess", False, "functional")
            print(f"TestAddThirdMovieSuccess = Failed | Exception: {e}")

    def test_submit_rating_url_loads(self):
        try:
            response = self.client.get('/rate')
            result = response.status_code == 200 and b"Submit Rating" in response.data
            self.test_obj.yakshaAssert("TestSubmitRatingUrlLoads", result, "functional")
            print("TestSubmitRatingUrlLoads = Passed" if result else "TestSubmitRatingUrlLoads = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestSubmitRatingUrlLoads", False, "functional")
            print(f"TestSubmitRatingUrlLoads = Failed | Exception: {e}")


if __name__ == "__main__":
    unittest.main()
