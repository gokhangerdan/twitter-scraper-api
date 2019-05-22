from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from resources.mongo_connect import MongoConnect

from resources.twitter_clinet import get_worldwide_trends
from resources.twitter_clinet import get_twitter_account
from resources.twitter_clinet import get_search_results


app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mongodb_connection = MongoConnect("YOUR_USER_NAME", "YOUR_PASSWORD")


class User:

    class Signup(Resource):

        def post(self):
            email = request.args.get("email")
            username = request.args.get("username")
            password = request.args.get("password")
            secret_question = request.args.get("secret_question")
            answer = request.args.get("answer")

            return mongodb_connection.create_user(email, username, password, secret_question, answer)


    class Signin(Resource):

        def post(self):
            username = request.args.get("username")
            password = request.args.get("password")

            return mongodb_connection.check_user(username, password)

        def put(self):
            secret_question = request.args.get("secret_question")
            answer = request.args.get("answer")
            new_password = request.arg.get("new_password")

            return mongodb_connection.change_pwd(secret_question, answer, new_password)


    class Profile(Resource):

        def get(self):
            token = request.args.get("token")
            return mongodb_connection.get(token)

        def put(self):
            params = request.args
            return mongodb_connection.put(params)

class Twitter:

    class worldwideTrends(Resource):

        def post(self):
            return get_worldwide_trends()

    class twitterAccount(Resource):

        def post(self):
            uname = request.args.get("uname")
            return get_twitter_account(uname)

    class twitterSearch(Resource):

        def post(self):
            q = request.args.get("q")
            return get_search_results(q)


api.add_resource(User.Signup, "/user/signup")
api.add_resource(User.Signin, "/user/signin")
api.add_resource(User.Profile, "/user/profile")

api.add_resource(Twitter.worldwideTrends, "/twitter/worldwide_trends")
api.add_resource(Twitter.twitterAccount, "/twitter/twitter_account")
api.add_resource(Twitter.twitterSearch, "/twitter/search_results")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
