import bcrypt
import requests
import query as qr
import getpass
from python_graphql_client import GraphqlClient

sorare_login = GraphqlClient(
    endpoint="https://api.sorare.com/federation/graphql",
    headers={
        'content-type': 'application/json'
    }
)


def create_token(email, password, otp, aud):
    url = f'https://api.sorare.com/api/v1/users/{email}'
    response = requests.get(url)

    response_json = response.json()

    salt = response_json['salt'].encode()

    otpAttempt = otp

    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

    if otp == "":
        query = qr.loginQuery
        variables = {"input": {"email": email, "password": hashed_password}, "aud": aud}
        response = sorare_login.execute(query=query, variables=variables)
        print(f'JWT token for {response["data"]["signIn"]["currentUser"]["slug"]} is\n')
        print(response["data"]["signIn"]["jwtToken"]["token"])
    else:
        query = qr.loginOtp
        variables = {"input": {"email": email, "password": hashed_password}, "aud": aud}
        response = sorare_login.execute(query=query, variables=variables)
        challenge = response['data']['signIn']['otpSessionChallenge']
        print(challenge)
        query = qr.loginQuery
        variables = {"input": {"otpSessionChallenge": challenge, "otpAttempt": otp}, "aud": aud}
        response = sorare_login.execute(query=query, variables=variables)
        print(f'JWT token for {response["data"]["signIn"]["currentUser"]["slug"]} is\n')
        print(response["data"]["signIn"]["jwtToken"]["token"])

    user_input = input("\nPress any key to continue.")
    if user_input:
        exit()


def userInput():
    otp = ""
    print("This script generates a Sorare JWT token, see")
    print("https://github.com/sorare/api?tab=readme-ov-file#user-authentication")
    print("for more information.\n")

    email = input("Enter email: ")

    aud = input("Audience: ")

    try:
        password = getpass.getpass()
        user_input = input(f'Use 2FA? [Y/n]: ').strip().lower()

        if user_input == 'n':
            otp = ""
        else:
            otp = input(f'OTP: ')

        create_token(email=email, password=password, otp=otp, aud=aud)

    except Exception as error:
        print('ERROR', error)


if __name__ == '__main__':
    userInput()
