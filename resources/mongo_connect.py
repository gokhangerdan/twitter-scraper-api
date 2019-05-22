import pymongo
from uuid import uuid4
import json
from bson.json_util import dumps


secret_question_key = "s3Cr3T_qUeSt10N"
answer_key = "aNsW3r"
password_key = "pAsSw0Rd"

class MongoConnect:

    def __init__(self, username, password):
        client = pymongo.MongoClient("mongodb+srv://%s:%s@gokhang1327-e5zxe.mongodb.net/test?retryWrites=true" % (username, password))
        db = client.twitscan
        self.col = db.user

    def create_user(self, email, username, password, secret_question, answer):
        check_email = self.col.count_documents(
            {
                "email": email
            }
        )
        check_username = self.col.count_documents(
            {
                "username": username
            }
        )
        
        try:
            if check_email == 0 and check_username == 0 and len(password) >= 6:
                token = uuid4().hex

                self.col.insert_one(
                    {
                        "token": token,
                        "email": email,
                        "username": username,
                        password_key: password,
                        secret_question_key: secret_question,
                        answer_key: answer
                    }
                )
                return {
                    "token": token
                }
            
            else:
                if check_email == 1:
                    return {
                        "message": "This email address is already in use."
                    }

                if username == 1:
                    return {
                        "message": "This username is already in use."
                    }

                if len(password) < 6:
                    return {
                        "message": "Password must be atleast 6 character long."
                    }

                else:
                    return {
                        "message": "Invalid parameters."
                    }
        
        except Exception as e:
            return {
                "message": str(e)
            }

    def check_user(self, username, password):
        check_email_password = self.col.count_documents(
            {
                "email": username,
                password_key: password
            }
        )
        check_username_password = self.col.count_documents(
            {
                "username": username,
                password_key: password
            }
        )
        
        if check_email_password == 1:
            user_data = self.col.find_one(
                {
                    "email": username,
                    password_key: password
                }
            )
            return {
                "token": user_data["token"]
            }

        elif check_username_password == 1:
            user_data = self.col.find_one(
                {
                    "username": username,
                    password_key: password
                }
            )
            return {
                "token": user_data["token"]
            }

        else:
            return {
                "message": "The username or password is incorrect."
            }

    def get(self, token):
        try:
            doc = self.col.find_one(
                {
                    "token": token
                },
                {
                    "_id": 0,
                    password_key: 0,
                    secret_question_key: 0,
                    answer_key: 0
                }
            )

            return doc

        except Exception as e:
            return {
                "message": str(e)
            }

    def put(self, params):
        try:
            query = {
                "token": params["token"]
            }
            result = self.col.update_one(
                query,
                {
                    "$set": params
                }
            )
            
            if result.matched_count:
                return {
                    "message": "The user information updated successfully."
                }
            else:
                return {
                    "message": "Invalid token for this action."
                }

        except Exception as e:
            return {
                "message": str(e)
            }

    def change_pwd(self, secret_question, answer, new_password):
        check_secret = self.col.count_documents(
            {
                secret_question_key: secret_question,
                answer_key: answer
            }
        )
        
        if check_secret == 1:
            query = {
                secret_question_key: secret_question,
                answer_key: answer
            }
            result = self.col.update_one(
                query,
                {
                    "$set": {
                        password_key: new_password
                    }
                }
            )

            if result.matched_count:
                return {
                    "message": "The user password updated successfully."
                }
            else:
                return {
                    "message": "Security question or answer is wrong."
                }
