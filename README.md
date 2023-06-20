# FastAPI Project

This is a sample FastAPI project demonstrating a simple API for managing products, reviews, and user authentication.

## Project Structure

The project structure is organized as follows:

- `app`: Contains the main application code and modules.
  - `api`: Contains the API endpoints for products, reviews, and users.
  - `database`: Contains the database module for managing data storage.
  - `models`: Contains the data models for products, reviews, and users.
  - `security`: Contains the authentication and security modules.
  - `main.py`: The main entry point of the FastAPI application.
- `Dockerfile`: Contains the configuration for building a Docker image.
- `Makefile`: Contains development-related commands and targets.

## Endpoints

The API provides the following endpoints:

+ `/products`: Manage products (GET, POST).

+ `/products/{product_id}`: Get product details (GET), delete product (DELETE).

+ `/products/{product_id}/reviews`: Get product reviews (GET), create product review (POST).

+ `/user/signup`: User sign up (POST).

+ `/user/signin`: User sign in (POST).

For the product endpoints (`/products/*`) all read (GET) operations do not need authentication, but write operations (POST, DELETE) require.


## Usage

### Running with Docker

1. Build the Docker image:

   ```bash
   docker build -t fastapi-project .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 80:80 --rm fastapi-project
   ```

3. Open your web browser and visit http://localhost to access the API.


### Running locally
1. Clone the repository:

   ```bash
   git clone https://github.com/paconte/fastapi-project.git
   ```

2. Create a virtual enviroment, for example:
   ```bash
    cd fastapi-project
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

5. Open your web browser and visit http://localhost:8000 to access the API.


## Development Workflow

1. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your changes, write tests, and ensure the code passes linting.

   ```bash
   make fmt lint
   ```

3. Run the tests:

   ```bash
   pytest
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add your commit message"
   ```

4. Generate test coverage and check the percentage:

   ```bash
   make test
   ```

4. Push your branch to the remote repository:

   ```bash
   git push origin feature/your-feature-name
   ```

## License

This project is licensed under the MIT License.
