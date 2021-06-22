# It's always better to store test data externally and/or not in a py file. But since there's only one
# instance of test data, I think it's okay to hardcode in this situation.
def get_test_user_login():
    return "brian_wilson@test.com", "password"
