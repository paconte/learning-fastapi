from app.security.hash import Hasher

# Create an instance of the Hasher class
hasher = Hasher()


def test_hasher_create():
    # Test the creation of a hashed password
    password = "password123"
    hashed_password = hasher.create(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password


def test_hasher_verify_valid():
    # Test the verification of a valid password
    password = "password123"
    hashed_password = hasher.create(password)
    result = hasher.verify(password, hashed_password)
    assert result is True


def test_hasher_verify_invalid():
    # Test the verification of an invalid password
    password = "password123"
    hashed_password = hasher.create(password)
    invalid_password = "invalid_password"
    result = hasher.verify(invalid_password, hashed_password)
    assert result is False
